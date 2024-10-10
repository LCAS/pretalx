from django.utils.translation import gettext_lazy as _

from pretalx.common.text.phrases import Phrases


class CfPPhrases(Phrases, app="cfp"):
    go_to_cfp = _("Go to CfP")

    auth_password_reset = _(
        "If we know a user by this email address (who has not requested a password reset in the last 24 hours), we will send you an e-mail containing further instructions. If you don’t "
        "see the email within the next minutes, check your spam inbox!"
    )
    auth_reset_fail = _(
        "This link was not valid. Make sure you copied the complete URL from the "
        "email and that the email is no more than 24 hours old."
    )
    auth_reset_success = _("Awesome! You can now log in using your new password.")
    token_regenerated = _(
        "Your API token has been regenerated. The previous token will not be usable "
        "any longer."
    )

    submission_withdrawn = _("Your paper has been withdrawn.")
    submission_not_withdrawn = _(
        "Your paper can’t be withdrawn at this time – please contact us if you need to withdraw your paper!"
    )
    submission_confirmed = _(
        "Your session has been confirmed – we’re looking forward to seeing you!"
    )
    submission_was_confirmed = _(
        "This paper has already been confirmed – we’re looking forward to seeing you!"
    )
    submission_not_confirmed = _(
        "This paper cannot be confirmed at this time – please contact us if you think this is an error."
    )
    submission_uneditable = _("This paper cannot be edited anymore.")

    speaker_email = _("author email")
    invite_subject = _("{speaker} invites you to join their session!")
    invite_text = _(
        """Hi!

I’d like to invite you to be a presenter in the session

  “{title}”

at {event}. Please follow this link to join:

  {url}

I’m looking forward to it!
{speaker}"""
    )
    invite_invalid_email = _("Please provide a valid email address.")
    invite_sent = _("The invitation was sent!")
    invite_accepted = _(
        "You are now part of this paper! Please fill in your profile below."
    )

    submission_email_fail = _(
        "We are experiencing difficulties when sending mails, but your session was submitted successfully!"
    )

    # Translators: This string is used for headings and refers to the custom questions
    # organisers can create for their CfP.
    questions = _("Questions")
