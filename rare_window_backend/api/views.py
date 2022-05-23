import string
from django.contrib import admin
from django.shortcuts import render
from pymysql import NULL
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
# Create your views here
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import requests
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

# To genrate shiprocket token 
def genratetoken():
    headers = {'Content-type': 'application/json',}
    data = '{"email":"akshay@giskernel.com","password":"9404797779"}'
    response = requests.post('https://apiv2.shiprocket.in/v1/external/auth/login', headers=headers, data=data)
    responsedata=json.loads(response.text)
    token=responsedata["token"]
    return token
@admin.action(description='Mark selected orders as shipped')
def make_shipped(modeladmin, request, queryset):
    for obj in queryset:
        billing_email=obj.email
        itmname=obj.product["productName"]
        subject, from_email, to = 'Shipped', 'orders@therarewindow.com', billing_email
        text_content = 'This is an important message.'
        context={"product_name":itmname,}
        html_content =  render_to_string('ordershipped.html',context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content,"text/html")
        msg.send()
        queryset.update(current_status='shipped')

# Function to create order
@admin.action(description='Mark selected orders to printed')
def make_printed(modeladmin, request, queryset):
    for obj in queryset:
        token=genratetoken()
        headers = {'Content-type': 'application/json','Authorization': 'Bearer'+token} 
        uuid= obj.uuid
        billing_customer_name=obj.billing_address["firstName"]
        billing_last_name=obj.billing_address["lastName"]
        billing_address=obj.billing_address["address"]
        billing_city=obj.billing_address["city"]
        billing_pincode=obj.billing_address["pin"]
        billing_state=obj.billing_address["state"]
        billing_country=obj.country
        billing_phone=obj.billing_address["phone"]
        billing_email=obj.email
        shipping_customer_name=obj.shipping_address["firstName"]
        shipping_last_name=obj.shipping_address["lastName"]
        shipping_address=obj.shipping_address["address"]
        shipping_city=obj.shipping_address["city"]
        shipping_pincode=obj.shipping_address["pin"]
        shipping_state=obj.shipping_address["state"]
        shipping_country=obj.country
        shipping_phone=obj.shipping_address["phone"]
        shipping_email=obj.email
        item=obj.product
        itemtype=type(item)
        if itemtype == list:
            order_items=[]
            for items in item:
                itmname=items["productName"]
                sku=items["productName"]
                sku=items["productName"]
                units=obj.quantity
                selling_price=obj.total_amount
                newdata={"name":itmname,"sku":sku,"units":units,"selling_price":selling_price}
                order_items.append(newdata)
                prod=product.objects.get(product_name=itmname)
                prod1=productSerializer(prod).data
                prod_code=prod1["Product_id"]
                f_size=item["frameSize"]
                prod=frameSize.objects.get(frame_size=f_size)
                prod1=frameSizeSerializer(prod).data
                prod_frameSize=prod1["frame_size_id"]
                prod_details= productDetails.objects.get(product_id=prod_code,frame_size=prod_frameSize)
                product_data =productDetailsSerializer(prod_details).data

        else:
            order_items=[]
            itmname=item["productName"]
            sku=item["productName"]
            units=obj.quantity
            selling_price=obj.total_amount
            newdata={"name":itmname,"sku":sku,"units":units,"selling_price":selling_price}
            order_items.append(newdata)
            prod=product.objects.get(product_name=itmname)
            prod1=productSerializer(prod).data
            prod_code=prod1["Product_id"]
            f_size=item["frameSize"]
            prod=frameSize.objects.get(frame_size=f_size)
            prod1=frameSizeSerializer(prod).data
            prod_frameSize=prod1["frame_size_id"]
            prod_details= productDetails.objects.get(product_id=prod_code,frame_size=prod_frameSize)
            product_data =productDetailsSerializer(prod_details).data
        payment_method="Prepaid",
        sub_total=obj.total_amount,
        length= prod_details.length,
        breadth=product_data["breadth"],
        height=product_data["height"],
        weight=product_data["weight"]
     
        data={  
                "order_id": uuid,
                "order_date": "2022-04-24 11:11",
                "pickup_location": "Primary",
              
              
                "billing_customer_name":billing_customer_name,
                "billing_last_name": billing_last_name,
                "billing_address":billing_address,
                "billing_address_2":billing_address,
                "billing_city":billing_city,
                "billing_pincode": billing_pincode,
                "billing_state":billing_state,
                "billing_country":billing_country,
                
                "billing_phone": billing_phone,
                "shipping_is_billing": False,
                "shipping_customer_name":shipping_customer_name,
                "shipping_last_name":shipping_last_name,
                "shipping_address": shipping_address,
                "shipping_address_2": shipping_address,
                "shipping_city": shipping_city,
                "shipping_pincode":shipping_pincode,
                "shipping_country":shipping_country,
                "shipping_state":shipping_state,
                "shipping_email": shipping_email,
                "shipping_phone": shipping_phone,
                "order_items":order_items,
                "payment_method": "Prepaid",
                "sub_total":obj.total_amount,
                "length":prod_details.length,
                "breadth": product_data["breadth"],
                "height":product_data["height"],
                "weight":product_data["weight"]
                }
        print(data)        
        data=json.dumps(data)
        orderresponse = requests.post('https://apiv2.shiprocket.in/v1/external/orders/create/adhoc', headers=headers, data=data)
        responsedata=json.loads(orderresponse.text)
        data=responsedata
        ser = orderResponseSerializer(data=data)
        order_id = data["order_id"]
        if not orderResponse.objects.filter(order_id=order_id).exists():
            if ser.is_valid():
                ser.save()
        else:
            snippet = orderResponse.objects.get(order_id=order_id)
            ser = OrderSerializer(snippet,data=data,partial=True)
            if ser.is_valid():
                ser.save()     
            token=genratetoken()
            headers = {'Content-type': 'application/json','Authorization': 'Bearer'+token} 
            jsondata={
                         "shipment_id":responsedata['shipment_id'] 
                    } 
            jsondata=json.dumps(jsondata)
            awbresponse = requests.post('https://apiv2.shiprocket.in/v1/external/courier/assign/awb',headers=headers,data=jsondata)
            awbresponse1=json.loads(awbresponse.text)
            data=awbresponse1
            #todo : dummy data
            resdata={
  "awb_assign_status": 1,
  "response": {
    "data": {
      "courier_company_id": 10,
      "awb_code": "1091208940593",
      "cod": 0,
      "order_id": 181771297,
      "shipment_id": 181302597,
      "awb_code_status": 1,
      "assigned_date_time": {
        "date": "2022-02-03 11:18:37.397226",
        "timezone_type": 3,
        "timezone": "Asia/Kolkata"
      },
      "applied_weight": 1,
      "company_id": 25149,
      "courier_name": "Delhivery",
      "child_courier_name":0,
      "routing_code": "DEL/KIS",
      "rto_routing_code": "",
      "invoice_no": "test5769122383",
      "transporter_id": "06AAPCS9575E1ZR",
      "transporter_name": "Delhivery",
      "shipped_by": {
        "shipper_company_name": "New RtO",
        "shipper_address_1": "34- house",
        "shipper_address_2": "",
        "shipper_city": "South West Delhi",
        "shipper_state": "Delhi",
        "shipper_country": "India",
        "shipper_postcode": "110030",
        "shipper_first_mile_activated": 0,
        "shipper_phone": "7777777777",
        "lat": "28.517677",
        "long": "77.175261",
        "shipper_email": "new@rto.com",
        "rto_company_name": "New RtO",
        "rto_address_1": "34- house",
        "rto_address_2": "",
        "rto_city": "South West Delhi",
        "rto_state": "Delhi",
        "rto_country": "India",
        "rto_postcode": "110030",
        "rto_phone": "8888888888",
        "rto_email": "new@rto.com"
      }
    }
  }
}   
            awbdata=resdata["response"]
            resdata={
                "awb_assign_status":resdata["awb_assign_status"],
                "data":awbdata["data"]
            }
            ser = awbresponseSerializer(data=resdata)
            if ser.is_valid():
                ser.save()
            awbdatamail=awbdata["data"]
            awbcode=awbdatamail["awb_code"]
         
            token=genratetoken()
            headers = {'Content-type': 'application/json','Authorization': 'Bearer'+token} 
            jsondata={
                        "shipment_id":responsedata['shipment_id'] 
                    } 
            jsondata=json.dumps(jsondata)
            pickupresponse = requests.post('https://apiv2.shiprocket.in/v1/external/courier/generate/pickup',headers=headers,data=jsondata)
            pickupresponse1=json.loads(pickupresponse.text)
            data=pickupresponse1
           
            ser = pickupresponseSerializer(data=data)
            if ser.is_valid():
                ser.save()
              
            else:
                print("something went wrong")
            subject, from_email, to = 'your order has been printed' , 'orders@therarewindow.com', billing_email
            text_content = 'This is an important message.'
            context={"order_id": order_id,"awb":awbcode,"product_name":itmname,"quantity":units,"total_amount":selling_price}
            html_content =  render_to_string('orderprinted.html',context)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content,"text/html")
            msg.send()     
        if  responsedata["status_code"]==1:
             shipment_id=responsedata["shipment_id"]
             queryset.update(tracking_id=shipment_id)
    queryset.update(current_status='printed')
@require_POST
def webhook_endpoint(request):
    jsondata = request.body
    data = json.loads(jsondata)
    return HttpResponse(status=200)
def home(request) :
    return HttpResponse("The rare window")
  
class awbdata(APIView):     
    def post(self,request):
        data=request.data
        ser = awbresponseSerializer(data=data)
        if ser.is_valid():
            ser.save()
            resultdata={
                    "status": 200,
                    "messages": "contact created successfully"
                      }
            return Response (resultdata)
        resultdataerr={
                    "status": 201,
                    "messages":ser.errors,
                      }   
        return Response(resultdataerr)
#start contact us 
class ContactUsView(APIView):       
    def post(self,request):
        data=request.data
        ser = contactUsSerializer(data=data)
        if ser.is_valid():
            ser.save()
            resultdata={
                    "status": 200,
                    "messages": "contact created successfully"
                      }
            return Response (resultdata)
        resultdataerr={
                    "status": 201,
                    "messages":ser.errors,
                      }   
        return Response(resultdataerr)
#end of contactUS
#start of order views
#? start create order
class create_orderView(APIView):
      
    def post(self,request):
        
        data=request.data
        try:
            item=data["product"]
        except :
                data = {
                    "status": 201,
                    "messages": "product is required",
                        }
                return Response(data)
        try:
            billing_email=data["email"]
        except :
                data = {
                    "status": 201,
                    "messages": "email is required",
                        }
                return Response(data)                  
        
        
        itemtype=type(item)
        if itemtype == list:
            order_items=[]
            for items in item:
                itmname=items["productName"]
                sku=items["productName"]
                units=data["quantity"]
                selling_price=data["total_amount"]
                newdata={"name":itmname,"sku":sku,"units":units,"selling_price":selling_price}
                order_items.append(newdata)
        else:
            order_items=[]
            itmname=item["productName"]
            sku=item["productName"]
            units=data["quantity"]
            selling_price=data["total_amount"]
            newdata={"name":itmname,"sku":sku,"units":units,"selling_price":selling_price}
            order_items.append(newdata)
        ser = OrderSerializer(data=data)
        if ser.is_valid():
            ser.save()
            subject, from_email, to = 'Thank you for your order', 'orders@therarewindow.com', billing_email
            text_content = 'This is an important message.'
            context={"product_name":itmname,"quantity":units,"total_amount":selling_price}
            html_content =  render_to_string('ordeconfirm.html',context)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content,"text/html")
            msg.send() 

            data={
                    "status": 200,
                    "messages": "order created successfully",
                     "data":{"uuid": ser.data["uuid"]}
                      }
            return Response (data)
        errdata= {
                    "status": 201, 
                    "messages":ser.errors,
                      }
        return Response(errdata)
#? end of create order
#?start order detailes
class orderDetailsView(APIView):
    def post(self,request):
        data=request.data
        uuid  = data["uuid"]
        if not uuid:
            data = {
                    "status": 201,
                    "messages": "orderId is required",
                        }
            return Response(data)
        else:
            if not Order.objects.filter(uuid=uuid).exists():
                errdata= {
                        "status": 201,
                        "messages":'order dose not exist'
                        }
                return Response(errdata)
            course = Order.objects.get(uuid=uuid)
            ser = OrderSerializer(course)
            data={
                        "status": 200,
                        "messages": "order updated successfully",
                        "data":ser.data
                    
                        }
            return Response (data)
#?end of order detailes
# ?start of update order  
class updateOrderView(APIView):
    def post(self,request):
        data=request.data
        try:
            uuid  = data["uuid"]
        except :
                data = {
                    "status": 201,
                    "messages": "uuid is required",
                        }
                return Response(data)     
        try:           
            payment_status  = data["payment_status"]
        except :
                data = {
                    "status": 201,
                    "messages": "payment_status is required",
                        }
                return Response(data)  

        try:
            order_status = data["order_status"]
        except :
            data = {
                    "status": 201,
                    "messages": "order_status is required",
                        }
            return Response(data)  

        if not uuid:
            data = {
                    "status": 201,
                    "messages": "orderId is required",
                        }
            return Response(data)
        elif not payment_status:
            data = {
                    "status": 201,
                    "messages": "payment status is required",
                        }
            return Response(data)
        elif not order_status:
            data = {
                    "status": 201,
                    "messages": "order status is required",
                        }
            return Response(data)
        else:
            if not Order.objects.filter(uuid=uuid).exists():
                errdata= {
                        "status": 201,
                        "messages":'order dose not exist'
                        }
                return Response(errdata)
            course = Order.objects.get(uuid=uuid)
            ser = OrderSerializer(course,data=data,partial=True)
            if ser.is_valid(raise_exception=True):
                ser.save()
                data={
                        "status": 200,
                        "messages": "order updated successfully",
                    
                        }
                return Response (data)
            else:
                errdata= {
                        "status": 201,
                        "messages":ser.errors,
                        }
                return Response(errdata)         
#?end of update order
#end of order views 
#start of product views
#?start get product
class getProductView(APIView):
    def get(self,request,id=None):
        if id:
            if not product.objects.filter(pk=id).exists():
                return Response ('object dose not exists')
            else:
                snippet = product.objects.get(pk=id)
                data = [productSerializer(snippet).data]
                return Response(data)
        else:
            if not  product.objects.exists():
                return Response('Object dose not exist')
            values= product.objects.all()
            context=[]
            for obj in values:
                newdata = productSerializer(obj).data
                context.append(newdata)
            return Response(context)     
    def post(self,request):
        data=request.data
        Id  = data["Product_id"]
        if id:
            if not product.objects.filter(Product_id=id).exists():
                return Response ('object dose not exists')
            else:
                snippet = product.objects.get(pk=id)
                data = [productSerializer(snippet).data]
                return Response(data)
        else:
            if not  product.objects.exists():
                return Response('Object dose not exist')
            values= product.objects.all()
            context=[]
            for obj in values:
                newdata = productSerializer(obj).data
                context.append(newdata)
            return Response(context) 
#?end of get product
#?start create product
class createProduct(APIView):
    def post(self,request):
        data=request.data
        ser = productSerializer(data=data)
        if ser.is_valid():
            ser.save()
            data={
                    "status": 200,
                    "messages": "order created successfully",
                      }
            return Response (data)
        errdata= {
                    "status": 201,
                    "messages":ser.errors,
                      }
        return Response(errdata)
#?end of create product
# end of product views
# start instock views                     
class InstockView(APIView):   
     def post(self,request):
        data=request.data       
        if not data:
            data = {
                    "status": 201,
                    "messages": "Productname is required",
                        }
            return Response(data)
        elif not data["product_name"]:
            data = {
                    "status": 201,
                    "messages": "Productname is required",
                        }
            return Response(data)
        else:
            product_name = data["product_name"]
            if not product.objects.filter(product_name=product_name).exists():
                    data = {
                    "status": 201,
                    "messages": "object dose not exists",
                        }
                    return Response (data)
            else:
                snippet = product.objects.get(product_name=product_name)
                data = productSerializer(snippet).data
                finaldata={"instock":data["in_stock"],"unavailablePrintingType": data["availability"]}
                resultdata= {
                            "status": 200,
                        
                            "data": finaldata
                            }
                return Response(resultdata)
#end instock
#start instock                
class calculatePriceView(APIView):
     def post(self,request):
        data=request.data  
        try:
            gproductName  = data["productName"]
        except:
            data = {
                "status": 201,
                "messages": "productName is required",
                    }
            return Response(data)        
        try:
            gframeSize = data["frameSize"]
        except:
            data = {
                "status": 201,
                "messages": "frameSize is required",
                    }
            return Response(data)       
        try:
            gprintingType = data["printingType"]
        except:
            data = {
                "status": 201,
                "messages": "printingType is required",
                    }
            return Response(data) 
        try:
            ggiftWrap = data["giftWrap"]
        except:
            data = {
                "status": 201,
                "messages": "giftWrap is required",
                    }
            return Response(data)        

        if not gproductName:
            data = {
                    "status": 201,
                    "messages": "Productname is required",
                        }
            return Response(data)
        elif not frameSize:
            data = {
                    "status": 201,
                    "messages": "frameSize is required",
                        }
            return Response(data)
        elif not printingType:
            data = {
                    "status": 201,
                    "messages": "printingType is required",
                        }
            return Response(data)
        else:
            if isinstance(ggiftWrap, bool):
             print("Does string belongs to BOOLEAN: ",isinstance(ggiftWrap, bool))
            else:
               
                data = {
                    "status": 201,
                    "messages": "giftWrap is required",
                        }
                return Response(data)
            try:
                productsnippet = product.objects.get(product_name=gproductName)
            except:
                data = {
                    "status": 201,
                    "messages": "Frame size type Does not exists",
                        }
                return Response(data)    
            data = productSerializer(productsnippet).data
            productprice=data["price"]
            product_id=data["Product_id"]
            if not product_id:
                data = {
                    "status": 201,
                    "messages": "Product Does not exists ",
                        }
                return Response(data)
          
            
            try:
                frameSizesnippet = frameSize.objects.get(frame_size=gframeSize,product_id=product_id)
            except:
                data = {
                    "status": 201,
                    "messages": "Frame size type Does not exists",
                        }
                return Response(data)            
            data =frameSizeSerializer(frameSizesnippet).data
            frameSizeprice=data["price"]
            if not frameSizeprice:
                data = {
                    "status": 201,
                    "messages": "Frame size Does not exists ",
                        }
                return Response(data)
            
          
            try:
                printingTypesnippet = printingType.objects.get(printing_type=gprintingType)
            except:
                data = {
                    "status": 201,
                    "messages": "Printing type Does not exists ",
                        }
                return Response(data)           
            data =printingTypeSerializer(printingTypesnippet).data

            printingTypeprice=data["price"]


            if not ggiftWrap == True:
                total_price= (productprice + frameSizeprice + printingTypeprice )
            else:
                giftwrapsnippet = giftWrap.objects.get(giftwrap_id=1)
                data =giftWrapSerializer(giftwrapsnippet).data
                giftwrap_eprice=data["price"]
           
                total_price= (productprice + frameSizeprice + printingTypeprice + giftwrap_eprice)

            data = {
                    "status": 200,
                    "messages": "Total amount is calculated",
                    "data": {
                            "price":total_price
                            }
                        }
            return Response(data)
#end instock    
#start trackorder
class trackOrder(APIView): 
     def post(self,request):
        try:
            data=request.data
        except :
            data = {
                    "status": 201,
                    "messages": " required fields not provided",
                        }
            return Response(data)

        if not data:
            data = {
                    "status": 201,
                    "messages": "order id is required",
                        }
            return Response(data)
        elif not data["uuid"]:
            data = {
                    "status": 201,
                    "messages": "order id is required",
                        }
            return Response(data)

        else:
            uuid = data["uuid"]
            if not Order.objects.filter(uuid=uuid).exists():
                    data = {
                    "status": 201,
                    "messages": "object dose not exists",
                        }
                    return Response (data)
            else:
                snippet = Order.objects.get(uuid=uuid)
                data =OrderSerializer(snippet).data
                
                shipment_id=data["tracking_id"]
                headers = {'Content-type': 'application/json',}
                data = '{"email":"akshay@giskernel.com","password":"9404797779"}'
                response = requests.post('https://apiv2.shiprocket.in/v1/external/auth/login', headers=headers, data=data)
                responsedata=json.loads(response.text)
                token=responsedata["token"]
                headers = {'Content-type': 'application/json','Authorization': 'Bearer'+token} 
                orderresponse = requests.get('https://apiv2.shiprocket.in/v1/external/courier/track/shipment/'+shipment_id, headers=headers, data=data)
                responsedata=json.loads(orderresponse.text)
                responsedata={
                            "tracking_data": {
                            "track_status": 1,
                            "shipment_status": 42,
                            "shipment_track": [
                                {
                                "id": 185584215,
                                "awb_code": "1091188857722",
                                "courier_company_id": 10,
                                "shipment_id": 168347943,
                                "order_id": 168807908,
                                "pickup_date": NULL,
                                "delivered_date": NULL,
                                "weight": "0.10",
                                "packages": 1,
                                "current_status": "PICKED UP",
                                "delivered_to": "Mumbai",
                                "destination": "Mumbai",
                                "consignee_name": "Musarrat",
                                "origin": "PALWAL",
                                "courier_agent_details": NULL,
                                "edd": "2021-12-27 23:23:18"
                                }
                                ],
                            "shipment_track_activities": [
                                {
                                "date": "2021-12-23 14:23:18",
                                "status": "X-PPOM",
                                "activity": "In Transit - Shipment picked up",
                                "location": "Palwal_NewColony_D (Haryana)",
                                "sr-status": "42"
                                },
                                {
                                "date": "2021-12-23 14:19:37",
                                "status": "FMPUR-101",
                                "activity": "Manifested - Pickup scheduled",
                                "location": "Palwal_NewColony_D (Haryana)",
                                "sr-status": "NA"
                                },
                                {
                                "date": "2021-12-23 14:19:34",
                                "status": "X-UCI",
                                "activity": "Manifested - Consignment Manifested",
                                "location": "Palwal_NewColony_D (Haryana)",
                                "sr-status": "5"
                                }
                            ],
                            "track_url": "https://shiprocket.co//tracking/1091188857722",
                            "etd": "2021-12-28 10:19:35"
                            }
                        }
                responsedata=json.dumps(responsedata["tracking_data"])
                tracking_data={"trackOrder_status":responsedata}
                ser = trackOrderResponseSerializer(data=tracking_data)
                if ser.is_valid():
                    ser.save()
                 
                else:
                    pass
           
                resultdata= {
                            "status": 200,
                            "messages": "success",
                            "data": responsedata
                            }
                return Response(resultdata)
#end track order  
#!need to remove                
@csrf_exempt
def test(request):
   if request.method == 'POST':
      username= request.POST["user"]
      password = request.POST["pass"]
      dict = {
         'username': username,
         'password': password
      }
      return Response(dict) 
#start testimonial
#?start create testimonial
class createTestimonial(APIView):
    def post(self,request):
        data=request.data
        ser = testimonialSerializer(data=data)
        if ser.is_valid():
            ser.save()
            data={
                    "status": 200,
                    "messages": "order created successfully",
                      }
            return Response (data)
        errdata= {
                    "status": 201,
                    "messages":ser.errors,
                      }
        return Response(errdata)
#?end of create testimonial
#? start get testimonial        
class getTestimonial(APIView):
    def get(self,request):
        data=testimonial.objects.all()
        ser = testimonialSerializer(data, many=True)
        if not data:
            data={
                    "status": 201,
                    "messages": "no Testimonial found ",
                      }
            return Response (data)
        errdata= {
                    "status": 200,
                    "messages":"success",
                    "data":ser.data
                      }
        return Response(errdata)  
#?end of get testimonial
# end of testimonial views        
#start of cancel order
class cancelOrder(APIView): 
     def post(self,request):
        data=request.data        
        if not data:
            data = {
                    "status": 201,
                    "messages": "order id is required",
                        }
            return Response(data)
        elif not data["uuid"]:
            data = {
                    "status": 201,
                    "messages": "order id is required",
                        }
            return Response(data)

        else:
            uuid = data["uuid"]
            if not Order.objects.filter(uuid=uuid).exists():
                    data = {
                    "status": 201,
                    "messages": "object dose not exists",
                        }
                    return Response (data)

            else:
              
                snippet = Order.objects.get(uuid=uuid)
                data =OrderSerializer(snippet).data
                shipment_id=data["tracking_id"]
                snippet = orderResponse.objects.get(shipment_id=shipment_id)
                data =orderResponseSerializer(snippet).data
                ids=[]
                id=int(data["order_id"])
                ids.append(id)
                canceldata={ "ids": ids}
                canceldata=json.dumps(canceldata)
            
                token=genratetoken()
                headers = {'Content-type': 'application/json','Authorization': 'Bearer'+token} 
                cancelorderresponse = requests.post('https://apiv2.shiprocket.in/v1/external/orders/cancel', headers=headers, data=canceldata)
                cancelorderresponse=json.loads(cancelorderresponse.text)

                resultdata= {
                            "status": 200,
                            "messages": "success",
                            "data": cancelorderresponse
                            }
                return Response(resultdata)
# ens of cancel order 
#start return order
class returnOrder(APIView): 
     def post(self,request):
        data=request.data        
        if not data:
            data = {
                    "status": 201,
                    "messages": "order id is required",
                        }
            return Response(data)
        elif not data["uuid"]:
            data = {
                    "status": 201,
                    "messages": "order id is required",
                        }
            return Response(data)
        else:
            uuid = data["uuid"]
            if not Order.objects.filter(uuid=uuid).exists():
                    data = {
                    "status": 201,
                    "messages": "object dose not exists",
                        }
                    return Response (data)
            else:              
                snippet = Order.objects.get(uuid=uuid)
                orderdata =OrderSerializer(snippet).data
                shipment_id=orderdata["tracking_id"]
                snippet = orderResponse.objects.get(shipment_id=shipment_id)
                ordrtresponsedata =orderResponseSerializer(snippet).data
                hubsnippet = hubAddress.objects.get(hub_id=1)
                hubdata =hubAddressSerializer(hubsnippet).data
           
                shipping_address=orderdata["shipping_address"]
                order_id=ordrtresponsedata["order_id"]
                order_date="2021-12-30"
                pickup_customer_name=shipping_address["firstName"]
                pickup_last_name=shipping_address["lastName"]
                pickup_address=shipping_address["address"]
                pickup_address_2=shipping_address["address"]
                pickup_city=shipping_address["city"]
                pickup_state=shipping_address["state"]
                pickup_country=orderdata["country"] 
                pickup_pincode=shipping_address["pin"]
                pickup_email=orderdata["email"] 
                pickup_phone=shipping_address["phone"]
                pickup_isd_code="91"
                shipping_customer_name=hubdata["customer_name"]
                shipping_last_name=hubdata["last_name"]
                sshipping_address=hubdata["address"]
                shipping_address_2=hubdata["address_2"]
                shipping_city=hubdata["city"]
                shipping_state=hubdata["state"]
                shipping_country=hubdata["country"]
                shipping_pincode=hubdata["pincode"]
                shipping_email=hubdata["email"]
                shipping_phone=hubdata["phone"]
                shipping_isd_code=hubdata["isd_code"]
                
                item=orderdata["product"]
                itemtype=type(item)
                if itemtype == list:
                    order_items=[]
                    for items in item:
                        name=items["productName"]
                        sku=items["productName"]
                        units=orderdata["quantity"]
                        selling_price=orderdata["total_amount"]
                        newdata={"name":name,"sku":sku,"units":units,"selling_price":selling_price}
                        order_items.append(newdata)
                        prod=product.objects.get(product_name=name)
                        prod1=productSerializer(prod).data
                        prod_code=prod1["Product_id"]
                        f_size=item["frameSize"]
                        prod=frameSize.objects.get(frame_size=f_size)
                        prod1=frameSizeSerializer(prod).data
                        prod_frameSize=prod1["frame_size_id"]
                        prod_details= productDetails.objects.get(product_id=prod_code,frame_size=prod_frameSize)
                        product_data =productDetailsSerializer(prod_details).data
                else:
                    order_items=[]
                    name=item["productName"]
                    sku=item["productName"]
                    units=orderdata["quantity"]
                    selling_price=orderdata["total_amount"]
                    newdata={"name":name,"sku":sku,"units":units,"selling_price":selling_price}
                    order_items.append(newdata)
                    prod=product.objects.get(product_name=name)
                    prod1=productSerializer(prod).data
                    prod_code=prod1["Product_id"]
                    f_size=item["frameSize"]
                    prod=frameSize.objects.get(frame_size=f_size)
                    prod1=frameSizeSerializer(prod).data
                    prod_frameSize=prod1["frame_size_id"]
                    prod_details= productDetails.objects.get(product_id=prod_code,frame_size=prod_frameSize)
                    product_data =productDetailsSerializer(prod_details).data
                sub_total= orderdata["total_amount"],
                length= product_data["length"],
                breadth=product_data["breadth"],
                height=product_data["height"],
                weight=product_data["weight"]
                      
            returndata={
                "order_id": order_id,
                "order_date": order_date,
                "pickup_customer_name": pickup_customer_name,
                "pickup_last_name": pickup_last_name,
                "company_name":"iorn pvt ltd",
                "pickup_address": pickup_address,
                "pickup_address_2":pickup_address_2,
                "pickup_city": pickup_city,
                "pickup_state": pickup_state,
                "pickup_country":pickup_country,
                "pickup_pincode": pickup_pincode,
                "pickup_email": pickup_email,
                "pickup_phone":pickup_phone,
                "pickup_isd_code": "91",
                "shipping_customer_name":shipping_customer_name,
                "shipping_last_name":shipping_last_name,
                "shipping_address":sshipping_address,
                "shipping_address_2": shipping_address_2,
                "shipping_city": shipping_city,
                "shipping_country": shipping_country,
                "shipping_pincode": shipping_pincode,
                "shipping_state": shipping_state,
                "shipping_email": shipping_email,
                "shipping_isd_code": "91",
                "shipping_phone": shipping_phone,
                "order_items":order_items,
                "payment_method": "PREPAID",
                "total_discount": "0",
                "sub_total":orderdata["total_amount"],
                "length":prod_details.length,
                "breadth": product_data["breadth"],
                "height":product_data["height"],
                "weight":product_data["weight"]
                    }
            returndata=json.dumps(returndata)
            token=genratetoken()
            headers = {'Content-type': 'application/json','Authorization': 'Bearer'+token} 
            cancelorderresponse = requests.post('https://apiv2.shiprocket.in/v1/external/orders/create/return', headers=headers, data=returndata)
            returndata=json.loads(cancelorderresponse.text)

            returndata={
                        "order_id": 170872392,
                        "shipment_id": 170411259,
                        "status": "RETURN PENDING",
                        "status_code": 21,
                        "company_name": "shiprocket"
                        }
            ser = returnOrderResponseSerializer(data=returndata)
            if ser.is_valid():
                ser.save()
                print("saved")
            else:
                print(ser.errors)    
            resultdata= {
                        "status": 200,
                        "messages": "success",
                        "data": cancelorderresponse
                        }
            return Response(resultdata)
# end of return order

#start test payment

class paymentlink(APIView):
    def post(self,request):
        url = "https://sandbox.cashfree.com/pg/orders"
        payload = {
            "order_id": request.data.get("order_id"),
            "order_amount": request.data.get("order_amount"),
            "order_currency": "INR",
            "customer_details": {
                "customer_id": request.data.get("customer_phone"),
                "customer_email": request.data.get("customer_email"),
                "customer_phone": request.data.get("customer_phone"),
            },
            "order_meta": {
                "return_url": "https://therarewindow.com/confirm?order_id={order_id}&order_token={order_token}",
                 "notify_url":"http://127.0.0.1:8000/webhook_endpoint/"
            }
        }
        headers = {
            "Accept": "application/json",
            "x-api-version": "2022-01-01",
            "x-client-id": "1524403344731507fa025f45b0044251",
            "x-client-secret": "baa03fdce4e4a520a2d9b9d9faca1d99dfa6c139",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        res=response.json()
        data={"data":res}
        ser = paymentResponseSerializer(data=data)
        if ser.is_valid():
            ser.save()
            print("saved")
        else:
            print(ser.errors)    
        return JsonResponse(response.json(), safe=False, status=status.HTTP_200_OK)
#end of test payment

#start payment gateway
@csrf_exempt
def startPayment(request):
    if request.method == 'POST':
        url = "https://sandbox.cashfree.com/pg/orders"
        payload = {
            "order_id": request.POST.get("order_id"),
            "order_amount": request.POST.get("order_amount"),
            "order_currency": "INR",
            "customer_details": {
                "customer_id": request.POST.get("customer_phone"),
                "customer_email": request.POST.get("customer_email"),
                "customer_phone": request.POST.get("customer_phone"),
            },
            "order_meta": {
                "return_url": "https://therarewindow.com/confirm?order_id={order_id}&order_token={order_token}",
            }
        }
        headers = {
            "Accept": "application/json",
            "x-api-version": "2022-01-01",
            "x-client-id": "1524403344731507fa025f45b0044251",
            "x-client-secret": "baa03fdce4e4a520a2d9b9d9faca1d99dfa6c139",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        return JsonResponse(response.json(), safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message': 'wrong method'}, status=status.HTTP_400_BAD_REQUEST)
#end payment gateway