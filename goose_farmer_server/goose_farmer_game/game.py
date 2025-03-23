import random
from django.db.models import Sum

from .models import Bird, DropWeight
from . import defines

def summon_bird(guarantee = None, guarantee_chance = 0, owner = None):
    def get_random_drop(exclude=None):
        if exclude is None:
            exclude = []
        drop_weights = DropWeight.objects.exclude(pk__in=exclude)
        #total_weight = sum(dw.drop_weight for dw in drop_weights)
        total_weight = drop_weights.aggregate(sum=Sum("drop_weight"))["sum"]
        roll = random.uniform(0, total_weight)
        current_weight = 0

        for drop_weight in drop_weights:
            current_weight += drop_weight.drop_weight
            if current_weight >= roll:
                return drop_weight
            
    # If a guarantee is provided, check the chance
    if guarantee is not None:
        if random.random() < guarantee_chance:
            # If the roll is successful, use the guaranteed drop weight
            bird = guarantee
        else:
            # Roll failed, proceed to draw based on other drop weights
            bird = get_random_drop(exclude=[guarantee])
    else:
        # No guarantee, draw based on drop weights
        bird = get_random_drop()
    
    # Create and return a new Bird instance based on the chosen drop weight
    bird_type = bird.bird_type
    new_bird = Bird.objects.create(
        name=bird_type.name,
        bird_type=bird_type,
        owner=owner,
        icon=bird_type.icon,
        weight=random.uniform(float(bird_type.min_weight), float(bird_type.max_weight)),
        base_color=bird.base_color,
        extra_color=bird.extra_color,
        beak_color=bird.beak_color,
        leg_color=bird.leg_color,
        eye_color=bird.eye_color,
        rarity=bird.rarity,
        egg_timer=bird_type.egg_timer,
        #health=100,  # Default health
        stars=defines.RARITY.get_base_stars(defines.RARITY[bird.rarity]),
        #exp=0,  # Starting experience
        #level=1,  # Starting level
        is_new=True,
        assigned_to_coop=False,
    )
    return new_bird
