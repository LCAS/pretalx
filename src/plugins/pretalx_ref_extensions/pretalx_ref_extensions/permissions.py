from django.db.models import Count, Q
from rest_framework.permissions import BasePermission


class OrganiserTeamManagerPermission(BasePermission):
    """Requires a token whose user manages teams for the requested organiser.

    Mirrors the organiser-coverage check pretalx's core API applies to
    organiser-level endpoints: a token must either be scoped to all events,
    or explicitly cover every event of the organiser.
    """

    def has_permission(self, request, view):
        organiser = getattr(request, "organiser", None)
        if not organiser or not request.user or not request.user.is_authenticated:
            return False
        token = request.auth
        if token and not token.all_events:
            coverage = organiser.events.aggregate(
                total=Count("pk"),
                uncovered=Count("pk", filter=~Q(pk__in=token.limit_events.all())),
            )
            if not coverage["total"] or coverage["uncovered"]:
                return False
        return request.user.teams.filter(
            organiser=organiser, can_change_teams=True
        ).exists()


class SubmissionUpdatePermission(BasePermission):
    """Requires the same permission core pretalx uses for add-speaker."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        submission = view.get_submission()
        return request.user.has_perm("submission.update_submission", submission)
