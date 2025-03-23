from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

from datetime import timedelta

import binascii
from os import urandom as generate_bytes

from .defines import RARITY, EXP_REQUIRED

from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True

# Create your models here.

class Token(models.Model):
    def random_string():
        return str(binascii.hexlify(generate_bytes(6)).decode())
    created = models.DateTimeField(auto_now_add=True, blank=True)
    expiry = models.DateTimeField(null=True, blank=True, default=timezone.now()+timedelta(hours=10))
    key = models.CharField(primary_key=True, default=random_string)
    user = models.ForeignKey('auth.User', related_name='verificationtokens', on_delete = models.CASCADE)

    class Meta:
        abstract = True

class VerificationToken(Token):
    pass

class Player(User):
    exp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    eggs = models.DecimalField(default=0, validators=[MinValueValidator(0)], decimal_places=2, max_digits=4)
    coop_level = models.IntegerField(default=1)
    summons = models.IntegerField(default=0)
    feed = models.IntegerField(default=0)

class BirdType(models.Model):
    name = models.TextField()
    species = models.TextField()
    icon = models.CharField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    min_weight = models.DecimalField(decimal_places=2, max_digits=4)
    max_weight = models.DecimalField(decimal_places=2, max_digits=4)
    egg_timer = models.DurationField(default=timedelta(days=1))

class Bird(models.Model):
    name = models.TextField()
    bird_type = models.ForeignKey(BirdType, related_name='birds', on_delete=models.PROTECT)
    owner = models.ForeignKey(Player, related_name='birds', on_delete=models.SET_NULL, null=True)
    icon = models.CharField(null=True, blank=True)
    weight = models.DecimalField(decimal_places=2, max_digits=4)
    base_color = models.CharField()
    extra_color = models.CharField(null=True, blank=True)
    beak_color = models.CharField(null=True, blank=True)
    leg_color = models.CharField(null=True, blank=True)
    eye_color = models.CharField(null=True, blank=True)
    rarity = models.CharField(choices=RARITY.choices())
    egg_timer = models.DurationField(default=timedelta(days=1))
    health = models.PositiveIntegerField(default=100)
    stars = models.CharField(default=3)
    exp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=0)
    is_new = models.BooleanField(default=True)
    assigned_to_coop = models.BooleanField(default=False)

    def __get_exp_multipler(self):
        if self.rarity == RARITY.COMMON:
            return 0.5
        if self.rarity == RARITY.RARE:
            return 1
        if self.rarity == RARITY.EPIC:
            return 1.5
        if self.rarity == RARITY.LEGENDARY:
            return 2
    
    def __get_egg_multiplier(self):
        if self.rarity == RARITY.COMMON:
            return 1
        if self.rarity == RARITY.RARE:
            return 2
        if self.rarity == RARITY.EPIC:
            return 3
        if self.rarity == RARITY.LEGENDARY:
            return 4

    @property
    def last_level_exp(self):
        return EXP_REQUIRED[self.level-1]*self.__get_exp_multipler()

    @property
    def next_level_exp(self):
        return EXP_REQUIRED[self.level]*self.__get_exp_multipler()

    @property
    def egg_amount(self):
        return self.level * self.__get_egg_multiplier()

class DropWeight(models.Model):
    bird_type = models.ForeignKey(BirdType, related_name='drop_weights', on_delete=models.CASCADE)
    base_color = models.CharField()
    extra_color = models.CharField(null=True, blank=True)
    beak_color = models.CharField(null=True, blank=True)
    leg_color = models.CharField(null=True, blank=True)
    eye_color = models.CharField(null=True, blank=True)
    rarity = models.CharField(choices=RARITY.choices())
    drop_weight = models.IntegerField(default=1)

class Mission(models.Model):
    player = models.ForeignKey(Player, related_name='missions', on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField(blank=True)
    expiry = models.DateTimeField(blank=True, null=True)
    exp_reward = models.PositiveBigIntegerField(default=0)
    egg_reward = models.PositiveBigIntegerField(default=0)
    feed_reward = models.PositiveBigIntegerField(default=0)
    summon_reward = models.PositiveBigIntegerField(default=0)

class MissionObjective(models.Model):
    mission = models.ForeignKey(Mission, related_name='objectives', on_delete=models.CASCADE)
    name = models.TextField()
    short_name = models.CharField()
    progress = models.PositiveIntegerField(default=0)
    target = models.PositiveIntegerField(default=1)