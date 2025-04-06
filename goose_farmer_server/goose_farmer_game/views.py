from rest_framework import viewsets, permissions, generics, status

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import SessionAuthentication # for admin console
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from . import serializers
from . import game
from .util import send_email_verification
from .models import VerificationToken, BirdType, Bird, DropWeight, Player
from .permissions import IsOwnerOrReadOnly

import math
import decimal
from datetime import timedelta

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)

class ValidateTokenView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'expiry': str(request.auth.expiry),  # None
        }
        return Response(content)
    
class RegistrationView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = serializers.CreateInactivePlayerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
    
        token = serializers.VerificationTokenSerializer(data={})
        token.is_valid()
        token = token.save(user_id=user.id)

        print(user.email, token.key)
        #send_email_verification(user.email, token.key)

        return Response({
            "user": serializers.UserSerializer(user).data
        })
    
class VerificationView(APIView):

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
    
class BirdTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser,]

    queryset = BirdType.objects.all()
    serializer_class = serializers.BirdTypeSerializer

class BirdViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser,]

    queryset = Bird.objects.all()
    serializer_class = serializers.BirdSerializer

class DropWeightsViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser,]

    queryset = DropWeight.objects.all()
    serializer_class = serializers.DropWeightSerializer

class PlayerBirdsView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.BirdSerializer
        birds = Bird.objects.filter(owner_id=request.user.player).select_related('bird_type').select_related('owner')
        birds_json = serializer(birds, many=True).data
        return Response(birds_json)

class SummonBirdView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if "times" in request.data:
            times = request.data.get("times")
        else:
            times = 1
        if times > request.user.player.summons:
            return Response(
                {"error": "Not enough summons"},
                status=status.HTTP_403_FORBIDDEN
            )
        request.user.player.summons -= times
        request.user.player.save()
        birds = []
        for i in range(times):
            bird = game.summon_bird(owner = request.user.player)
            bird.egg_timer = bird.egg_timer_max
            bird.save()
            birds.append(serializers.BirdSerializer(bird).data)
        return Response(
            birds,
            status=status.HTTP_200_OK
        )
    
class ActivateBirdView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        try:
            bird = Bird.objects.get(pk=request.data.get("bird_id"))
            if self.check_object_permissions(self.request, bird) == False:
                raise PermissionDenied()

            if request.data.get("active") == True:
                assigned_birds = Bird.objects.filter(owner = request.user.player, assigned_to_coop = True).count()
                if assigned_birds >= 6:
                    raise Exception("Too many birds assigned")
                else:
                    bird.assigned_to_coop = True;
                    bird.save()

            if request.data.get("active") == False:
                bird.assigned_to_coop = False;
                bird.save()

            return Response(status=status.HTTP_200_OK)
                    
        except Bird.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
class FeedBirdView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request):
        try:
            bird = Bird.objects.get(pk=request.data.get("bird_id"))
            if self.check_object_permissions(self.request, bird) == False:
                raise PermissionDenied()

            bird.feed(request.data.get("amount"))
            bird.save()

            serializer = serializers.BirdSerializer
            return Response(serializer(bird).data, status=status.HTTP_200_OK)
                    
        except Bird.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
class ReleaseBirdView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request):
        try:
            bird = Bird.objects.get(pk=request.data.get("bird_id"))
            if self.check_object_permissions(self.request, bird) == False:
                raise PermissionDenied()

            feed_gain = math.floor(bird.weight * bird.egg_amount * decimal.Decimal(0.8))
            bird.owner.feed += feed_gain
            bird.owner.save()
            bird.delete()
            return Response({
                "feed": feed_gain,
            }, status=status.HTTP_200_OK)
                    
        except Bird.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
class CollectEggsView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request):
        try:
            bird = Bird.objects.get(pk=request.data.get("bird_id"))
            if self.check_object_permissions(self.request, bird) == False:
                raise PermissionDenied()
            
            if bird.egg_timer > timedelta(seconds=60):
                return Response(status=status.HTTP_403_FORBIDDEN)

            egg_amount = bird.egg_amount
            bird.egg_timer = bird.egg_timer_max
            bird.save()
            bird.owner.eggs += egg_amount
            bird.owner.save()
            return Response({
                "eggs": egg_amount,
            }, status=status.HTTP_200_OK)
                    
        except Bird.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
class PlayerView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if ("username" not in request.data or request.user.player.user.username == request.data.get("username")):
            serializer = serializers.PlayerSerializerFull
            return Response(serializer(request.user.player).data)
        else:
            try:
                user = User.objects.get(username = request.data.get("username"))
                player = user.player
                serializer = serializers.PlayerSerializer
                return Response(serializer(player).data)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)