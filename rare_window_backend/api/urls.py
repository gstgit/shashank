
from django.urls import path,include
from . import views
urlpatterns = [
        path('', views.home),  
        path('test', views.test),  
        path('contactUs/', views.ContactUsView.as_view()),             #for contact us
        path('createOrder/', views.create_orderView.as_view()),        #to create order
        path('orderDetails/', views.orderDetailsView.as_view()),       #to get order details
        path('updateOrder/', views.updateOrderView.as_view()),         #to update order
        path('getProduct/', views.getProductView.as_view()),           #to get product
        path('createProduct/', views.createProduct.as_view()),         #to create product
        path('Instock/', views.InstockView.as_view()),                 #for instock
        path('calculatePrice/', views.calculatePriceView.as_view()),   #to calculate price
        path('trackOrder/', views.trackOrder.as_view()),               #to track order 
        path('createTestimonial/', views.createTestimonial.as_view()), #for create testimonial
        path('getTestimonial/', views.getTestimonial.as_view()),       #to get testimonial details
        path('webhook_endpoint/', views.webhook_endpoint),             #for webhook
        path('cancelOrder/', views.cancelOrder.as_view()),  #to cancel order
        path('returnOrder/', views.returnOrder.as_view()),  #for return order request
        path('paymentlink/', views.paymentlink.as_view()),  #for payment test
        path('startPayment/', views.startPayment), #for payment gateway

]