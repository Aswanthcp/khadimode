from django.contrib import admin
from .models import Product, Variation, ProductGallery, Color, Size


class ProductGallaryInline(admin.TabularInline):
    model = ProductGallery
    extra = 4


class ProductVaritionInline(admin.TabularInline):
    model = Variation
    extra = 6
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name', 'price', 'stock',
                    'is_available', 'modified_date')
    inlines = [ProductGallaryInline, ProductVaritionInline]


class Variationadmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category',
                    'variation_value', 'is_active')
    list_editable = ('is_active',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, Variationadmin)
admin.site.register(ProductGallery)
admin.site.register(Size)
admin.site.register(Color)
