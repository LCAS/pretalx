from pretalx.person.domain.user import create_user
from pretalx.person.models import User


def get_or_create_user(*, email, name=None, locale=None, event=None):
    """Find a user by email, or silently create one (no invitation email sent)."""
    try:
        return User.objects.get(email__iexact=email), False
    except User.DoesNotExist:
        kwargs = {}
        if locale:
            kwargs["locale"] = locale
        user = create_user(email=email, name=name or "", event=event, **kwargs)
        return user, True
