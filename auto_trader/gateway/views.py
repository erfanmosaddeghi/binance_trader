from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from .models import User
from django.views import View
from .serializers import UserRegisterSerializer
from rest_framework.authtoken.models import Token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .utils import email_token
from .utils import emailVerifi
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, request
from binance.client import Client
from binance.exceptions import *
from binance.enums import *
from rest_framework.parsers import JSONParser

"""
Registration part That Contains email sending process and make Validation link for user
"""
@api_view(['POST',])
def register_view(request):
    if request.method =='POST':
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['responce'] = 'Done!!'
            data['Email'] = user.email
            data['UserName'] = user.username
            token = Token.objects.get(user = user).key
            data['Token'] = token
            status,msg = emailVerifi.send_mail(request) # Send Email to the user email for verified.
            if status == True:
                return JsonResponse("Please Check Your email")
            else:
                return JsonResponse(msg)
        else:
            data = serializer.errors
            return JsonResponse(data)


@api_view(['GET',])
@authentication_classes((TokenAuthentication, ))
@permission_classes([IsAuthenticated])
def checkServerTime_view(request):
    if request.method == 'GET':
        try:
            cli = Client()
            status = cli.get_server_time()
            return JsonResponse(status)
        except Exception as e:
            return JsonResponse(e)



@api_view(['GET',])
@authentication_classes((TokenAuthentication, ))
@permission_classes([IsAuthenticated])
def get_system_status_view(request):
    if request.method == "GET":
        cli = Client()
        status = cli.get_system_status()
        return JsonResponse(status)


@api_view(['GET',])
@authentication_classes((TokenAuthentication, ))
@permission_classes([IsAuthenticated])
def get_exchange_info_view(request):
    if request.method == "GET":
        cli = Client()
        info = cli.get_exchange_info()
        return JsonResponse(info)



"""
    GENERAL ENDPOINTS
"""
@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes([IsAuthenticated])
def get_order_book_view(request):
    '''Parameters:	
        symbol (str) – required
        limit (int) – Default 100; max 1000.'''
    if request.method == "POST":
        cli = Client()
        data = request.data 
        order_book = cli.get_order_book(**data)
        return JsonResponse(order_book,safe=False)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes([IsAuthenticated])
def get_recent_trades_view(request):
    '''Parameters:	
        symbol (str) – required
        limit  (int) - def = 500 to max = 500
        '''
    if request.method == "POST":
        cli = Client()
        data = request.data
        recent = cli.get_recent_trades(**data)
        return JsonResponse(recent,safe=False)



@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes([IsAuthenticated])
def get_historical_trades_view(request):
    '''Parameters:	
        symbol (str) – required
        limit  (int) - def = 500 to max = 500
        fromId (str) - TradeId to fetch from. Default gets most recent trades.
        '''
    if request.method == "POST":
        cli = Client()
        data = request.data
        try:
            recent = cli.get_historical_trades(**data)
            return JsonResponse(recent,safe=False)
        except BinanceAPIException as e:
            return JsonResponse({"MessageError":e.message},safe=False)



@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes([IsAuthenticated])
def get_aggregate_trades_view(request):
    '''Parameters:	
            symbol (str) – required
            fromId (str) – ID to get aggregate trades from INCLUSIVE.
            startTime (int) – Timestamp in ms to get aggregate trades from INCLUSIVE.
            endTime (int) – Timestamp in ms to get aggregate trades until INCLUSIVE.
            limit (int) – Default 500; max 500.
        '''
    if request.method == "POST":
        cli = Client()
        data = request.data
        try:
            agg = cli.get_aggregate_trades(**data)
            return JsonResponse(agg,safe=False)
        except BinanceAPIException as e:
            return JsonResponse({"MessageError":e.message},safe=False)



@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes([IsAuthenticated])
def get_klines(request):
    '''Parameters:	
            symbol (str) – required
            interval (str) –
            limit (int) –
            Default 500; max 500.
            startTime (int) –
            endTime (int) –
        '''
    if request.method == "POST":
        cli = Client()
        data = request.data
        try:
            agg = cli.get_klines(**data)
            return JsonResponse(agg,safe=False)
        except BinanceAPIException as e:
            return JsonResponse({"MessageError":e.message},safe=False)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes([IsAuthenticated])
def get_historical_klines(request):
    '''Parameters:	
            symbol (str) – Name of symbol pair e.g BNBBTC
            interval (str) – Binance Kline interval
            start_str (str|int) – Start date string in UTC format or timestamp in milliseconds
            end_str (str|int) – optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
            limit (int) – Default 500; max 1000.–
        '''
    if request.method == "POST":
        cli = Client()
        data = request.data
        try:
            agg = cli.get_historical_klines(**data)
            return JsonResponse(agg,safe=False)
        except BinanceAPIException as e:
            return JsonResponse({"MessageError":e.message},safe=False)



@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes([IsAuthenticated])
def get_avg_price_view(request):
    '''Parameters:	
            symbol (str) – Name of symbol pair e.g BNBBTC
        '''
    if request.method == "POST":
        cli = Client()
        data = request.data
        try:
            agg = cli.get_avg_price(**data)
            return JsonResponse(agg,safe=False)
        except BinanceAPIException as e:
            return JsonResponse({"MessageError":e.message},safe=False)



@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes([IsAuthenticated])
def get_ticker_view(request):
    '''Parameters:	
            symbol (str) – Name of symbol pair e.g BNBBTC
        '''
    if request.method == "POST":
        cli = Client()
        data = request.data
        try:
            agg = cli.get_ticker(**data)
            return JsonResponse(agg,safe=False)
        except BinanceAPIException as e:
            return JsonResponse({"MessageError":e.message},safe=False)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes([IsAuthenticated])
def get_all_tickers_view(request):
    '''Parameters:	
            symbol (str) – Name of symbol pair e.g BNBBTC
        '''
    if request.method == "POST":
        cli = Client()
        data = request.data
        try:
            agg = cli.get_all_tickers(**data)
            return JsonResponse(agg,safe=False)
        except BinanceAPIException as e:
            return JsonResponse({"MessageError":e.message},safe=False)




"""
This is Class base view 
Checks for Validation link and Activate The Account
"""
class Verification_view(View):

    def get(self, request, uid, token):
        try:
            user_id = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)

            if not email_token.check_token(user,token):
                return JsonResponse('The link is invalid')

            if user.is_active:
                return JsonResponse("Your account is active")
            user.is_active = True
            user.save()
            return JsonResponse("Your account Is now active")
        except Exception as e:
            return JsonResponse(e)
        return JsonResponse("Ok")


"""
The CustomAuthToken is Class That contains The Custom authtication 
And Also Acts Like Login process
"""
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        try: 
            User.objects.get(username__exact=request.data['username'])
        except User.DoesNotExist:
            return JsonResponse("Username Dose Not exists")
        try:
            user = User.objects.get(username__exact=request.data['username'])
            if not user.is_active:
                return JsonResponse('Please activate Your account First')
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
        except:
            return JsonResponse("Please Check You username Or Password")
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
