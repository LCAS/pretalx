import pytest
from django.core import mail
from django_scopes import scopes_disabled

from pretalx.mail.models import QueuedMail
from pretalx.person.models import User
from tests.factories import (
    EventFactory,
    SubmissionFactory,
    TeamFactory,
    UserApiTokenFactory,
    UserFactory,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def event():
    return EventFactory()


@pytest.fixture
def team(event):
    return TeamFactory(
        organiser=event.organiser,
        can_change_teams=True,
        can_change_submissions=True,
        all_events=True,
    )


@pytest.fixture
def orga_user(team):
    user = UserFactory()
    team.members.add(user)
    return user


@pytest.fixture
def orga_token(orga_user):
    return UserApiTokenFactory(user=orga_user, all_events=True)


def _users_url(organiser):
    return f"/api/organisers/{organiser.slug}/plugins/ref-extensions/users/"


def _add_member_url(organiser, team_id):
    return (
        f"/api/organisers/{organiser.slug}/plugins/ref-extensions/"
        f"teams/{team_id}/add-member/"
    )


def _add_speaker_silent_url(event, code):
    return (
        f"/api/events/{event.slug}/plugins/ref-extensions/"
        f"submissions/{code}/add-speaker-silent/"
    )


def test_create_user_creates_new_user_without_email(client, event, orga_token):
    queued_before = QueuedMail.objects.count()

    response = client.post(
        _users_url(event.organiser),
        data={"email": "new.user@example.com", "name": "New User"},
        content_type="application/json",
        headers={"Authorization": f"Token {orga_token.token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new.user@example.com"
    assert data["created"] is True
    with scopes_disabled():
        assert User.objects.filter(email="new.user@example.com").exists()
    assert QueuedMail.objects.count() == queued_before
    assert len(mail.outbox) == 0


def test_create_user_is_idempotent_for_existing_email(client, event, orga_token):
    existing = UserFactory(email="existing@example.com")

    response = client.post(
        _users_url(event.organiser),
        data={"email": "Existing@example.com"},
        content_type="application/json",
        headers={"Authorization": f"Token {orga_token.token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["created"] is False
    assert data["code"] == existing.code


def test_create_user_rejected_without_can_change_teams(client, event):
    other_user = UserFactory()
    token = UserApiTokenFactory(user=other_user, all_events=True)

    response = client.post(
        _users_url(event.organiser),
        data={"email": "blocked@example.com"},
        content_type="application/json",
        headers={"Authorization": f"Token {token.token}"},
    )

    assert response.status_code == 403
    with scopes_disabled():
        assert not User.objects.filter(email="blocked@example.com").exists()


def test_add_team_member_adds_directly_without_invite(client, event, orga_token, team):
    invite_count = team.invites.count()

    response = client.post(
        _add_member_url(event.organiser, team.pk),
        data={"email": "reviewer@example.com", "name": "New Reviewer"},
        content_type="application/json",
        headers={"Authorization": f"Token {orga_token.token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["added"] is True
    with scopes_disabled():
        assert team.members.filter(email="reviewer@example.com").exists()
        assert team.invites.count() == invite_count
    assert QueuedMail.objects.count() == 0
    assert len(mail.outbox) == 0


def test_add_team_member_is_idempotent_for_existing_member(
    client, event, orga_token, team, orga_user
):
    response = client.post(
        _add_member_url(event.organiser, team.pk),
        data={"email": orga_user.email},
        content_type="application/json",
        headers={"Authorization": f"Token {orga_token.token}"},
    )

    assert response.status_code == 200
    assert response.json()["added"] is False


def test_add_speaker_silent_attaches_speaker_without_email(client, event, orga_token):
    event.plugins = "pretalx_ref_extensions"
    event.save()
    with scopes_disabled():
        submission = SubmissionFactory(event=event)

    response = client.post(
        _add_speaker_silent_url(event, submission.code),
        data={"email": "speaker@example.com", "name": "New Speaker"},
        content_type="application/json",
        headers={"Authorization": f"Token {orga_token.token}"},
    )

    assert response.status_code == 200
    with scopes_disabled():
        submission.refresh_from_db()
        speaker_emails = [s.user.email for s in submission.speakers.all()]
        assert "speaker@example.com" in speaker_emails
    assert QueuedMail.objects.count() == 0
    assert len(mail.outbox) == 0


def test_add_speaker_silent_404_when_plugin_not_enabled_for_event(
    client, event, orga_token
):
    with scopes_disabled():
        submission = SubmissionFactory(event=event)

    response = client.post(
        _add_speaker_silent_url(event, submission.code),
        data={"email": "speaker2@example.com"},
        content_type="application/json",
        headers={"Authorization": f"Token {orga_token.token}"},
    )

    assert response.status_code == 404
