from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError

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


def update_user_details(user, *, name=None, locale=None, log_user=None):
    """Overwrite name/locale on an existing user where the given values differ.

    Blank values are ignored, so they never clear existing data. Returns True
    if the user was changed."""
    changes = {}
    name = (name or "").strip()
    if name and name != user.name:
        changes["name"] = name
    if locale and locale != user.locale:
        changes["locale"] = locale
    if not changes:
        return False

    errors = {}
    for field_name, value in changes.items():
        try:
            changes[field_name] = User._meta.get_field(field_name).clean(value, user)
        except DjangoValidationError as exc:
            errors[field_name] = exc.messages
    if errors:
        raise ValidationError(errors)

    old_data = {field_name: getattr(user, field_name) for field_name in changes}
    for field_name, value in changes.items():
        setattr(user, field_name, value)
    user.save(update_fields=list(changes))
    user.log_action(
        "pretalx.user.profile.update",
        person=log_user,
        orga=True,
        old_data=old_data,
        new_data=changes,
    )
    return True
