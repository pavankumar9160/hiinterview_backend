# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import * 
from rest_framework_simplejwt.views import TokenRefreshView
 

urlpatterns = [
    
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/userprofile/',UserProfileView.as_view(), name="userprofile"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/auth/reset-password-otp/', SendOTPView.as_view(), name='send-otp'),
    path('api/auth/trainer/reset-password-otp/', TrainerSendOTPView.as_view(), name='send-trainer-otp'),
    path('api/auth/verify-password-reset-otp/',VerifyOTPView.as_view(),name="verify-otp"),
    path('api/trainers/signup/', TrainerRegisterView.as_view(), name='trainer-register'),
    path('api/trainers/login/', TrainerLoginView.as_view(), name='trainer-login'),
    path('api/trainer/logout/', LogoutView.as_view(), name='trainer-logout'),
    path('api/trainer/profile/', TrainerProfileView.as_view(), name='trainer-profile'),
    path('api/update/user-profile/',EditUserProfileView.as_view(),name ="update-userprofile"),
    path('api/users/',ShowAllUsersView.as_view(),name='users-data'),
    path('api/update-user-status/<int:id>/',UpdateUserStatusView.as_view(),name='update-user-status'),



    
    
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
