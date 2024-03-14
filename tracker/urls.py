from django.urls import path

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import home_page, contact_us, login_user, logout_user, register_user, about_us, user_profile, reset_password_sent, reset_password_complete, privacy_policy

app_name = "tracker"

urlpatterns = [
    path('', home_page, name='home'),
    path('contact-us/', contact_us, name='contact-us'),
    path('about-us/', about_us, name='about-us'),
    path('log-in/', login_user, name='log-in'),
    path('log-out/', logout_user, name='log-out'),
    path('register/', register_user, name='register'),
    path('profile/', user_profile, name='profile'),
    path('privacy-policy/', privacy_policy, name='privacy-policy'),
    path('reset_password_sent/', reset_password_sent, name='reset_password_sent'),
    path('reset_password_complete/', reset_password_complete,
         name='reset_password_complete'),
    # Reset password urls#####################################################
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html',
         success_url=reverse_lazy('tracker:reset_password_sent')), name='reset_password'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'),
         name='reset_password_sent'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password_confirm.html',
         success_url=reverse_lazy('tracker:reset_password_complete')), name='password_reset_confirm'),

    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='reset_password_complete.html'), name='password_reset_complete'),
    ###########################################################################
]


##########################
