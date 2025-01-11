from django.contrib.auth import login, authenticate, logout
from rest_framework import (
	generics,
	status,
	pagination,
	mixins,
	viewsets,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from knox.models import AuthToken

from .serializers import (
	SignUpSerializer,
	SignInSerializer,
	AccountSerializer,
	AccountDeletionSerializer,
)
from .models import Account

from core.apps.misc import permissions as app_permissions


class SignUpView(generics.CreateAPIView):
	
	serializer_class = SignUpSerializer
	permission_classes = (app_permissions.isNotAuthenticated,)

	def create(self, request, *args, **kwargs):
		data = request.data

		serializer = self.get_serializer(data=data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)

		auth_user_account = authenticate(username=data.get("username"), password=data.get("password"))
		login(request, auth_user_account)

		headers = self.get_success_headers(serializer.data)
		response_data = {
			"user": AccountSerializer(auth_user_account, context=self.get_serializer_context()).data,
			"token": AuthToken.objects.create(auth_user_account)[1]
		}
		
		return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

	def perform_create(self, serializer):
		return serializer.save()


class SignInView(generics.GenericAPIView):
	serializer_class = SignInSerializer
	permission_classes = (app_permissions.isNotAuthenticated,)

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		auth_user_account = serializer.validated_data
		response_data = {
			"user": AccountSerializer(auth_user_account, context=self.get_serializer_context()).data,
			"token": AuthToken.objects.create(auth_user_account)[1]
		}
		
		return Response(response_data, status=status.HTTP_200_OK)


class AccountViewSetPagination(pagination.PageNumberPagination):
	page_size = 10
	page_size_query_param = "size"
	max_page_size = 25


class AccountViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

	queryset = Account.objects.all_active().order_by('-username')
	serializer_class = AccountSerializer
	pagination_class = AccountViewSetPagination
	# parser_classes = (MultiPartParser, FormParser)

	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer_data = self.get_serializer(instance).data

		response_data = {
			"account": {
				**serializer_data
			},
			"isAuthUser": instance == self.request.user,
		}

		return Response(response_data)

	def perform_update(self, serializer):
		instance = self.get_object()
		if instance != self.request.user:
			return Response({"error":"You cannot update an account that doesn't belong to you"}, status=status.HTTP_403_FORBIDDEN)
		return serializer.save()


class AccountDeletionView(APIView):
	
	def post(self, request, *args, **kwargs):
		auth_user_account = request.user
		serializer = AccountDeletionSerializer(data=request.data, instance=request.user)
		serializer.is_valid(raise_exception=True)
		auth_user_account.deactivate()
		return Response(status=status.HTTP_204_NO_CONTENT)


class RetrieveAuthenticatedAccount(generics.RetrieveAPIView):
	
	serializer_class = AccountSerializer

	def get_object(self):
		return self.request.user