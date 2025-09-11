from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class customUserManager(BaseUserManager):     
        def create_user(self, email, password=None, **extra_fields):
            if not email:
                raise ValueError('Email is required')
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
        def create_superuser(self, email, password=None, **extra_fields):
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            return self.create_user(email, password, **extra_fields)
        
class User(AbstractBaseUser, PermissionsMixin):
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say')
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('Single / Unmarried', 'Single / Unmarried'),
        ('Married', 'Married')
    ]
    
    TRAINING_TIME_CHOICES = [
        ("8:00-9:00", "8:00 AM — 9:00 AM"),
        ("9:00-10:00", "9:00 AM — 10:00 AM"),
        ("10:00-11:00", "10:00 AM — 11:00 AM"),
        ("11:00-12:00", "11:00 AM — 12:00 PM"),
        ("12:00-13:00", "12:00 PM — 1:00 PM"),
        ("13:00-14:00", "1:00 PM — 2:00 PM"),
        ("14:00-15:00", "2:00 PM — 3:00 PM"),
        ("15:00-16:00", "3:00 PM — 4:00 PM"),
        ("16:00-17:00", "4:00 PM — 5:00 PM"),
        ("17:00-18:00", "5:00 PM — 6:00 PM"),
        ("18:00-19:00", "6:00 PM — 7:00 PM"),
        ("19:00-20:00", "7:00 PM — 8:00 PM"),
        ("20:00-21:00", "8:00 PM — 9:00 PM"),
        ("21:00-22:00", "9:00 PM — 10:00 PM"),
    ]
     
    BUDDY_TIME_CHOICES = [
        ("9:00-10:00", "9:00 AM — 10:00 AM"),
        ("10:00-11:00", "10:00 AM — 11:00 AM"),
        ("11:00-12:00", "11:00 AM — 12:00 PM"),
        ("12:00-13:00", "12:00 PM — 1:00 PM"),
        ("13:00-14:00", "1:00 PM — 2:00 PM"),
        ("14:00-15:00", "2:00 PM — 3:00 PM"),
        ("15:00-16:00", "3:00 PM — 4:00 PM"),
    ]
    
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Mentor', 'Mentor'),
        ('Candidate', 'Candidate'),
        
    )
    
    
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    alt_mobile_number = models.CharField(max_length=15, null=True, blank=True)
    profile_photo = models.FileField(upload_to='profilePhotos/', null=True, blank=True)
    cv = models.FileField(upload_to='resumes/', null=True, blank=True)
    first_name =  models.CharField(max_length=100, null=True, blank=True)
    last_name =  models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, null=True, blank=True)    
    marital_status = models.CharField(max_length=50, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    domain =  models.CharField(max_length=100, null=True, blank=True)
    experience =  models.CharField(max_length=15, null=True, blank=True)
    profile_desc =  models.CharField(max_length=15, null=True, blank=True)
    training_time = models.CharField( max_length=15, choices=TRAINING_TIME_CHOICES, null=True, blank=True)
    buddy_days =  models.CharField(max_length=15, null=True, blank=True)
    buddy_time = models.CharField(max_length=15,choices=BUDDY_TIME_CHOICES,null=True,blank=True)
    can_candidates_visit = models.BooleanField(default=False)
    willing_to_visit = models.BooleanField(default=False)
    is_whatsapp_available = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    joined_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Candidate')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = customUserManager()
    
    def __str__(self):
        return self.email
    
    
class UserUploadedFiles(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='user_files/')
    def __str__(self):
        return self.file.name