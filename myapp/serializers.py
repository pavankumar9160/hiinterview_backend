
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


# class TicketResponseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TicketResponse
#         fields = ['by', 'text', 'created_at']
        
           
class UserSessionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionHistory
        fields="__all__"  
        

# class TicketSerializer(serializers.ModelSerializer):
#     responses = TicketResponseSerializer(many=True, read_only=True)
#     class Meta:
#         model = Ticket
#         fields = ['ticket_id', 'subject', 'message', 'related_OrderId',
#                   'status', 'created_at', 'responses']




class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.fullname", read_only=True)
    sender_role = serializers.CharField(source="sender.role", read_only=True)
    attachment = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ["id", "ticket", "sender", "sender_name",'sender_role', "text","attachment",'is_read_admin','is_read_candidate',"created_at"]
        read_only_fields = ["id", "created_at", "sender_name",'sender_role']
        
    def get_attachment(self, obj):
        if obj.attachment:
            return obj.attachment.url
        return None
    


class TicketSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.fullname", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)
    mobile_number = serializers.CharField(source="user.mobile_number", read_only=True)


    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "ticketID", "user", "user_name",'email','role','mobile_number',"category", "subject", "status", "created_at", "messages"]
        read_only_fields = ["id","ticketID","created_at", "user_name", "messages"]        
                

                        
class UserProfileSerializer(serializers.ModelSerializer):
    cv_url = serializers.SerializerMethodField()
    profile_photo_url = serializers.SerializerMethodField()
    subscription = UserSubscriptionSerializer(read_only = True,many=True)
    tickets = TicketSerializer(many=True, read_only=True)
    session_history = UserSessionHistorySerializer(many=True, read_only=True, source="sessions")
    class Meta:
        model = User
        fields = ['fullname','email','cv','mobile_number','alt_mobile_number','profile_photo','profile_photo_url','cv_url','role','paid_customer','subscription','session_history','tickets']

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
    
class PartnerRegisterSerializer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    mobile = serializers.CharField(required=True)
    alt_mobile = serializers.CharField(required=False)
    dob =  serializers.DateField(required=True,input_formats=['%Y-%m-%d', '%d/%m/%Y', '%m-%d-%Y'])
    tos =  serializers.BooleanField(required=True)
    
    
    class Meta: 
        model = User
        fields=['first_name','last_name','email','password','mobile','alt_mobile','dob','password2',
                'tos']  
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate(self, validated_data):
        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return validated_data      
    

class PartnerLoginSerializer(serializers.Serializer):
    email_or_mobile = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
     



        
        
        
        

class PartnerProfileSerializer(serializers.ModelSerializer):
    pan_url = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['first_name','last_name','email','pan','pan_url','dob','mobile_number','role','aadhar_number']

    def get_pan_url(self, obj):
        if obj.pan:
            return obj.pan.url
        return None

    def update(self, instance, validated_data):
        
        pan = validated_data.get('pan', None)
        if pan and pan != "":
            if instance.pan:
                instance.pan.delete(save=False)
            instance.pan = pan

        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.save()
        return instance          
        
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
    
 
class CandidateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User 
        fields="__all__"   
        
        
class CandidateAssignmentSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(read_only = True)
    class Meta :
        model = CandidateAssignment
        fields =["id","candidate",'assigned_at']
        
    
class TrainerProfileSerializer(serializers.ModelSerializer):
    
    assigned_candidates = CandidateAssignmentSerializer(
        many=True, read_only=True, source='trainer_assignments'
    )
    class Meta:
        model = User
        fields = ['id','first_name','last_name','fullname','email','gender'
                  ,'domain','role','experience','is_active','assigned_candidates']       
    
    
        
        
      
class UpdateCandidateAssignmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = CandidateAssignment
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        
        model =  User
        fields="__all__"
        


class ServiceSerializer(serializers.ModelSerializer):
    originalPrice = serializers.DecimalField(source="original_price", max_digits=10, decimal_places=2, required=False, allow_null=True)

    features = serializers.SerializerMethodField()
    applicableDomains = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ["id","type","name","price","originalPrice","description","features","applicableDomains"]

    def get_features(self, obj):
        if obj.features:
            return [f.strip() for f in obj.features.split(",") if f.strip()]
        return []

    def get_applicableDomains(self, obj):
        if obj.applicable_domains:
            return [d.strip() for d in obj.applicable_domains.split(",") if d.strip()]
        return []
    
class CouponSerializer(serializers.ModelSerializer):
    displayPages = serializers.SerializerMethodField()
    class Meta:
        model = Coupon
        fields =['couponCode','title','description','discountType','priority','discountValue','minOrderValue','maxDiscountValue',
                 'startAt','endAt','isActive','usageLimit','usedCount','isFeatured','displayPages',
                    'productId','createdBy','updatedBy','createdAt','updatedAt']
     
    def get_displayPages(self, obj):
        if obj.displayPages:
            return [d.strip() for d in obj.displayPages.split(",") if d.strip()]
        return []    
    


class GetAssignedTrainerSerializer(serializers.Serializer):
    
    trainer = UserSerializer(read_only=True)
    candidate = UserSerializer(read_only=True)
    class Meta:
        model = CandidateAssignment
        fields =['id','trainer','candidate']
        
        




class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    attachment = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'text','attachment','created_at','is_read_admin','is_read_candidate','is_read_trainer']
    
    def get_attachment(self, obj):
        if obj.attachment:
            return obj.attachment.url
        return None    

class ChatRequestSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)
    chat_messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRequest
        fields = ['id', 'user1', 'user2', 'chat_messages', 'created_at']
    