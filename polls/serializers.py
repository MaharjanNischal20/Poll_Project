from rest_framework import serializers
from .models import Poll, Choice, Vote
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name']

    def get_name(self, obj):
        return obj.get_full_name()


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class ChoiceSerializer(serializers.ModelSerializer):
    voted = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = '__all__'

    def get_voted(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return Vote.objects.filter(user=request.user, choice=obj).exists()
        return False


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, context={'request': None})

    class Meta:
        model = Poll
        fields = ("id", "question", "choices", "created_at")

    def to_representation(self, instance):
        request = self.context.get('request')
        self.fields['choices'].context.update({'request': request})
        return super().to_representation(instance)


class VoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    choice = ChoiceSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'user', 'choice']
