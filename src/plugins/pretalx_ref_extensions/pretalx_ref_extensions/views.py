from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pretalx.api.auth import UserTokenAuthentication
from pretalx.api.pagination import PageNumberPagination
from pretalx.person.models import User
from pretalx.submission.domain.submission import add_speaker

from .domain import get_or_create_user, update_user_details
from .permissions import OrganiserTeamManagerPermission, SubmissionUpdatePermission
from .serializers import (
    AddSpeakerSilentSerializer,
    TeamAddMemberSerializer,
    UserCreateSerializer,
    UserListSerializer,
)


def _user_response_data(user, created):
    return {
        "code": user.code,
        "email": user.email,
        "name": user.name,
        "created": created,
    }


class UserCreateView(APIView):
    """List users of an organiser's teams, or get-or-create a user by email
    (creation never sends an invitation email). With ``update: true``, an
    existing user's name/locale are overwritten with the given non-blank values."""

    authentication_classes = [UserTokenAuthentication]
    permission_classes = [OrganiserTeamManagerPermission]
    pagination_class = PageNumberPagination

    def get(self, request, **kwargs):
        users = User.objects.filter(teams__organiser=request.organiser).distinct().order_by("code")
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(users, request, view=self)
        serializer = UserListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user, created = get_or_create_user(
            email=data["email"], name=data.get("name"), locale=data.get("locale")
        )
        updated = False
        if not created and data["update"]:
            updated = update_user_details(
                user,
                name=data.get("name"),
                locale=data.get("locale"),
                log_user=request.user,
            )
        response_data = _user_response_data(user, created)
        response_data["updated"] = updated
        return Response(
            response_data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class TeamAddMemberView(APIView):
    """Add a user directly to a team's members, bypassing invite/accept."""

    authentication_classes = [UserTokenAuthentication]
    permission_classes = [OrganiserTeamManagerPermission]

    def post(self, request, **kwargs):
        team = get_object_or_404(request.organiser.teams, pk=kwargs["team_id"])
        serializer = TeamAddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user, created = get_or_create_user(
            email=data["email"], name=data.get("name"), locale=data.get("locale")
        )
        already_member = team.members.filter(pk=user.pk).exists()
        if not already_member:
            team.members.add(user)
            team.organiser.log_action(
                "pretalx.invite.orga.accept", person=user, orga=True
            )
        response_data = _user_response_data(user, created)
        response_data["added"] = not already_member
        return Response(response_data, status=status.HTTP_200_OK)


class AddSpeakerSilentView(APIView):
    """Attach a speaker to a submission by email. Never sends an invitation email."""

    authentication_classes = [UserTokenAuthentication]
    permission_classes = [SubmissionUpdatePermission]

    def get_submission(self):
        # cached so the permission check and the handler share one query
        if not hasattr(self, "_submission"):
            self._submission = get_object_or_404(
                self.request.event.submissions, code__iexact=self.kwargs["code"]
            )
        return self._submission

    def post(self, request, **kwargs):
        submission = self.get_submission()
        serializer = AddSpeakerSilentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user, created = get_or_create_user(
            email=data["email"],
            name=data.get("name"),
            locale=data.get("locale"),
            event=submission.event,
        )
        speaker = add_speaker(
            submission, user=user, name=data.get("name"), log_user=request.user
        )
        response_data = _user_response_data(user, created)
        response_data["speaker_code"] = speaker.code
        return Response(response_data, status=status.HTTP_200_OK)
