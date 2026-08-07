from django.urls import path

from .views import AddSpeakerSilentView, TeamAddMemberView, UserCreateView

urlpatterns = [
    path(
        "api/organisers/<slug:organiser>/plugins/ref-extensions/users/",
        UserCreateView.as_view(),
        name="ref_extensions.users.create",
    ),
    path(
        "api/organisers/<slug:organiser>/plugins/ref-extensions/teams/"
        "<int:team_id>/add-member/",
        TeamAddMemberView.as_view(),
        name="ref_extensions.teams.add_member",
    ),
    path(
        "api/events/<slug:event>/plugins/ref-extensions/submissions/"
        "<slug:code>/add-speaker-silent/",
        AddSpeakerSilentView.as_view(),
        name="ref_extensions.submissions.add_speaker_silent",
    ),
]
