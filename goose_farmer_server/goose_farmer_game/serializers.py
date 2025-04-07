from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Player, VerificationToken, BirdType, Bird, DropWeight, Mission, MissionObjective

class CreateInactiveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'email', 'is_active')

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'],
                                        validated_data['email'],
                                        validated_data['password'],
                                        is_active = False)
        return user
    
class CreateInactivePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'email', 'is_active')

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'],
                                        validated_data['email'],
                                        validated_data['password'],
                                        is_active = False)
        player = Player.objects.create(user=user)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'last_login', 'date_joined')

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        None,
                                        validated_data['password'])
        return user

class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Player
        fields = ('user', 'level',)

class PlayerSerializerFull(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Player
        fields = ('user', 'exp', 'level', 'eggs', 'coop_level', 'summons', 'feed',)

class VerificationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationToken
        fields = ['user_id']

class BirdTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirdType
        fields = '__all__'

class BirdSerializer(serializers.ModelSerializer):
    bird_type = BirdTypeSerializer()
    egg_timer = serializers.SerializerMethodField()

    last_level_exp = serializers.SerializerMethodField()
    next_level_exp = serializers.SerializerMethodField()
    egg_amount = serializers.SerializerMethodField()
    egg_timer_max = serializers.SerializerMethodField()

    
    def get_egg_timer(self, object):
        return object.egg_timer.total_seconds()
    
    def get_last_level_exp(self, object):
        return object.last_level_exp
    
    def get_next_level_exp(self, object):
        return object.next_level_exp
    
    def get_egg_amount(self, object):
        return object.egg_amount
    
    def get_egg_timer_max(self, object):
        return object.egg_timer_max.total_seconds()

    class Meta:
        model = Bird
        fields = '__all__'

class DropWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropWeight
        fields = '__all__'

class MissionSerializer(serializers.ModelSerializer):
    objectives = serializers.SerializerMethodField()

    def get_objectives(self, object):
        return MissionObjectiveSerializer(object.objectives.all(), many=True).data
    
    class Meta:
        model = Mission
        fields = '__all__'

class MissionObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionObjective
        fields = '__all__'