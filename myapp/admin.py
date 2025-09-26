from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "fullname", "role", "is_active", "is_staff", "joined_date", "paid_customer")
    list_filter = ("role", "is_active", "is_staff", "paid_customer")
    search_fields = ("email", "fullname", "mobile_number")


@admin.register(UserUploadedFiles)
class UserUploadedFilesAdmin(admin.ModelAdmin):
    list_display = ("user", "file")
    search_fields = ("user__email",)


@admin.register(CandidateAssignment)
class CandidateAssignmentAdmin(admin.ModelAdmin):
    list_display = ("candidate", "trainer", "buddy", "assigned_at")
    search_fields = ("candidate__fullname", "trainer__fullname", "buddy__fullname")


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subscription_name",
        "one_to_one_training",
        "interview_buddy_coins_remaining",
        "interview_buddy_coins_used",
        "special_customer",
        "extra_features",
    )
    list_filter = ("subscription_name", "special_customer", "extra_features")
    search_fields = ("user__email",)


@admin.register(SessionHistory)
class SessionHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "session_date", "completed_status")
    list_filter = ("completed_status", "session_date")
    search_fields = ("user__email", "company_name")
    
    
@admin.register(WebsiteStatus)    
class WebsiteStatusAdmin(admin.ModelAdmin):
    list_display = ("website_status","is_active", "updated_at")
    readonly_fields = ("website_status",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'price', 'original_price')
    search_fields = ('id', 'name')
    list_filter = ("type", "name")



@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("user","ticketID","category","subject","status","created_at")
    search_fields = ("ticketID",)

   

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("ticket", "sender", "text", "created_at")

     