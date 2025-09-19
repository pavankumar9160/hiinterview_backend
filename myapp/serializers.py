
from rest_framework import serializers

from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()
class UserUploadedFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserUploadedFiles
        fields = ('file')
        
class RegisterSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(required=True)
    cv = serializers.FileField(required=False,allow_null=True,use_url=False)
    password2 = serializers.CharField(write_only=True, required=True)
    mobile = serializers.CharField(required=False)
    alt_mobile = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ('email', 'password', 'fullname', 'cv', 'password2','mobile','alt_mobile')
        
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate(self, validated_data):
        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return validated_data
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ('email', 'password')
        
        
class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields="__all__"  


class TicketResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketResponse
        fields = ['by', 'text', 'created_at']
        
           
class UserSessionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionHistory
        fields="__all__"  
        

class TicketSerializer(serializers.ModelSerializer):
    responses = TicketResponseSerializer(many=True, read_only=True)
    class Meta:
        model = Ticket
        fields = ['ticket_id', 'subject', 'message', 'related_OrderId',
                  'status', 'created_at', 'responses']
                        
class UserProfileSerializer(serializers.ModelSerializer):
    cv_url = serializers.SerializerMethodField()
    profile_photo_url = serializers.SerializerMethodField()
    tickets  = TicketSerializer(many=True, read_only=True)
    subscription = UserSubscriptionSerializer(read_only = True,many=True)
    session_history = UserSessionHistorySerializer(many=True, read_only=True, source="sessions")
    class Meta:
        model = User
        fields = ['fullname','email','cv','mobile_number','alt_mobile_number','profile_photo','profile_photo_url','cv_url','role','paid_customer','subscription','tickets','session_history']

    def get_profile_photo_url(self, obj):
        if obj.profile_photo:
            return obj.profile_photo.url
        return None

    def get_cv_url(self, obj):
        if obj.cv:
            return obj.cv.url
        return None

    def update(self, instance, validated_data):
        profile_photo = validated_data.get('profile_photo', None)
        if profile_photo == "" or profile_photo is None:
            if instance.profile_photo:
                instance.profile_photo.delete(save=False)
            instance.profile_photo = None
        else:
            instance.profile_photo = profile_photo

        
        cv = validated_data.get('cv', None)
        if cv and cv != "":
            if instance.cv:
                instance.cv.delete(save=False)
            instance.cv = cv


        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.alt_mobile_number = validated_data.get('alt_mobile_number', instance.alt_mobile_number)
        instance.save()
        return instance

    
class TrainerRegisterSerializer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    cv = serializers.FileField(required=False,allow_null=True,use_url=False)
    password2 = serializers.CharField(write_only=True, required=True)
    mobile = serializers.CharField(required=True)
    alt_mobile = serializers.CharField(required=False)
    dob =  serializers.DateField(required=True,input_formats=['%Y-%m-%d', '%d/%m/%Y', '%m-%d-%Y'])
    gender =  serializers.ChoiceField(choices=User.GENDER_CHOICES)
    marital_status =  serializers.ChoiceField(choices=User.MARITAL_STATUS_CHOICES)
    domain =  serializers.CharField(required=True)
    experience =  serializers.CharField(required=True)
    profile_desc =  serializers.CharField(required=True)
    training_time =  serializers.ChoiceField(choices=User.TRAINING_TIME_CHOICES)
    buddy_days =  serializers.CharField(required=True)
    buddy_time =  serializers.ChoiceField(choices=User.BUDDY_TIME_CHOICES)
    can_candidates_visit =  serializers.BooleanField(required=False)
    willing_to_visit =  serializers.BooleanField(required=False)
    is_whatsapp_available = serializers.BooleanField(required=False)
    
    class Meta: 
        model = User
        fields=['first_name','last_name','email','password','cv','mobile','alt_mobile','dob','password2',
                'gender','marital_status','domain','experience','profile_desc','training_time',
                'buddy_days','buddy_time','can_candidates_visit','willing_to_visit','is_whatsapp_available']  
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate(self, validated_data):
        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return validated_data  
    


class TrainerLoginSerializer(serializers.Serializer):
    email_or_mobile = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
     


class TrainerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
class AllUserProfileSerializer(serializers.ModelSerializer):
    profile_photo_url = serializers.SerializerMethodField()
    #joined_date = serializers.DateField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = User
        fields = ['id','first_name','last_name','fullname','profile_photo','email',
                  'profile_photo_url','domain','role','is_active','joined_date']   
        
    def get_profile_photo_url(self, obj):
        if obj.profile_photo:
            return obj.profile_photo.url
        return None  

class UpdateUserStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['id','is_active']    


class GetCandidateAssignmentSerializer(serializers.ModelSerializer):
    
    trainer_id = serializers.SerializerMethodField()
    buddy_id = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id','first_name','last_name','fullname','email'
                  ,'domain','role','is_active','joined_date', 'buddy_id','trainer_id']       
    
    def get_trainer_id(self, obj):
        assignment = obj.assignments.last()  
        return assignment.trainer.id if assignment and assignment.trainer else None

    def get_buddy_id(self, obj):
        assignment = obj.assignments.last()
        return assignment.buddy.id if assignment and assignment.buddy else None         
    
      
class UpdateCandidateAssignmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = CandidateAssignment
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        
        model =  User
        fields="__all__"
                

class AllTicketsSerializer(serializers.ModelSerializer):
    responses = TicketResponseSerializer(many=True, read_only=True)
    related_OrderId = UserSubscriptionSerializer(read_only = True)
    created_by = UserSerializer(read_only =True)
    class Meta:
        model = Ticket
        fields = ['ticket_id', 'subject', 'message', 'related_OrderId',
                  'status', 'created_at', 'responses','created_by']
        
        
class UpdateTicketStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Ticket
        fields=['ticket_id','status']         


# from collections import defaultdict

# class ConversationSerializer:
#     def __init__(self, messages, current_user):
#         self.messages = messages
#         self.current_user = current_user

#     def to_dict(self):
#         conversations = defaultdict(lambda: {
#             "id": None,
#             "name": None,
#             "type": None,
#             "avatarUrl": None,
#             "unread": 0,
#             "lastMessage": None,
#             "messages": []
#         })

#         for msg in self.messages:
#             other = msg.receiver if msg.sender == self.current_user else msg.sender
#             conv_id = other.fullname.lower().replace(" ", "-")

#             # figure out display name
#             if hasattr(other, "first_name") and other.first_name:  
#                 # trainer / mentor / buddy
#                 display_name = f"{other.first_name} {getattr(other, 'last_name', '')}".strip()
#                 initials = f"{other.first_name[0].upper()}{getattr(other, 'last_name', ' ')[0].upper()}"
#             else:
#                 # candidate
#                 display_name = other.fullname
#                 parts = other.fullname.split()
#                 initials = "".join([p[0].upper() for p in parts[:2]])  # take first 2 letters

#             # Init conversation if first time
#             if not conversations[conv_id]["id"]:
#                 conversations[conv_id]["id"] = conv_id
#                 conversations[conv_id]["name"] = display_name
#                 conversations[conv_id]["type"] = self.get_chat_type(other)
#                 conversations[conv_id]["avatarUrl"] = (
#                     f"https://placehold.co/100x100/1e293b/e2e8f0?text={initials}"
#                 )

#             conversations[conv_id]["messages"].append({
#                 "from": "me" if msg.sender == self.current_user else "them",
#                 "text": msg.text,
#                 "time": msg.timestamp.strftime("%Y-%m-%d %H:%M")
#             })

#             # Update last message
#             conversations[conv_id]["lastMessage"] = msg.text

#             # Update unread count
#             if msg.receiver == self.current_user and not msg.is_read:
#                 conversations[conv_id]["unread"] += 1

#         return conversations

#     def get_chat_type(self, user):
#         if user.role == "Candidate":
#             return "candidate_chat"
#         elif user.role == "Mentor":
#             return "trainer_chat"
#         else:
#             return "other"


# from collections import OrderedDict
# from django.db.models import Q



# class CandidateChatSerializer:
#     def __init__(self, candidate):
#         self.candidate = candidate

#     def get_messages(self, user):
#         """
#         Fetch messages between the candidate and another user,
#         format sender as 'me' if candidate sent, else the sender's role.
#         """
#         msgs = Message.objects.filter(
#             Q(sender=self.candidate, receiver=user) | Q(sender=user, receiver=self.candidate)
#         ).order_by("timestamp")

#         formatted = []
#         for m in msgs:
#             if m.sender == self.candidate:
#                 sender_role = "me"
#             else:
#                 sender_role = m.sender.role  # Keep exact case: Admin, Mentor, Candidate

#             formatted.append({
#                 "sender": sender_role,
#                 "text": m.text,
#                 "time": m.timestamp.strftime("%Y-%m-%d %H:%M")
#             })

#         return formatted

#     def get_avatar(self, user):
#         """Generate avatar placeholder URL with initials."""
#         if user.role == "Mentor":
#             initials = f"{user.first_name[0].upper()}{getattr(user, 'last_name', ' ')[0].upper()}"
#         else:  # Admin or Candidate
#             parts = user.fullname.split()
#             initials = "".join([p[0].upper() for p in parts[:2]])
#         return f"https://placehold.co/100x100/1e293b/e2e8f0?text={initials}"

#     def get_display_name(self, user):
#         """Display name based on role."""
#         if user.role == "Mentor":
#             display_name = f"{user.first_name} {getattr(user, 'last_name', '')}".strip()
#             display_name += " (Your Mentor)"
#         elif user.role == "Admin":
#             display_name = "Admin Support"
#         else:  # Candidate
#             display_name = user.fullname
#         return display_name

#     def to_dict(self):
#         chat_dict = OrderedDict()

#         # Admin chat
#         admin_user = User.objects.filter(role="Admin").first()
#         if admin_user:
#             chat_dict["admin-support"] = {
#                 "name": self.get_display_name(admin_user),
#                 "avatarUrl": self.get_avatar(admin_user),
#                 "unread": Message.objects.filter(sender=admin_user, receiver=self.candidate, is_read=False).count(),
#                 "type": "admin",
#                 "messages": self.get_messages(admin_user)
#             }

#         # Candidate's assigned Mentor
#         assignment = CandidateAssignment.objects.filter(candidate=self.candidate).first()
#         if assignment and assignment.trainer:
#             trainer = assignment.trainer
#             chat_dict[f"mentor-{trainer.id}"] = {
#                 "name": self.get_display_name(trainer),
#                 "avatarUrl": self.get_avatar(trainer),
#                 "unread": Message.objects.filter(sender=trainer, receiver=self.candidate, is_read=False).count(),
#                 "type": "normal",
#                 "messages": self.get_messages(trainer)
#             }

#         # Candidate's assigned Buddy
#         if assignment and assignment.buddy:
#             buddy = assignment.buddy
#             chat_dict[f"request-{buddy.id}"] = {
#                 "name": f"Buddy Day Request: {buddy.fullname}",
#                 "avatarUrl": self.get_avatar(buddy),
#                 "unread": Message.objects.filter(sender=buddy, receiver=self.candidate, is_read=False).count(),
#                 "type": "request",
#                 "status": "Accepted",  # dynamic if needed
#                 "details": "TCS - Technical Round (Java)",  # dynamic if needed
#                 "messages": self.get_messages(buddy)
#             }

#         return chat_dict

        
    
        
   