pretalx-ref-extensions
=======================

A pretalx plugin that adds a small set of API endpoints needed for
programmatic, SSO-friendly user provisioning. It does not change pretalx
core; it only orchestrates existing pretalx domain functions in ways the
stock API does not currently expose.

Why this exists
----------------

Our deployment authenticates users via SSO (see the ``pretalx-socialauth``
plugin), so accounts don't need a password or an "activate your account"
invitation email. This plugin lets an organiser API token:

* Create user accounts up front from a batch of email addresses (e.g. for
  reviewers or speakers who haven't logged in yet), without sending any
  email.
* Attach a user as a speaker on a submission by email, without sending the
  usual speaker-invitation email.
* Add a user directly to a team (e.g. as a reviewer), without going through
  the email invite/accept flow.

None of the new endpoints send email; they only call pretalx's existing
``create_user``, ``add_speaker`` and ``Team.members.add`` operations
directly, which are the same building blocks pretalx's own invitation flows
use internally, minus the mail step.

Endpoints
---------

All endpoints require a valid ``Authorization: Token <token>`` header for a
pretalx organiser API token whose user is a member of a team with
"Can change teams" permission for the target organiser (for the
organiser-level endpoints), or "Can change submissions" for the
submission-level endpoint.

``POST /api/organisers/<organiser>/plugins/ref-extensions/users/``
    Body: ``{"email": "...", "name": "...", "locale": "...", "update": false}``
    (all but ``email`` optional). Returns the existing user, or creates one
    silently. With ``"update": true``, an existing user's ``name`` and
    ``locale`` are overwritten with any non-blank values given (logged as a
    profile update); the response includes ``"updated": true/false``.

``GET /api/organisers/<organiser>/plugins/ref-extensions/users/``
    Paginated list of users who are members of any of the organiser's teams.

``POST /api/organisers/<organiser>/plugins/ref-extensions/teams/<team_id>/add-member/``
    Body: same as above. Finds-or-creates the user and adds them directly to
    the team's members, without an invite/accept step.

``POST /api/events/<event>/plugins/ref-extensions/submissions/<code>/add-speaker-silent/``
    Body: same as above. Finds-or-creates the user and attaches them as a
    speaker on the submission, without sending an invitation email.

Installation
------------

::

    pip install -e src/plugins/pretalx_ref_extensions

Restart pretalx so the plugin and its URLs are detected. No database
migrations are required.
