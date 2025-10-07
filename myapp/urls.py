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
    path('api/admin/candidate-assignments/',GetCandidateAssignemtView.as_view(),name='candidate-assignments'),
    path('api/admin/update-candidate-assignments/',UpdateCandidateAssignment.as_view(),name='update-candidate-assignments'),
    path('api/update-user-payment-status/',UpdatePaymentAndSubscriptionView.as_view(),name='update-candidate-payment-status'),
    path("api/website-status/", WebsiteStatusView.as_view(), name="website-status"),
    # path("api/tickets/create/", TicketCreateView.as_view(), name="ticket-create"),
    # path('api/tickets/',GetAllTicketsView.as_view(), name="tickets"),
    # path('api/update-ticket-status/',UpdateTicketStatusView.as_view(), name="update-ticket-status"),
    path("tickets/", AllTicketsListView.as_view(), name="ticket-list"),
    path("api/tickets/create/", TicketCreateView.as_view(), name="ticket-create"),
    path("tickets/<int:pk>/", TicketDetailView.as_view(), name="ticket-detail"),
    path("messages/create/", MessageCreateView.as_view(), name="message-create"),
    path("tickets/update-status/", UpdateTicketStatusView.as_view(), name="update-status"),
    path('api/services/', ServiceListView.as_view(), name='service-list'),
    path('api/coupons/', CouponListView.as_view(), name='coupon-list'),
    path('api/partner/login/', PartnerLoginView.as_view(), name='partner-login'),
    path('api/partner/signup/', PartnerRegisterView.as_view(), name='partner-register'),
    path('api/partnerprofile/',PartnerProfileView.as_view(), name="partnerprofile"),
    path('api/update/partner-profile/',EditPartnerProfileView.as_view(),name ="update-partnerprofile"),




    




     
          
          

    # path('api/admin/chat-conversation/',ConversationView.as_view(),name='admin-chat-conversation'),
    # path('api/user/candidate-chat/',CandidateChatView.as_view(),name='candidate-chat')





    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
