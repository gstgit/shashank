from pyexpat import model
from django.db import models
import uuid
from json import JSONEncoder
from uuid import UUID

JSONEncoder_olddefault = JSONEncoder.default
def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)
JSONEncoder.default = JSONEncoder_newdefault
# Create your models here.
class contactUs(models.Model):
    contact_us_id=models.AutoField(primary_key=True)
    name= models.CharField (max_length=500)
    email= models.EmailField()
    phone_no= models.CharField (max_length=500)
    message= models.CharField (max_length=500)

CURRENT_STATUS= (
        ("un attended", 'un attended'),
        ("printed", 'printed'),
        ("shipped", 'shipped')
        ) 
#todo add width height etc
class Order(models.Model):
    email=models.EmailField()
    uuid =models.UUIDField(
         default = uuid.uuid4,
         editable = False)
    send_news_and_Offers=models.BooleanField()
    discount_code=models.CharField (max_length=500,blank=True)
    gifting_msg=models.CharField (max_length=500,blank=True)
    total_amount=models.IntegerField()
    quantity=models.IntegerField()
    payment_status=models.CharField (max_length=500,default="ACTIVE")
    order_status=models.CharField (max_length=500,default="pending")
    tracking_id=models.CharField (max_length=500,blank=True)
    product=models.JSONField()
    shipping_address=models.JSONField()
    billing_address=models.JSONField()
    current_status=models.CharField (max_length=500, choices=CURRENT_STATUS,default="un attended")    
    country=models.CharField (max_length=500,default="INDIA")

AVAILABILITY= (
    ("single level", 'single level'),
    ("double level", 'double level'),
    ("Digital Copy", 'Digital Copy')
    )    
class product(models.Model):

    Product_id=models.AutoField(primary_key=True)
    product_code=models.CharField(max_length=500)
    product_name=models.CharField (max_length=500,unique=True)
    in_stock=models.BooleanField()
    availability=models.CharField (max_length = 100, choices=AVAILABILITY,default="single level")
    price=models.FloatField()

    def __str__(self):
        return self.product_code

class hubAddress(models.Model):
    hub_id=models.AutoField(primary_key=True)
    customer_name=models.CharField(max_length=500)
    last_name=models.CharField(max_length=500)
    address=models.CharField(max_length=500)
    address_2=models.CharField(max_length=500)
    city=models.CharField(max_length=500)
    country=models.CharField(max_length=500)
    pincode=models.CharField(max_length=500)
    state=models.CharField(max_length=500)
    email=models.CharField(max_length=500)
    isd_code=models.CharField(max_length=500)
    phone=models.CharField(max_length=500)

class frameSize(models.Model):
    frame_size_id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(product,on_delete=models.CASCADE)
    frame_size=models.CharField (max_length=500)
    availability=models.BooleanField()
    price=models.IntegerField()
    def __str__(self):
        return self.frame_size

PRINTINGTYPEOPTION= (
    ("Single Level", 'Single Level'),
    ("Double Level", 'Double Level'),
    ("Digital Copy", 'Digital Copy')
    )  
class printingType(models.Model):
    printing_type_id=models.AutoField(primary_key=True,unique=True)
    product_id=models.ForeignKey(product,on_delete=models.CASCADE)
    printing_type=models.CharField (max_length = 100, choices=PRINTINGTYPEOPTION)
    availability=models.BooleanField()
    price=models.IntegerField()
  
class giftWrap(models.Model):
    giftwrap_id=models.AutoField(primary_key=True)
    price=models.IntegerField()

 
class testimonial(models.Model):
    name=models.CharField (max_length=500)
    productMedia=models.FileField()
    Message=models.CharField (max_length=500)
    Rating=models.CharField (max_length=500)
    user_image=models.ImageField()
    def __str__(self):
        return self.name

#Table to store create order response
class orderResponse(models.Model):
    order_id=models.CharField (max_length=500)
    shipment_id=models.CharField (max_length=500)
    status=models.CharField (max_length=500,blank=True)
    status_code=models.CharField (max_length=500,blank=True)
    onboarding_completed_now=models.CharField (max_length=500,blank=True)
    awb_code=models.CharField (max_length=500,blank=True)
    courier_company_id=models.CharField (max_length=500,blank=True)
    courier_name=models.CharField (max_length=500,blank=True)

#To store response of  create awb
class awbresponse(models.Model):
    awb_assign_status=models.CharField (max_length=500)
    data=models.JSONField()

class pickupresponse(models.Model):
    pickup_status=models.CharField (max_length=500)
    pickup_scheduled_date=models.CharField (max_length=500)
    pickup_token_number=models.CharField (max_length=500)
    status=models.CharField (max_length=500)
    others=models.JSONField()
    pickup_generated_date=models.JSONField()
    data=models.CharField (max_length=500)
#to store response of Return Order   

class returndata(models.Model):
    order_id=models.CharField(max_length=500)
    order_date=models.CharField (max_length=500)
    channel_id=models.CharField (max_length=500)
    pickup_customer_name=models.CharField (max_length=500)
    pickup_last_name=models.CharField (max_length=500)
    company_name=models.CharField (max_length=500)
    pickup_address=models.CharField (max_length=500)
    pickup_address_2=models.CharField (max_length=500)
    pickup_city=models.CharField (max_length=500)
    pickup_state=models.CharField (max_length=500)
    pickup_country=models.CharField (max_length=500)
    pickup_pincode=models.CharField (max_length=500)
    pickup_email=models.CharField (max_length=500)
    pickup_phone=models.CharField (max_length=500)
    pickup_isd_code=models.CharField (max_length=500)
    shipping_customer_name=models.CharField (max_length=500)
    shipping_last_name=models.CharField (max_length=500)
    shipping_address=models.CharField (max_length=500)
    shipping_address_2=models.CharField (max_length=500)
    shipping_city=models.CharField (max_length=500)
    shipping_country=models.CharField (max_length=500)
    shipping_pincode=models.CharField (max_length=500)
    shipping_state=models.CharField (max_length=500)
    shipping_email=models.CharField (max_length=500)
    shipping_isd_code=models.IntegerField()
    shipping_phone=models.CharField (max_length=500)
    payment_method=models.CharField (max_length=500)
    total_discount=models.IntegerField ()
    sub_total=models.IntegerField ()
    length=models.IntegerField()
    breadth=models.IntegerField()
    height=models.IntegerField()
    weight=models.IntegerField ()
    order_items=models.JSONField()
class returnOrderResponse(models.Model):
    order_id=models.CharField(max_length=100)
    shipment_id=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    status_code=models.CharField(max_length=50)
    company_name=models.CharField(max_length=50)
class trackOrderResponse(models.Model):
    trackOrder_id=models.AutoField(primary_key=True)
    trackOrder_status=models.JSONField()


#start of product physical detailes

class productDetails(models.Model):
    product_id=models.ForeignKey(product,on_delete=models.CASCADE)
    frame_size=models.ForeignKey(frameSize,on_delete=models.CASCADE)
    length=models.IntegerField()
    breadth=models.IntegerField()
    height=models.IntegerField()
    weight=models.IntegerField()
    
#end of product

#start payment response

class paymentResponse(models.Model):
    paymentresponse_id=models.AutoField(primary_key=True)
    data=models.JSONField()