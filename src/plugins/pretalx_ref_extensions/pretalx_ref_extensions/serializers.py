from rest_framework import serializers

from pretalx.person.models import User


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(required=False, allow_blank=True, default="")
    locale = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, default=None
    )


class TeamAddMemberSerializer(UserCreateSerializer):
    pass


class AddSpeakerSilentSerializer(UserCreateSerializer):
    pass


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["code", "email", "name", "locale", "is_active"]

