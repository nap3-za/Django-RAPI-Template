from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from knox import views as knox_views

from core.apps.account import views as account_views


urlpatterns = [
    path('knox-authentication/', include('knox.urls')),
    path('authentication/sign-up/', account_views.SignUpView.as_view(), name="sign-up"),
    path('authentication/sign-in/', account_views.SignInView.as_view(), name="sign-in"),
    path('authentication/account/', account_views.RetrieveAuthenticatedAccount.as_view(), name="retrieve-account"),

    path('account/', include('core.apps.account.urls', namespace="account")),

    # Password related views using 3rd party app
    # re_path(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
    #     TemplateView.as_view(template_name="account/password-reset/password_reset_email.html"),
    #     name='password_reset_confirm'),
    path('rest-authentication/', include('dj_rest_auth.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)