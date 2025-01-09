import datetime

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase 

from core.apps.account.models import Account


class AccountTests(APITestCase):

	@classmethod
	def setUpTestData(cls):
		account = Account.objects.create_user(
			username="admin",
			name=f"name",
			surname=f"surname",		
			gender="MLE",

			email="admin@user.com",
			phone_number="+27123456780",

			accept=True,
			password="root.1352",
		)

	def test_account_sign_up(self):
		user_data = {
			"username":"user",
			"name":f"name",
			"surname":f"surname",		
			"gender":"MLE",

			"email":"user@user.com",
			"phone_number":"+27123456781",

			"accept":True,
			"password":"root.1352",
			"password2":"root.1352",
		}

		sign_up_url = reverse("sign-up")
		sign_out_url = reverse("knox_logout")

		response = self.client.post(sign_up_url, user_data, format="json")

		account = Account.objects.get(username="user")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(str(account.phone_number), "+27123456781")
		self.assertEqual(str(account), f"{account.name} {account.surname}")


	def test_account_sign_in_out(self):
		data = {
			"username":"admin",
			"password":"root.1352"
		}

		# Signing in
		sign_in_url = reverse("sign-in")
		sign_in_response = self.client.post(sign_in_url, data, format="json")
		self.assertEqual(sign_in_response.status_code, status.HTTP_200_OK)
		self.assertTrue(sign_in_response.data.get("token"))

		# Adding Authorization Token
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {sign_in_response.data['token']}")

		# Signing out
		sign_out_url = reverse("knox_logout")
		sign_out_response = self.client.post(path=sign_out_url)


	def test_account_update_delete(self):

		# Signing In
		sign_in_data = {
			"username":"admin",
			"password":"root.1352"
		}
		
		sign_in_url = reverse("sign-in")
		sign_in_response = self.client.post(sign_in_url, sign_in_data, format="json")

		# Adding Authorization Token
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {sign_in_response.data['token']}")
		
		# Testing Update
		update_data = {
			"username":"johndoe",
			"name":"John",
			"surname":"Doe",

			"email":"johndoe@user.com",
			"phone_number":"+27123456785",
		}

		account = Account.objects.get(username="admin")
		update_url = f"{reverse('account:account-list')}{str(account.pk)}/"

		update_response = self.client.put(update_url, update_data, format="json")
		
		account = Account.objects.get(username=update_data["username"])
		self.assertEqual(account.name, update_data["name"])
		self.assertEqual(account.surname, update_data["surname"])

		self.assertEqual(account.email, update_data["email"])
		self.assertEqual(account.phone_number, update_data["phone_number"])

		# Testing Delete
		deactivation_url = reverse("account:account-delete")
		deactivation_data = {
			"username":"johndoe",
			"password":"root.1352",
		}

		deactivation_response = self.client.post(deactivation_url, deactivation_data, format="json")
		self.assertEqual(deactivation_response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(Account.objects.get(username="johndoe").is_active, False)


	def test_account_extras(self):
		pass




