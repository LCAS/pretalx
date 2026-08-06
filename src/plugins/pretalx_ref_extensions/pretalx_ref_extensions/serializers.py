from rest_framework import serializers


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
