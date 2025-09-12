from django.contrib import admin
from .models import User, UserUploadedFiles, CandidateAssignment, UserSubscription, SessionHistory


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
