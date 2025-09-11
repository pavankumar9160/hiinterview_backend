
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
        
class UserProfileSerializer(serializers.ModelSerializer):
    cv_url = serializers.SerializerMethodField()
    profile_photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['fullname','email','cv','mobile_number','alt_mobile_number','profile_photo','profile_photo_url','cv_url','role']

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
             
    
      
    
    
        
   