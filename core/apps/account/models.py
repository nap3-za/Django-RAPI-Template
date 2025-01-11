from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import Q

from phonenumber_field.modelfields import PhoneNumberField

from core.apps.misc.field_choices import (
	Genders,
)


class AccountQuerySet(models.QuerySet):

	def search(self, query=None):
		if query == None:
			return self.none()
		
		queries = str(query).split(" ")
		for query in queries:
			lookups += Q((Q(name__icontains=query) | Q(surname__icontains=query) | Q(phone_number__icontains=query) | Q(email__icontains=query)) & Q(is_active=True))
		return self.filter(lookups)

def get_profile_image_filepath(self, filename):
	return "profile_images/" + str(self.pk) +  "/profile_image.png"

class Account(AbstractBaseUser, PermissionsMixin):

	class AccountManager(BaseUserManager):
		
		def get_queryset(self):
			return AccountQuerySet(self.model, using=self.db)

		def search(self, query=None):
			return self.get_queryset().search(query=query)

		def create_user(self,username,name,surname,gender,accept,email=None,phone_number=None,password=None):
			user = self.model(
				username=username,
				name=name,
				surname=surname,
				gender=gender,
				email=email,
				phone_number=phone_number,
				accept=True,
			)
			user.set_password(password)
			user.save(using=self._db)
			
			return user

		def create_superuser(self,username,name,surname,gender,accept,email,phone_number,password):
			user = self.create_user(
				username=username,
				name=name,
				surname=surname,
				gender=gender,
				email=email,
				phone_number=phone_number,
				accept=accept,
				password=password,
			)
			user.is_superuser = True
			user.save(using=self._db)
			return user

		def all_active(self):
			return self.all().filter(is_active=True)

	username 				= models.CharField(verbose_name="username", max_length=50, unique=True, null=False, blank=False)
	name 					= models.CharField(verbose_name="name", max_length=125, unique=False, null=False, blank=False)
	surname 				= models.CharField(verbose_name="surname", max_length=125, unique=False, null=False, blank=False)
	gender 					= models.CharField(choices=Genders.choices, max_length=10, unique=False, null=False, blank=False)	
	profile_image 			= models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=False, blank=False, default="profile_images/default.png")
	
	email 					= models.EmailField(max_length=125, unique=True, null=False, blank=False)
	phone_number 			= PhoneNumberField(verbose_name="phone number",null=True, unique=True, blank=True, error_messages={"unique":"Phonenumber is already in use"})
	
	# If false then the account is deleted
	is_active 				= models.BooleanField(default=True)

	date_joined				= models.DateTimeField(auto_now_add=True)
	last_login				= models.DateTimeField(auto_now=True)	
	
	is_admin				= models.BooleanField(default=False)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	
	# Accepts the Ts&Cs of the school
	accept 					= models.BooleanField(verbose_name="accept", help_text="Terms and Conditions", default=False)

	USERNAME_FIELD = "username"
	REQUIRED_FIELDS = ["name", "surname", "gender", "email", "accept"]

	objects = AccountManager()

	def __str__(self):
		return self.full_names

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=["username", "email", "phone_number"],
				name="unique_undeleted_fields",
				condition=Q(is_active=True),
			)
		]

	@property 
	def full_names(self):
		return f"{self.name} {self.surname}"
	
	def update(self, **kwargs):
		Account.objects.filter(id=self.id).update(**kwargs)
		if "profile_image" in kwargs.keys():
			self.profile_image = kwargs["profile_image"]
			self.save()

		return Account.objects.get(id=self.id)

	def get_profile_image_filename(self):
		return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

	# Set the account as innactive and
	# schedule it for deletion
	def deactivate(self):
		Account.objects.filter(id=self.id).update(is_active=False)