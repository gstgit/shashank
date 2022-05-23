
from rest_framework import serializers
from . models import *

class contactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model=contactUs
        fields="__all__" 

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__" 

class productSerializer(serializers.ModelSerializer):
    class Meta:
        model=product
        fields="__all__" 

class frameSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model=frameSize
        fields="__all__"  

class frameColorSerializer(serializers.ModelSerializer):
    class Meta:
        model=frameSize
        fields="__all__"  

class printingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=printingType
        fields="__all__"  

class testimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model=testimonial
        fields="__all__"    

class orderResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=orderResponse
        fields="__all__"  
      
class pickupresponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=pickupresponse
        fields="__all__"  

class awbresponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=awbresponse
        fields="__all__"  

class returnOrderResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=returnOrderResponse
        fields="__all__"  

class giftWrapSerializer(serializers.ModelSerializer):
    class Meta:
        model=giftWrap
        fields="__all__"  

class hubAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=hubAddress
        fields="__all__"  

class trackOrderResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=trackOrderResponse
        fields="__all__"  
class productDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=productDetails
        fields="__all__"  
class paymentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=paymentResponse
        fields="__all__"  


        
