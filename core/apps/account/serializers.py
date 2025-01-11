from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from dj_rest_auth.serializers import PasswordResetSerializer
from phonenumber_field.serializerfields import PhoneNumberField

from .models import Account


class SignUpSerializer(serializers.ModelSerializer):
	password2   					= serializers.CharField(style={"input_type":"password"}, allow_blank=False, write_only=True)

	class Meta:
		model = Account
		fields = [
			"username",
			"name",
			"surname",
			"gender",

			"email",
			"phone_number",

			"accept",

			"password",
			"password2"
		]
		extra_kwargs = {
			"password":{"write_only":True},
			"password2":{"write_only":True},
		}

	def create(self, validated_data):
		password = validated_data["password"]
		confirm_password = validated_data["password2"]

		if password != confirm_password:
			raise serializers.ValidationError("Passwords do not match")
		else:
			del validated_data["password2"]
			return Account.objects.create_user(**validated_data)


class AccountSerializer(serializers.ModelSerializer):

	class Meta:
		model = Account
		fields = (
			"id",
			"username",
			"name",
			"surname",
			"gender",
			"profile_image",

			"email",
			"phone_number",
		)
		read_only_fields = (
			"id",
		)

	def update(self, instance, validated_data):
		instance = instance.update(**validated_data)
		return instance


class SignInSerializer(serializers.Serializer):

	username	   				 	= serializers.CharField(min_length=3, max_length=125, allow_blank=False)
	password	   				 	= serializers.CharField(style={"input_type":"password"}, allow_blank=False, write_only=True)

	def validate(self, data):
		try:
			username = data.get("username")
			password = data.get("password")
			account = authenticate(username=username, password=password)
			if not account.is_active:
				raise serializers.ValidationError({"error":"Account has been deactivated"});

		except Exception:
			raise serializers.ValidationError({"error":"Invalid credentials"})

		return account


class AccountDeletionSerializer(serializers.Serializer):

	username	   				 	= serializers.CharField(min_length=3, max_length=125, allow_blank=False)
	password   	 				 	= serializers.CharField(style={"input_type":"password"}, allow_blank=False, write_only=True)


	def validate(self, attrs):
		username = attrs.get("username", None)
		password = attrs.get("password", None)

		user = authenticate(username=username, password=password)
		if user == None:
			raise serializers.ValidationError({"error":"Invalid credentials"})

		return attrs


class CustomPasswordResetSerializer(PasswordResetSerializer):
	
	def get_email_options(self):
		return {
			"email_template_name": "account/password_reset_email.html",
			
			"extra_email_context": {
				"frontend_app_domain": settings.FRONTEND_APP["DOMAIN"],
				"frontend_app_password_reset_confirm": settings.FRONTEND_APP["PASSWORD_RESET_CONFIRM"],
			}
		}

