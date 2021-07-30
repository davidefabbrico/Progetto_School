"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from polls.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', loginPage, name='login'),
    path('verification/', include('verify_email.urls')),
    path('logout/', logoutUser, name='logout'),
    path('home/', homepage, name='home'),
    path('', inizio, name='inizio'),
    path('registration/', registrationPage, name='register'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="polls/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="polls/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="polls/password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="polls/password_reset_done.html"), name="password_reset_complete"),
    path('salvadati/', GeouserData, name="test_data"),
    path('filtered_data/', filtered_data, name="filtered_data"),
    path('feedback/', feedback, name="feedback"),
    path('chisiamo/', auth_views.PasswordResetCompleteView.as_view(template_name="polls/chisiamo.html"), name="chisiamo"),
    path('privacy/', auth_views.PasswordResetCompleteView.as_view(template_name="polls/privacy.html"), name="privacy"),
    path('poke/', auth_views.PasswordResetCompleteView.as_view(template_name="polls/poke.html"), name="poke"),
    path('risultati/', risultati, name="risultati"),
    path('get_all_questions_data', get_all_questions_data, name="get_all_questions_data"),
    path('save_all_questions_data/', save_all_questions_data, name="save_all_questions_data")
]

handler404 = 'polls.views.error_404_view'
handler500 = 'polls.views.error_500_view'