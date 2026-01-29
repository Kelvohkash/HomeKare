from django.contrib import admin
from .models import Service, HeroContent, Worker, WorkerDocument, Booking, Review, UserProfile, Category

class WorkerDocumentInline(admin.TabularInline):
    model = WorkerDocument
    extra = 1

@admin.register(HeroContent)
class HeroContentAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('title', 'description')

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'location', 'experience_level', 'internal_rating', 'is_active', 'date_joined')
    list_filter = ('experience_level', 'is_active', 'skills', 'location', 'date_joined')
    search_fields = ('full_name', 'phone_number', 'id_number', 'notes')
    filter_horizontal = ('skills',)
    inlines = [WorkerDocumentInline]
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'phone_number', 'email', 'id_number', 'id_scan', 'location')
        }),
        ('Professional Details', {
            'fields': ('experience_level', 'skills', 'is_active')
        }),
        ('Internal Metrics & Notes', {
            'fields': ('internal_rating', 'notes'),
            'description': 'These fields are for internal use only.'
        }),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'service', 'agreed_price', 'status', 'is_paid', 'assigned_worker', 'created_at')
    list_filter = ('status', 'is_paid', 'service', 'created_at')
    search_fields = ('customer_name', 'user__email', 'customer_phone', 'location')
    list_editable = ('status', 'assigned_worker', 'agreed_price')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('service', 'assigned_worker')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'worker', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'worker__full_name', 'user__email')
    readonly_fields = ('booking', 'worker', 'user', 'created_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'contact_preference')
    list_filter = ('contact_preference',)
    search_fields = ('user__email', 'phone_number')
    raw_id_fields = ('user',)
