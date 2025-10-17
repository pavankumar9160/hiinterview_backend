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



from django.contrib import admin
from .models import Coupon
from django import forms


class CouponAdminForm(forms.ModelForm):
    PAGE_CHOICES = [
        ('home', 'home'),
        ('slider', 'slider'),
        ('cart', 'cart'),
        ('checkout', 'checkout'),
        ('profile','profile'),
    ]

    displayPages = forms.MultipleChoiceField(
        choices=PAGE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Display Pages"
    )

    class Meta:
        model = Coupon
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.displayPages:
            self.initial['displayPages'] = self.instance.displayPages.split(',')

    def clean_displayPages(self):
        return ','.join(self.cleaned_data.get('displayPages', []))

class CouponAdmin(admin.ModelAdmin):
    form = CouponAdminForm
    list_display = ("couponCode", "title", "discountType", "discountValue", "isActive", "isFeatured", "priority", "startAt", "endAt")
    list_filter = ("isActive", "isFeatured", "discountType", "displayPages")
    search_fields = ("couponCode", "title", "description")
    ordering = ("priority", "-createdAt")

    filter_horizontal = ()
    fieldsets = (
        (None, {
            "fields": (
                "couponCode", "title", "description",
                "discountType", "discountValue", "minOrderValue", "maxDiscountValue",
                "startAt", "endAt", "isActive", "priority",
                "usageLimit", "usedCount", "isFeatured", "displayPages", "productId",
                "createdBy", "updatedBy", "isDeleted"
            )
        }),
    )
admin.site.register(Coupon, CouponAdmin)    

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Custom filter for user1
class User1NameFilter(admin.SimpleListFilter):
    title = _('User Name')
    parameter_name = 'user1_name'

    def lookups(self, request, model_admin):
        users = set(model_admin.model.objects.values_list('user1__fullname', 'user1__first_name'))
        lookup_list = []
        for fullname, first_name in users:
            name = fullname or first_name
            if name:
                lookup_list.append((name, name))
        return sorted(lookup_list)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                user1__fullname=self.value()
            ) | queryset.filter(
                user1__first_name=self.value()
            )
        return queryset


@admin.register(ChatRequest)
class ChatRequestAdmin(admin.ModelAdmin):
    list_display = ("user1", "user2", "created_at")
    list_filter = ("is_active", User1NameFilter)
    
    # Search by either fullname or first_name
    search_fields = (
        "user1__fullname",
        "user1__first_name",
        "user2__fullname",
        "user2__first_name",
        "user1__last_name",
        "user2__last_name",
    )


     
    
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("chatRequest", "sender", "text", "created_at")
     