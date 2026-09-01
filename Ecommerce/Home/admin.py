from django.contrib import admin
from .models import Product, Order, OrderItem, Cart, CartItem, Review, Oderinfo


# Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'is_featured', 'created_at')
    list_filter = ('category', 'is_active', 'is_featured', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_active', 'is_featured')

    fieldsets = (
        ('Product Information', {'fields': ('name', 'description', 'category', 'price')}),
        ('Media', {'fields': ('image',)}),
        ('Inventory', {'fields': ('stock',)}),
        ('Status', {'fields': ('is_active', 'is_featured')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


# Order Item Inline
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('get_cost',)
    fields = ('product', 'quantity', 'price', 'get_cost')

    def get_cost(self, obj):
        return f"৳{obj.get_cost()}"
    get_cost.short_description = "Total Cost"


# Order Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'status', 'total_price', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('name', 'email', 'phone', 'address', 'bkash_number')
    readonly_fields = ('created_at', 'updated_at', 'get_total')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Customer Information', {'fields': ('user', 'name', 'email', 'phone')}),
        ('Address', {'fields': ('address', 'city', 'postal_code')}),
        ('Payment Information', {'fields': ('payment_method', 'bkash_number')}),
        ('Order Details', {'fields': ('status', 'total_price', 'get_total')}),
        ('Additional Info', {'fields': ('notes',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def get_total(self, obj):
        return f"৳{obj.get_total()}"
    get_total.short_description = "Order Total"


# Cart Admin
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('get_cost',)
    fields = ('product', 'quantity', 'get_cost', 'added_at')

    def get_cost(self, obj):
        return f"৳{obj.get_cost()}"
    get_cost.short_description = "Total"


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_item_count', 'get_total', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'session_id')
    readonly_fields = ('created_at', 'updated_at', 'get_total', 'get_item_count')
    inlines = [CartItemInline]

    def get_item_count(self, obj):
        return obj.get_item_count()
    get_item_count.short_description = "Items"

    def get_total(self, obj):
        return f"৳{obj.get_total()}"
    get_total.short_description = "Cart Total"


# Review Admin
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'title')
    readonly_fields = ('created_at',)


# Legacy Order Info Admin (deprecated)
class OrderinfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'payment', 'address', 'quantity')


# Register all models
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Oderinfo, OrderinfoAdmin)