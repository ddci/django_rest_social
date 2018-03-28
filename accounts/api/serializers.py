__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "22.03.2018"
__app__ = "django_rest_social"
__status__ = "Development"

import clearbit
from django.contrib.auth import get_user_model
from rest_framework import serializers
from pyhunter import PyHunter
from requests import HTTPError
from rest_framework.exceptions import ValidationError
from django_rest_social import settings

clearbit.key = settings.CLEARBIT_API_KEY
hunter = PyHunter(settings.EMAIL_HUNTER_API_KEY)

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'is_superuser'
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label='Email Address')
    email2 = serializers.EmailField(label='Confirm Email')
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=100)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
            'first_name',
            'last_name'
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")
        if settings.CLEARBIT_ENRICHMENT_ENABLED:
            # Retrieving enrichment information from Clearbit
            if not data.get('first_name') or not data.get('last_name'):
                try:
                    response = clearbit.Enrichment.find(email=email, stream=True)
                    if response:
                        if response['person']:
                            if not data.get('first_name'):
                                data['first_name'] = response['person'].get('name').get('givenName')
                            if not data.get('last_name'):
                                data['last_name'] = response['person'].get('name').get('familyName')
                except HTTPError as e:
                    print('Failed to receive enrichment for email: {}'.format(email))
                    pass

        return data

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")
        # https://hunter.io/ verifying email address
        if settings.ONLY_DELIVERABLE_EMAILS:
            try:
                hunter.email_verifier(email1)
            except Exception as e:
                print(e)
                raise ValidationError("Email address is not deliverable.")
        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data.get('first_name') or ""
        last_name = validated_data.get('last_name') or ""
        user_obj = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data
