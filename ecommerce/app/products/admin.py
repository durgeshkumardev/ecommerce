from django.contrib import admin

# Register your models here.

from .models import Role, User, Category, Product

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'created_at')
    search_fields = ('role_name',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'mobile_no', 'created_at')
    search_fields = ('username', 'email')
    list_filter = ('role',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'description')
    search_fields = ('category_name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price', 'stock_quantity')
    search_fields = ('product_name', 'category')
    list_filter = ('category',)