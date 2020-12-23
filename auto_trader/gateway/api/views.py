from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from gateway.models import User
from django.views import View
from gateway.api.serializers import UserRegisterSerializer
from rest_framework.authtoken.models import Token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .utils import email_token
from .utils import emailVerifi
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from binance.client import Client
#from binance.client import Client

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
                return Response("Please Check Your email")
            else:
                return Response(msg)
        else:
            data = serializer.errors
            return Response(data)


"""
This view just test server for live
"""
@api_view(['GET',])
@authentication_classes((TokenAuthentication, ))
@permission_classes([IsAuthenticated])
def checkServer_view(request):
    if request.method == 'GET':
        cli = Client()
        return cli.ping()


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
                return HttpResponse('The link is invalid')

            if user.is_active:
                return HttpResponse("Your account is active")
            user.is_active = True
            user.save()
            return HttpResponse("Your account Is now active")
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse("Ok")


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
            return Response("Username Dose Not exists")
        try:
            user = User.objects.get(username__exact=request.data['username'])
            if not user.is_active:
                return Response('Please activate Your account First')
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
        except:
            return Response("Please Check You username Or Password")
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


