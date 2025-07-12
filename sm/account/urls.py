from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('verify/', views.UserVerifyRegisterView.as_view(), name='verify_register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    path('reset_password/', views.UserPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password_confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]