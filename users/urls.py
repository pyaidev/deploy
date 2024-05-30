from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import RegisterView, ProfileView, LoginModifiedView, generate_new_password
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    # Login view with a custom template
    path('', LoginModifiedView.as_view(template_name='users/login.html'), name='login'),

    # Logout view
    path('logout/', LogoutView.as_view(), name='logout'),

    # User registration view
    path('register/', RegisterView.as_view(), name='register'),

    # User profile view
    path('profile/', ProfileView.as_view(), name='profile'),

    # View to generate a new password for the user
    path('profile/genpassword', generate_new_password, name='generate_new_password'),
]
