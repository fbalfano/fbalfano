from django.contrib import admin

from .models import Lead, NewsletterSubscriber, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "order", "active", "updated_at")
    list_editable = ("order", "active")
    search_fields = ("title", "summary", "details")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "source", "status", "created_at")
    list_filter = ("status", "source", "created_at")
    search_fields = ("name", "email", "company", "message", "notes")
    list_editable = ("status",)
    readonly_fields = ("source", "created_at", "updated_at")
    date_hierarchy = "created_at"
    actions = ["mark_as_client", "mark_as_contacted"]

    fieldsets = (
        (None, {"fields": ("name", "email", "company", "phone", "message")}),
        ("Pipeline", {"fields": ("source", "status", "notes")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.action(description="Mark selected leads as CLIENT")
    def mark_as_client(self, request, queryset):
        updated = queryset.update(status=Lead.Status.CLIENT)
        self.message_user(request, f"{updated} lead(s) are now clients. 🤘")

    @admin.action(description="Mark selected leads as contacted")
    def mark_as_contacted(self, request, queryset):
        updated = queryset.update(status=Lead.Status.CONTACTED)
        self.message_user(request, f"{updated} lead(s) marked contacted.")


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "active", "created_at")
    list_filter = ("active",)
    search_fields = ("email",)
