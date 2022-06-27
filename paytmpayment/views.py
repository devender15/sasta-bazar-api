import environ
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions

from .models import Order
from .serializers import OrderSerializer
from . import Checksum

# Create your views here.

env = environ.Env()

# reading .env file
environ.Env.read_env()


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def start_payment(request):

    amount = request.data['amount']
    name = request.data['name']
    email = request.data['email']

    # we are saving an order instance (keeping isPaid=False)
    order = Order.objects.create(product_name=name, order_amount=amount, user_email=email, )

    serializer = OrderSerializer(order)

    param_dict = {
        'MID': env('MERCHANTID'),
        'ORDER_ID': str(order.id),
        'TXN_AMOUNT': str(amount),
        'CUST_ID': email,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'http://localhost:8000/payment/handlepayment/',
        # this is the url of handlepayment function, paytm will send a POST request to the fuction associated with this CALLBACK_URL
    }

    # create new checksum (unique hashed string) using our merchant key with every paytm payment
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, env('MERCHANTKEY'))

    return Response({'param_dict': param_dict})


@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def handlepayment(request):

    checksum = ""

    # the request.POST is coming from Paytm
    form = request.POST


    response_dict = {}
    order = None # initialize the order variable with None

    for i in form.keys():
        response_dict[i] = form[i]

        if(i == 'CHECKSUMHASH'):
            # 'CHECKSUMHASH' is coming from paytm and we will assign it to checksum variable to verify our paymant
            checksum = form[i]
            
        if(i == 'ORDERID'):
            # we will get an order with id==ORDERID to turn isPaid=True when payment is successful
            order = Order.objects.get(id=form[i])
    

    # we will verify the payment using our merchant key and the checksum that we are getting from Paytm request.POST
    verify = Checksum.verify_checksum(response_dict, env('MERCHANTKEY'), checksum)

    if(verify):
        if(response_dict['RESPCODE'] == '01'):
            # if the response code is 01 that means our transaction is successfull

            order.isPaid = True
            order.save()
            print(response_dict)
            return render(request, 'paytm/paymentstatus.html', {'response': response_dict})
        
        else:
            print('Order was not successfull because ' + response_dict['RESPMSG'])
            return render(request, 'paytm/paymentstatus.html', {'response': response_dict})