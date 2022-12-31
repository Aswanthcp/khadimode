from django.contrib import admin

from .models import Order, OrderItems, ProfileAddress


class OrderProductInline(admin.TabularInline):
    model = OrderItems
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'email',
                    'city', 'total_price', 'payment_mode', 'status']
    list_filter = ['status']
    search_fields = ['order_number', 'first_name', 'phone', 'email']
    list_per_page = 20


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems)
admin.site.register(ProfileAddress)

