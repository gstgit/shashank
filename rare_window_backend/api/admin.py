from django.contrib import admin
from . models import *
from django.utils.html import format_html
from . import views
# Register your models here.

admin.site.site_header = "The Rare Window  Admin"
admin.site.site_title = "The Rare Window Admin Portal"
admin.site.index_title = "Welcome to The Rare Window admin Portal"


class contactUsAdmin(admin.ModelAdmin):
    list_display = ("contact_us_id", "name", "email", "phone_no","message")
admin.site.register(contactUs, contactUsAdmin)


class awbresponseAdmin(admin.ModelAdmin):
    list_display = ("awb_assign_status", "data")
admin.site.register(awbresponse,awbresponseAdmin)


class orderResponseAdmin(admin.ModelAdmin):
    list_display = ("order_id","shipment_id","status") 
admin.site.register(orderResponse, orderResponseAdmin)


class hubAddressAdmin(admin.ModelAdmin):
    list_display = ("hub_id","customer_name","last_name","address","address_2","city","country","pincode","state","email","isd_code","phone") 
admin.site.register(hubAddress, hubAddressAdmin)
class testimonialAdmin(admin.ModelAdmin):
    list_display = ("name",  "Message", "Rating")
admin.site.register(testimonial, testimonialAdmin)


class orderAdmin(admin.ModelAdmin):
    list_display = ("uuid", "email", "discount_code", "total_amount","quantity","payment_status","order_status","tracking_id","current_status_colored")
    def current_status_colored(self, obj):
        colors = {
            'un attended': 'orange',
            'printed': 'yellow',
            'shipped': 'green',
                }
        return format_html(
            '<b style="color:{};">{}</b>',
            colors[obj.current_status],
            obj.current_status,
        )
    actions = [views.make_printed,views.make_shipped]

    current_status_colored.short_description = "current_status"
admin.site.register(Order, orderAdmin)



class productAdmin(admin.ModelAdmin):
    list_display = ("Product_id","product_code", "product_name","in_stock","status_colored")
    def status_colored(self, obj):
        colors = {
            'single level': 'orange',
            'double level': 'yellow',
            'triple level': 'green',
        }
        return format_html(
            '<b style="color:{};">{}</b>',
            colors[obj.availability],
            obj.availability,
        )
    
    status_colored.short_description = "Availability"    
admin.site.register(product, productAdmin)


class frameSizeAdmin(admin.ModelAdmin):
    list_display = ("frame_size_id","frame_size","product_id", "price", "availability")
admin.site.register(frameSize, frameSizeAdmin)


class printingTypeAdmin(admin.ModelAdmin):
    list_display = ("printing_type_id","printing_type","product_id", "price", "availability")
admin.site.register(printingType, printingTypeAdmin)
class giftWrapAdmin(admin.ModelAdmin):
    list_display = ("giftwrap_id","price")
admin.site.register(giftWrap, giftWrapAdmin)
class returnOrderResponseAdmin(admin.ModelAdmin):
    list_display = ("order_id", "shipment_id", "status","status_code")
admin.site.register(returnOrderResponse, returnOrderResponseAdmin)
class trackOrderResponseAdmin(admin.ModelAdmin):
    list_display = ("trackOrder_id", "trackOrder_status")
admin.site.register(trackOrderResponse, trackOrderResponseAdmin)
class productDetailsAdmin(admin.ModelAdmin):
    list_display = ("product_id", "frame_size","length","breadth","height","weight")
admin.site.register(productDetails, productDetailsAdmin)
class paymentResponseAdmin(admin.ModelAdmin):
    list_display = ("paymentresponse_id", "data")
admin.site.register(paymentResponse, paymentResponseAdmin)