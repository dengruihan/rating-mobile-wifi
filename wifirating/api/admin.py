from django.contrib import admin
from django.utils import timezone

from .models import User, WifiModel, DataPlan, Review, Favorite


class DataPlanInline(admin.TabularInline):
    model = DataPlan
    extra = 0


@admin.action(description="通过审核（设为已通过）")
def approve_wifi_models(modeladmin, request, queryset):
    queryset.update(
        approval_status=WifiModel.APPROVAL_APPROVED,
        approved_by=request.user,
        approved_at=timezone.now(),
        rejection_reason=None,
    )


@admin.action(description="驳回审核（设为已驳回）")
def reject_wifi_models(modeladmin, request, queryset):
    queryset.update(
        approval_status=WifiModel.APPROVAL_REJECTED,
        approved_by=request.user,
        approved_at=timezone.now(),
        rejection_reason="管理员驳回",
    )


@admin.register(WifiModel)
class WifiModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "approval_status",
        "submitted_by",
        "submitted_at",
        "approved_by",
        "approved_at",
    )
    list_filter = ("approval_status", "brand")
    search_fields = ("name", "brand", "model")
    ordering = ("-submitted_at", "-id")
    inlines = [DataPlanInline]
    actions = [approve_wifi_models, reject_wifi_models]


@admin.register(DataPlan)
class DataPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "wifi_model", "name", "price")
    search_fields = ("wifi_model__name", "name")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "wifi_model", "user", "rating", "is_anonymous", "date")
    list_filter = ("is_anonymous", "rating")
    search_fields = ("wifi_model__name", "user__username", "comment")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "wifi_model")
    search_fields = ("user__username", "wifi_model__name")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_superuser", "date_joined")
    search_fields = ("username", "email")
