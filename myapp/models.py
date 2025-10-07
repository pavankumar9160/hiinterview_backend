from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid
import random
import string




class WebsiteStatus(models.Model):
    website_status = models.CharField( max_length=50, default="toggle_website_status")
    is_active = models.BooleanField(default=True)  
    updated_at = models.DateTimeField(auto_now=True)

    


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
        ('Partner', 'Partner'),
        
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
    pan = models.FileField(upload_to='documents/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    joined_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Candidate')
    paid_customer = models.BooleanField(default=False)
    is_tos = models.BooleanField(default=False)
    partner_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    aadhar_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = customUserManager()
    

    def save(self, *args, **kwargs):
        if self.role == 'Partner' and not self.partner_id:
            base_name = (self.first_name or self.username).upper()
            random_number = ''.join(random.choices(string.digits, k=3))
            self.partner_id = f"{base_name[:6]}{random_number}"
        super().save(*args, **kwargs)
        
    
    def __str__(self):
        return self.email
    
    
class UserUploadedFiles(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='user_files/')
    def __str__(self):
        return self.file.name
    
 


class CandidateAssignment(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignments", limit_choices_to={'role': 'Candidate'})
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="trainer_assignments", limit_choices_to={'role': 'Mentor'})
    buddy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="buddy_assignments", limit_choices_to={'role': 'Mentor'})
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assignment for {self.candidate.fullname}"


# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
#     text = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)



class UserSubscription(models.Model):
    SUBSCRIPTION_CHOICES = [
        ("Silver", "Silver"),
        ("Bronze", "Bronze"),
        ("Gold", "Gold"),
        ("Diamond", "Diamond"),
        ("Custom", "Custom"),
    ]
    
    SUBSCRIPTION_STATUS = [
        ("Pending", "Pending"),
        ("Delivered", "Delivered"),
        ("Refunded", "Refunded"),
        ("Cancelled", "Cancelled"),
        
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscription")
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default="Bronze")
    subscription_name =  models.CharField(max_length=200,blank=True,null=True)
    subscription_domain =  models.CharField(max_length=200,blank=True,null=True)
    subscription_price=  models.CharField(max_length=200,blank=True,null=True)
    status = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS, default="Pending")
    date = models.DateTimeField(auto_now_add=True)
    one_to_one_training = models.BooleanField(default=False)
    weeks_completed = models.PositiveIntegerField(default=0)  
    one_to_one_progress = models.PositiveIntegerField(default=0)
    interview_buddy_coins_remaining = models.PositiveIntegerField(default=0)
    interview_buddy_coins_used = models.PositiveIntegerField(default=0)
    interview_buddy_slots_remaining = models.PositiveIntegerField(default=0)
    special_customer = models.BooleanField(default=False)
    extra_features = models.BooleanField(default=False)

    


class SessionHistory(models.Model):
    STATUS_CHOICES = [
        ("Completed", "Completed"),
        ("Pending", "Pending"),
        ("Requested", "Requested"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    company_name = models.CharField(max_length=255)
    session_date = models.DateTimeField()
    completed_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    
    
# class Ticket(models.Model):
#     TICKET_STATUS_CHOICES = [
#         ('Open', 'Open'),
#         ('Closed', 'Closed'),
#         ('Pending', 'Pending'),
#         ('Resolved', 'Resolved'),
#     ]

#     ticket_id = models.CharField(max_length=20, unique=True)
#     subject = models.CharField(max_length=255)
#     message = models.TextField()
#     related_OrderId = models.ForeignKey( UserSubscription,on_delete=models.SET_NULL,null=True,blank=True,related_name="tickets")
#     status = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, default='Open')
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')

#     def __str__(self):
#         return f"{self.ticket_id} - {self.subject}"
    


# class TicketResponse(models.Model):
    
#     ticket = models.ForeignKey('Ticket',on_delete=models.CASCADE,related_name='responses')
#     by = models.CharField(max_length=255) 
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)   





class Ticket(models.Model):
    TICKET_STATUS_CHOICES = [
        ('New', 'New'),
         ('Open', 'Open'),
         ('Awaiting', 'Awaiting'),
         ('Resolved', 'Resolved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    category = models.CharField(max_length=100,default ="candidate")
    subject = models.CharField(max_length=255)
    ticketID = models.CharField(max_length=255,default= "")
    status = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, default="Open")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.ticketID} - {self.subject}"


class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Message by {self.sender.username} on Ticket {self.ticket.id}"
 

class Service(models.Model):
    SERVICE_TYPES = [
        ('core', 'core'),
        ('alacarte', 'alacarte'),
    ]

    type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    features = models.TextField(blank=True, null=True, help_text="Comma separated list of features")
    applicable_domains = models.TextField(blank=True, null=True, help_text="Comma separated list of domains")

    def __str__(self):
        return f"{self.id} - {self.name}"
    


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ("fixed", "fixed"),
        ("percentage", "percentage"),
    ]

    couponCode = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    discountType = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discountValue = models.DecimalField(max_digits=10, decimal_places=2)

    minOrderValue = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    maxDiscountValue = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    startAt = models.DateTimeField()
    endAt = models.DateTimeField()

    isActive = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)

    usageLimit = models.IntegerField(blank=True, null=True)
    usedCount = models.IntegerField(default=0)

    isFeatured = models.BooleanField(default=False)

    displayPages = models.CharField(max_length=255,blank=True, null=True,help_text="Comma separated list of pages")

    productId = models.IntegerField(blank=True, null=True)

    createdBy = models.ForeignKey(User, related_name="coupon_created", on_delete=models.SET_NULL, null=True, blank=True)
    updatedBy = models.ForeignKey(User, related_name="coupon_updated", on_delete=models.SET_NULL, null=True, blank=True)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.couponCode} - {self.title}"
    
    def get_display_pages_list(self):
        return self.displayPages.split(',') if self.displayPages else []
    
    
    
    

    
    