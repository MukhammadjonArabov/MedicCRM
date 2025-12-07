from django.contrib import admin
from apps.payment.models import Category, Service, Payments, PaymentItems

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'service_count')
    search_fields = ('name',)

    def service_count(self, obj):
        return obj.service_category.count()
    service_count.short_description = "Service"

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category__name', 'price', 'created_at')
    search_fields = ('name',)
    list_filter = ('category__name',)

class PaymentItemsInline(admin.TabularInline):
    model = PaymentItems
    extra = 1
    autocomplete_fields = ('service',)

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ("id", "payment_method", "amount_total", "patient", "created_by", "created_at")
    list_filter = ("payment_method", "created_at")
    search_fields = ("patient__full_name", "created_by__full_name")

    autocomplete_fields = ("patient", "created_by")
    inlines = [PaymentItemsInline]
