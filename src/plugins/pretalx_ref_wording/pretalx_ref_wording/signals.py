from django.dispatch import receiver

from pretalx.common.signals import register_locales


@receiver(register_locales)
def register_ref_wording_locale(sender, **kwargs):
    """Registers the 'en-rex' locale, a variant of English with overridden
    terminology for REF-style output review processes.

    Returning this even when `sender` is None (i.e. no event context) makes
    this locale discoverable by pretalx's makemessages management command.
    """
    return [("en-rex", "English (REF Outputs)")]
