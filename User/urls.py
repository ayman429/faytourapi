from django.urls import path
from .views import RegistrationView, LoginView, LogoutView,ChangePasswordView,display_users,display_user,update_user
from rest_framework_simplejwt import views as jwt_views
# from dj_rest_auth.views import PasswordResetView,PasswordResetConfirmView


app_name = 'users'

urlpatterns = [
    
    path('updateUser/<int:id>',update_user,name='Update_user'),
    path('getUser/<int:id>',display_user,name='Show_user'),
    path('getAllUsers',display_users,name='All_users'),   
    path('accounts/register', RegistrationView.as_view(), name='register'),
    path('accounts/login', LoginView.as_view(), name='login'),
    path('accounts/logout', LogoutView.as_view(), name='logout'),
    path('accounts/change-password', ChangePasswordView.as_view(), name='change-passwor'),
    path('accounts/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # path("restPassword/", PasswordResetView.as_view(), name="rest_password"),
    # path("restPasswordConfirm/", PasswordResetConfirmView.as_view(), name="rest_password_confirm"),
]
