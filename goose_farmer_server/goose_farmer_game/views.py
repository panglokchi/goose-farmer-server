from rest_framework import viewsets, permissions, generics, status

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

from django.contrib.auth import login
from django.contrib.auth.models import User

from .serializers import UserSerializer, CreateInactiveUserSerializer, VerificationTokenSerializer
from .util import send_email_verification
from .models import VerificationToken

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)

class ExampleView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
    
class RegistrationView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = CreateInactiveUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
    
        token = VerificationTokenSerializer(data={})
        token.is_valid()
        token = token.save(user_id=user.id)

        print(user.email, token.key)
        #send_email_verification(user.email, token.key)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
    
class verificationView(generics.GenericAPIView):
    #queryset = User.objects.all()
    #serializer_class = CreateInactiveUserSerializer

    def post(self, request, *args, **kwargs):
        try:
            token = VerificationToken.objects.get(pk=request.data["key"])
        except VerificationToken.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user = User.objects.get(pk=token.user_id)
        user.is_active = True
        user.save()

        token.delete()

        return Response(status=status.HTTP_200_OK) 
    
