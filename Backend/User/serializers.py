from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import ValidationError
from .models import Profile, Skill, Education, User , PasswordResetCode , Project, Experience
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'role', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        # Authenticate the user
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        if not user.is_active:
            raise serializers.ValidationError('Account disabled, contact admin')

        if not user.is_verified:
            raise serializers.ValidationError('Email is not verified')

        # Add the authenticated user to the validated data
        attrs['user'] = user
        return attrs


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    code = serializers.CharField(min_length=1, write_only=True)


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'image', 'resume_link', 'skills', 'educations']
        extra_kwargs = {
            'skills': {'required': False},
            'educations': {'required': False},
        }



class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    skills = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    educations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'profile', 'skills', 'educations']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'



