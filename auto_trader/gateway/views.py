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
def get_order_book_view(request):
    '''Parameters:	
        symbol (str) – required
        limit (int) – Default 100; max 1000.'''
    if request.method == "POST":
        cli = Client()
        data = request.data 
        order_book = cli.get_order_book(**data)
        return JsonResponse(order_book)


@api_view(['GET','POST'])
def getKline():
    '''Parameters:	
        symbol (str) – required
        interval (str) –
        limit (int) –
        Default 500; max 500.
        startTime (int) –
        endTime (int) –'''
    pass



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
