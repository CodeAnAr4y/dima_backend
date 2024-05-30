from django.contrib import admin
from .models import PaymentsInfo, Role, Users, Product, PurchaseHistory, UsersPaymentInfo

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'fullname', 'company', 'email', 'phone', 'role', 'created')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'company', 'email')
    list_filter = ('company',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'vendor', 'cost', 'quantity', 'average_rating', 'number_of_ratings')
    list_display_links = ('id', 'product_name')
    search_fields = ('product_name', 'specification')
    list_filter = ('vendor', 'cost')

class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'product', 'created', 'paid')
    list_display_links = ('id', 'client')
    search_fields = ('client__username', 'product__product_name')
    list_filter = ('paid', 'created')

class PaymentsInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'owner_name')
    list_display_links = ('id', 'card', 'owner_name')
    search_fields = ('id', 'card', 'owner_name')
    list_filter = ('card', 'owner_name')

class UsersPaymentInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'card', 'created')
    list_display_links = ('id', 'client')
    search_fields = ('client', 'card')
    list_filter = ('client', 'card')



admin.site.register(Role, RoleAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(PurchaseHistory, PurchaseHistoryAdmin)
admin.site.register(PaymentsInfo, PaymentsInfoAdmin)
admin.site.register(UsersPaymentInfo, UsersPaymentInfoAdmin)

