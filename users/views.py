import random
import string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config import settings
from config.settings import RECAPTCHA_PUBLIC_KEY
from users.forms import UserRegisterForm, UserProfileForm, UserLoginForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save(commit=False)  # Getting an object without storing it in data sources
        self.object.email = self.object.email.lower()  # Convert email to lowercase
        self.object.save()
        # Send a welcome email to the user upon successful registration
        try:
            send_mail(
                subject='Congratulations on successful registration at "GEOTEST" service!',
                message='Welcome to our platform\n'
                        f'Your login is "{self.object.email}"\n'
                        'You can login here: https://geotest.tech',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.object.email],
            )
        except Exception as e:
            print(f"An exception occurred while sending email: {e}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['recaptcha_public_key'] = RECAPTCHA_PUBLIC_KEY
        return context_data


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('education_content:chapter_list')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        # Method works with success validation
        if form.is_valid():
            self.object = form.save(commit=False)
            # Проверка соответствия паролей
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if password1 or password2:
                # Проверка пароля на соответствие стандартам
                try:
                    validate_password(password1, self.object)
                except ValidationError as e:
                    form.add_error('password1', e)
                    print(form.errors)
                    return self.form_invalid(form)

                if password1 != password2:
                    form.add_error('password2', 'Passwords do not match.')
                    return self.form_invalid(form)

                self.object.set_password(password1)

                try:
                    send_mail(
                        subject='Setting new password at "GEOTEST" service',
                        message='You have successfully updated your password!\n'
                                f'Your login is "{self.object.email}"\n'
                                f'Your current password is "{password1}"\n'
                                'You can login here: https://geotest.tech',
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[self.object.email],
                    )
                except Exception as e:
                    print(f"An exception occurred while sending email: {e}")

                self.object.save()

            return super().form_valid(form)


class LoginModifiedView(LoginView):
    model = User
    form_class = UserLoginForm


def generate_new_password(request):
    # Generate a new random password
    characters = string.ascii_letters + string.digits + string.punctuation
    new_password = ''.join(random.choice(characters) for _ in range(12))
    # Send an email to the user with the new password
    send_mail(
        subject='Setting new password at "GEOTEST" service',
        message='You have successfully updated your password!\n'
                f'Your login is "{request.user.email}"\n'
                f'Your current password is "{new_password}"\n'
                'You can login here: https://geotest.tech',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
    )

    # Set the user's password to the new random password
    request.user.set_password(new_password)
    request.user.save()

    # Redirect the user to the home page
    return redirect(reverse('users:login'))
