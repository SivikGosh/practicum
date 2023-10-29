from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from . import views

app_name = 'users'

logout_template = 'users/logged_out.html'
login_template = 'users/login.html'
password_change_template = 'users/password_change_form.html'
password_change_done_template = 'users/password_change_done.html'
password_reset_template = 'users/password_reset_form.html'
password_reset_done_template = 'users/password_reset_done.html'
password_reset_confirm_template = 'users/password_reset_confirm.html'
password_reset_complete_template = 'users/password_reset_complete.html'

urlpatterns = [
    path(
        'logout/',
        LogoutView.as_view(
            template_name=logout_template),
        name='logout'
    ),

    path(
        'signup/',
        views.SignUp.as_view(),
        name='signup'
    ),

    path(
        'login/',
        LoginView.as_view(
            template_name=login_template),
        name='login'
    ),

    path(
        'password_change/',
        PasswordChangeView.as_view(
            template_name=password_change_template),
        name='password_change'
    ),

    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name=password_change_done_template),
        name='password_change_done'
    ),

    path(
        'password_reset/',
        PasswordResetView.as_view(
            template_name=password_reset_template),
        name='password_reset'
    ),

    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name=password_reset_done_template),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name=password_reset_confirm_template),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name=password_reset_complete_template),
        name='password_reset_complete'
    )
]
