from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.permissions import *
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *

import pyotp
from django.core.mail import send_mail

from .permissions import IsAdmin, IsMentor, IsCandidate, IsPartner
from .utils.google_sheets import add_user_to_sheet  # <-- import





# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    def post(self, request):
        password = request.data.get('password'),
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            
            user = User.objects.create_user(
                email = request.data.get('email'),
                password = request.data.get('password'),
                fullname = request.data.get('fullname'),
                mobile_number = request.data.get('mobile')
                
            )
            
            
            alt_mobile = request.data.get('altMobile')
            
            if alt_mobile:
                user.alt_mobile_number = alt_mobile
                user.save()
                
                
            cv = request.FILES.get('cv')
            
            if cv:
                user.cv = request.FILES.get('cv')
                user.save()
            
            sheet_data = {
                "email": user.email,
                "password": password,
                'hash_password': user.password,
                "fullname": user.fullname,
                "mobile": user.mobile_number,
                "alt_mobile": user.alt_mobile_number if alt_mobile else "",
                "cv": user.cv.name if cv else ""
            }
            add_user_to_sheet(sheet_data)    
           
            return Response({"success":True, "message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            
            user = authenticate(username=email, password=password)
            
            if user is None:
               return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_active:
               return Response(
                    {"message": "Your account is inactive. Please contact support."},
                    status=status.HTTP_403_FORBIDDEN
                )
            if  user.role=="Candidate" or user.role=="Admin":
                refresh = RefreshToken.for_user(user)
              
                return Response({
                    "success": True,
                    "message": "User logged in successfully",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "role": user.role,
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist() 
            return Response({"success": True, "message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class UserProfileView(APIView):
    permission_classes = [IsCandidate]    
    serializer_class = UserProfileSerializer
    
    def get(self,request):
        user_details = request.user
        if user_details is None:
            return Response({"error": "user not found"},status=status.HTTP_400_BAD_REQUEST)
        
        user = (
            User.objects
            .prefetch_related('tickets','sent_messages','subscription','sessions')
            .get(id=request.user.id)
        )
        serializer= self.serializer_class(user)
        return Response(serializer.data)   
    

class EditUserProfileView(APIView):
    permission_classes = [IsCandidate]
    serializer_class = UserProfileSerializer
    
    def put(self,request):
        user = request.user
        
        try:
            profile = User.objects.get(email=user.email)
        except User.DoesnotExist:
            return Response({"error":"Profile not found"},status= status.HTTPS_404_NOT_FOUND)    
        
        serializer = self.serializer_class(profile,data=request.data,partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    


class SendOTPView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            email = request.data.get('email')
            
            if User.objects.filter(email=email,role='Candidate').first():
                secret_key = pyotp.random_base32()
                totp = pyotp.TOTP(secret_key, interval=300)
                otp_value = totp.now()
                print(otp_value)
                cd
                send_mail(
                    subject='Email Verification Code from Hi Interview',
                    message=(
                        f'Dear User,\n\n'
                        f'To verify your email address, please use the following One-Time Password (OTP):\n\n'
                        f'{otp_value}\n\n'
                        
                        f'Otp Valid for 5 Minutes\n\n'
                       
                        f'If you did not request this verification, please ignore this email.\n\n'
                        f'Thank you,\n'
                        
                    ),
                    from_email='hiinterview@gmail.com',
                    recipient_list=[email],
                    fail_silently=False,
                )

                return Response({'message': 'OTP sent to email', "secret_key":secret_key}, status=status.HTTP_200_OK)
            
            return Response({'error': 'User not found with this email'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Failed to send OTP email', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TrainerSendOTPView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            email = request.data.get('email')
            
            user = User.objects.filter(email=email, role='Mentor').first()
            
            if user:
                secret_key = pyotp.random_base32()
                totp = pyotp.TOTP(secret_key, interval=300)
                otp_value = totp.now()
                print(otp_value)
                
                send_mail(
                    subject='Email Verification Code from Hi Interview',
                    message=(
                        f'Dear User,\n\n'
                        f'To verify your email address, please use the following One-Time Password (OTP):\n\n'
                        f'{otp_value}\n\n'
                        f'Otp Valid for 5 Minutes\n\n'
                        f'If you did not request this verification, please ignore this email.\n\n'
                        f'Thank you,\n'
                    ),
                    from_email='hiinterview@gmail.com',
                    recipient_list=[email],
                    fail_silently=False,
                )

                return Response(
                    {'message': 'OTP sent to email', "secret_key": secret_key},
                    status=status.HTTP_200_OK
                )
            
            return Response(
                {'error': 'Mentor not found with this email'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        except Exception as e:
            return Response(
                {'error': 'Failed to send OTP email', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
   
            
class VerifyOTPView(APIView):
    permission_classes = []

    def post(self, request):
        
        secret_key = request.data.get('secret_key')
        otp_value = request.data.get('otpValue')
        email = request.data.get('email')
        password = request.data.get('password')
        print(otp_value)
        
        
        print(secret_key)
        
        
        if  not secret_key or not otp_value:
            return Response({'message': 'Missing secret_key, or otpValue'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            veri_otp =pyotp.TOTP(secret_key,interval=300)
            print(veri_otp)
            
            if not veri_otp.verify(otp_value, valid_window=1):
                
                return Response({'message':  'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not email or not password:
                return Response({'message': 'Missing email or password'}, status=status.HTTP_400_BAD_REQUEST)
            
            try: 
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                return Response({'message': 'OTP verified & password updated successfully'}, status=status.HTTP_200_OK)

            except User.DoesNotExists:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"message": "OTP Verification failed",'error':str(e)},status = status.HTTP_400_BAD_REQUEST)
        
       
    
class TrainerRegisterView(APIView):
    
    permission_classes=[AllowAny]
    serializer_class = TrainerRegisterSerializer
    def post(self,request):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            
            user = User.objects.create_user(
                email = request.data.get('email'),
                password = request.data.get('password'),
                first_name = request.data.get('first_name'),
                last_name = request.data.get('last_name'),
                mobile_number = request.data.get('mobile'),
                dob = request.data.get('dob'),
                gender = request.data.get('gender'),
                marital_status = request.data.get('marital_status'),
                domain = request.data.get('domain'),
                experience = request.data.get('experience'),
                profile_desc = request.data.get('profile_desc'),
                training_time = request.data.get('training_time'),
                buddy_days = request.data.get('buddy_days'), 
                buddy_time = request.data.get('buddy_time'),
                can_candidates_visit = request.data.get('can_candidates_visit'),
                willing_to_visit = request.data.get('willing_to_visit'),
                is_whatsapp_available = request.data.get('is_whatsapp_available'),         
                role = "Mentor"
                
                
            )
            
            
            alt_mobile = request.data.get('alt_mobile')
            
            if alt_mobile:
                user.alt_mobile_number = alt_mobile
                user.save()
                
                
            cv = request.FILES.get('cv')
            
            if cv:
                user.cv = request.FILES.get('cv')
                user.save()
                
           
            return Response({"success":True, "message": "Trainer account created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class TrainerLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = TrainerLoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email_or_mobile = serializer.validated_data.get('email_or_mobile')
            password = serializer.validated_data.get('password')
         
            user = authenticate(username=email_or_mobile, password=password)
          
            if user is None:
               return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_active:
               return Response(
                    {"message": "Your account is inactive. Please contact support."},
                    status=status.HTTP_403_FORBIDDEN
                )
               
            if user.role == "Mentor":
                refresh = RefreshToken.for_user(user)
              
                return Response({
                    "success": True,
                    "message": "Trainer logged in successfully",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    

class PartnerRegisterView(APIView):
    
    permission_classes=[AllowAny]
    serializer_class = PartnerRegisterSerializer
    def post(self,request):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            
            user = User.objects.create_user(
                email = request.data.get('email'),
                password = request.data.get('password'),
                first_name = request.data.get('first_name'),
                last_name = request.data.get('last_name'),
                mobile_number = request.data.get('mobile'),
                dob = request.data.get('dob'),
                is_tos = request.data.get('tos'),    
                role = "Partner"  
            )
            
            
            alt_mobile = request.data.get('alt_mobile')
            
            if alt_mobile:
                user.alt_mobile_number = alt_mobile
                user.save()
            return Response({"success":True, "message": "Partner account created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class PartnerLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PartnerLoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email_or_mobile = serializer.validated_data.get('email_or_mobile')
            password = serializer.validated_data.get('password')
         
            user = authenticate(username=email_or_mobile, password=password)
          
            if user is None:
               return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_active:
               return Response(
                    {"message": "Your account is inactive. Please contact support."},
                    status=status.HTTP_403_FORBIDDEN
                )
               
            if user.role == "Partner":
                refresh = RefreshToken.for_user(user)
              
                return Response({
                    "success": True,
                    "message": "Partner logged in successfully",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
class PartnerProfileView(APIView):
    permission_classes = [IsPartner]   
    serializer_class = PartnerProfileSerializer
    
    def get(self,request):
        user = request.user
        if user is None:
            return Response({"error": "partner not found"},status=status.HTTP_400_BAD_REQUEST)
        serializer= self.serializer_class(user)
        return Response(serializer.data)      
    
    
class EditPartnerProfileView(APIView):
    permission_classes = [IsPartner]
    serializer_class = PartnerProfileSerializer
    
    def put(self,request):
        user = request.user
        
        try:
            profile = User.objects.get(email=user.email)
        except User.DoesnotExist:
            return Response({"error":"Profile not found"},status= status.HTTPS_404_NOT_FOUND)    
        
        serializer = self.serializer_class(profile,data=request.data,partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
                  
            
            

class TrainerProfileView(APIView):
    permission_classes = [IsMentor]   
    serializer_class = TrainerProfileSerializer
    
    def get(self,request):
        user = request.user
        if user is None:
            return Response({"error": "user not found"},status=status.HTTP_400_BAD_REQUEST)
        serializer= self.serializer_class(user)
        return Response(serializer.data)     
    
    

class ShowAllUsersView(APIView):
    permission_classes=[IsAdmin]
    serializer_class = AllUserProfileSerializer
    
    def get(self,request):
        users = User.objects.all()
        serializer = self.serializer_class(users,many=True)
        return Response(serializer.data) 
    
    
class UpdateUserStatusView(APIView):
    
    permission_classes = [IsAdmin]
    serializer_class = UpdateUserStatusSerializer
    def put(self,request,id):
        user = User.objects.get(id=id)
        
        serializer = self.serializer_class(user,data=request.data,partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User Status Updated Successfully"}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_200_OK) 
    

class GetCandidateAssignemtView(APIView):
    permission_classes=[IsAdmin]
    serializer_class = GetCandidateAssignmentSerializer
    
    def get(self,request):
        users = User.objects.all()
        serializer = self.serializer_class(users,many=True)
        return Response(serializer.data)         
            

class UpdateCandidateAssignment(APIView):
    
    permission_classes = [IsAdmin]
    serializer_class = UpdateCandidateAssignmentSerializer
    
    def post(self, request):
        candidate_id = request.data.get("candidate")
        trainer_id = request.data.get("trainer")
        buddy_id = request.data.get("buddy")

        if not candidate_id:
            return Response({"error": "Candidate ID is required"}, status=400)

        assignment = CandidateAssignment.objects.filter(candidate_id=candidate_id).first()

        if assignment:
            serializer = UpdateCandidateAssignmentSerializer(assignment, data=request.data, partial=True)
        else:
            serializer = UpdateCandidateAssignmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
        
        

# class ConversationView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         messages = Message.objects.filter(
#             Q(sender=request.user) | Q(receiver=request.user)
#         ).select_related("sender", "receiver").order_by("timestamp")

#         serializer = ConversationSerializer(messages, current_user=request.user)
#         return Response(serializer.to_dict(), status=200)
    

# class CandidateChatView(APIView):
#     permission_classes = [IsCandidate]

#     def get(self, request):
#         if request.user.role != "Candidate":
#             return Response({"error": "Only candidates can access this"}, status=403)

#         serializer = CandidateChatSerializer(request.user)
#         return Response(serializer.to_dict(), status=200)    
        
        
 

from django.shortcuts import get_object_or_404


# class UpdatePaymentAndSubscriptionView(APIView):
#     permission_classes = [IsCandidate]  

#     def post(self, request):
#         user = request.user
#         data = request.data

#         paid_customer = data.get("paid_candidate")
#         subscription_name = data.get("subscription_name")

#         if paid_customer is None or subscription_name is None:
#             return Response(
#                 {"message": "paid_candidate and subscription_name are required."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         user.paid_customer = bool(paid_customer)
#         user.save()

#         subscription, created = UserSubscription.objects.get_or_create(user=user)
#         subscription.subscription_name = subscription_name
#         subscription.save()

#         return Response({
#             "message": "Payment status and subscription updated successfully.",
#             "paid_customer": user.paid_customer,
#             "subscription_name": subscription.subscription_name
#         }, status=status.HTTP_200_OK)
      
      

class UpdatePaymentAndSubscriptionView(APIView):
    permission_classes = [IsCandidate]  

    def post(self, request):
        user = request.user
        data = request.data

        paid_customer = data.get("paid_candidate")
        subscriptions = request.data.get("subscriptions", [])
        
        if paid_customer is None or subscriptions is None  :
            return Response(
                {"message": "paid_candidate or subscription_name or subscription_domain or subscription_price are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.paid_customer = bool(paid_customer)
        user.save()

        
        for sub in subscriptions:
            UserSubscription.objects.create(
                user=user,
                subscription_name=sub["name"],
                subscription_price=sub["price"],
                subscription_domain=sub.get("domain", "")
            )

        return Response({
            "message": "Payment status and subscription updated successfully.",
            "paid_customer": user.paid_customer,
        }, status=status.HTTP_200_OK)
        
        


class WebsiteStatusView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        status_obj = WebsiteStatus.objects.first()
        return Response({
            "is_active": status_obj.is_active if status_obj else True
        }, status=status.HTTP_200_OK)        
            
    

# class TicketCreateView(APIView):
#     permission_classes = [IsCandidate]

#     def post(self, request):
#         data = request.data

#         related_orderId = request.data.get("related_orderId")
#         subject = request.data.get("subject")
#         message = request.data.get("message")
#         ticket_status =request.data.get("status","Open")
#         created_by = request.user
#         last_id = Ticket.objects.count() + 1
#         ticket_id = f"TCK-{9000 + last_id}"
#         subscription = None
#         if related_orderId:
#             try:
#                 subscription = UserSubscription.objects.get(id=related_orderId)
#             except UserSubscription.DoesNotExist:
#                 return Response(
#                     {"error": "Invalid subscription ID"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#         Ticket.objects.create(
#             ticket_id = ticket_id,
#             subject=subject,
#             status = ticket_status,
#             created_by=created_by,
#             message = message,
#             related_OrderId = subscription 
#         )    
#         return Response({"success":True, "message": "Trainer account created successfully"}, status=status.HTTP_201_CREATED)
                              


# class GetAllTicketsView(APIView):
    
#     permission_classes = [IsAdmin]
#     serializer_class = AllTicketsSerializer
    
#     def get(self,request):   
         
#         tickets = Ticket.objects.select_related('related_OrderId', 'created_by').all();
#         serializer = self.serializer_class(tickets,many=True)
#         return Response(serializer.data)
        
 
# class UpdateTicketStatusView(APIView):      
     
#     permission_classes = [IsAdmin]
#     serializer_class = UpdateTicketStatusSerializer
    
#     def post(self, request):
#         status = request.data.get("status")
#         ticket_id = request.data.get("ticketId")
        
#         if not status and not ticket_id:
#             return Response({"error": "Ticket Update Status Failed"}, status=400)

#         ticket = Ticket.objects.filter(ticket_id=ticket_id).first()

#         if ticket:
#             serializer = UpdateTicketStatusSerializer(ticket, data=request.data, partial=True)
#         else:
#             serializer = UpdateTicketStatusSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400) 
        




# Create Ticket
class TicketCreateView(APIView):
    permission_classes = [IsCandidate]

    def post(self, request):
        user = request.user
        data = request.data

        subject = data.get('subject', '').strip()
        description = data.get('description', '').strip()

        if not subject or not description:
            return Response({"detail": "Subject and description are required."}, status=status.HTTP_400_BAD_REQUEST)

        ticket = Ticket.objects.create(
            user=user,
            subject=subject,
            ticketID='TCK-' + str(Ticket.objects.count() + 1),
        )

        Message.objects.create(
            ticket=ticket,
            sender=user,
            text=description
        )

        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    




class AllTicketsListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):

        tickets = Ticket.objects.select_related('user').prefetch_related('messages').all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
        


# Retrieve a single Ticket with messages
class TicketDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)


# Add a message (chat) to a ticket
class MessageCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ticketID = request.data.get("ticketID")
        text = request.data.get('text')
        
        if not ticketID or not text:
            return Response({"detail": "TicketID and text are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ticket = Ticket.objects.get(ticketID =ticketID)
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)
        
        message = Message.objects.create(ticket=ticket,sender=request.user,text=text)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class UpdateTicketStatusView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ticketID = request.data.get("ticketID")
        ticket_status = request.data.get('status')
        
        if not ticketID or not status:
            return Response({"detail": "TicketID and status are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ticket = Ticket.objects.get(ticketID =ticketID)
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)
        
        ticket.status = ticket_status
        ticket.save()
        
        return Response({"message":"status updated successfully"} , status=status.HTTP_200_OK)    



class ServiceListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)        
        

from django.utils.timezone import now


class CouponListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        today = now()
        coupons = Coupon.objects.filter(
            isActive=True,
                isDeleted=False,
                startAt__lte=today,
                endAt__gte=today
        )
        serializer = CouponSerializer(coupons, many=True)
        return Response(serializer.data)
     
                    
       
       
        
        

    