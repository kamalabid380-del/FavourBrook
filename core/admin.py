from django.contrib import admin

from .models import (
    AboutBand, Category, ContactMessage, EditorialCard, FeatureBlock, HeroPanel,
    NewsletterSubscriber, Order, OrderItem, Page, Product, ProductRow,
    SiteSettings, UspIcon, WideHero,
)

admin.site.site_header = "Favourbrook — Administration"
admin.site.site_title = "Favourbrook Admin"
admin.site.index_title = "Store management"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroPanel)
class HeroPanelAdmin(admin.ModelAdmin):
    list_display = ["title", "kicker", "link", "order", "is_active"]
    list_editable = ["order", "is_active"]


@admin.register(ProductRow)
class ProductRowAdmin(admin.ModelAdmin):
    list_display = ["title", "collection", "limit", "order", "is_active"]
    list_editable = ["limit", "order", "is_active"]


@admin.register(EditorialCard)
class EditorialCardAdmin(admin.ModelAdmin):
    list_display = ["title", "group", "link", "order", "is_active"]
    list_editable = ["group", "order", "is_active"]
    list_filter = ["group"]


@admin.register(FeatureBlock)
class FeatureBlockAdmin(admin.ModelAdmin):
    list_display = ["title", "link", "image_right", "is_active"]
    list_editable = ["image_right", "is_active"]


@admin.register(WideHero)
class WideHeroAdmin(admin.ModelAdmin):
    list_display = ["title", "link", "is_active"]
    list_editable = ["is_active"]


@admin.register(AboutBand)
class AboutBandAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(UspIcon)
class UspIconAdmin(admin.ModelAdmin):
    list_display = ["title", "icon", "order"]
    list_editable = ["icon", "order"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "show_in_nav", "nav_order"]
    list_editable = ["show_in_nav", "nav_order"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "compare_price", "available", "is_featured", "order"]
    list_editable = ["price", "compare_price", "available", "is_featured", "order"]
    list_filter = ["available", "is_featured", "collections"]
    search_fields = ["name", "slug"]
    filter_horizontal = ["collections"]
    prepopulated_fields = {"slug": ("name",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["subtotal"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "phone", "city", "total", "status", "created_at"]
    list_editable = ["status"]
    list_filter = ["status", "city"]
    search_fields = ["name", "phone", "email"]
    inlines = [OrderItemInline]
    readonly_fields = ["total", "created_at"]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "handled", "created_at"]
    list_editable = ["handled"]
    list_filter = ["handled"]


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "created_at"]
    search_fields = ["email"]


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "updated_at"]
    prepopulated_fields = {"slug": ("title",)}