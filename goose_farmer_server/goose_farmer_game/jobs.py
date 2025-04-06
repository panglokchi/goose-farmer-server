from . import models

from datetime import timedelta



def update_egg_timers(delta = timedelta(seconds=60)):
    birds_to_update = models.Bird.objects.filter(
        assigned_to_coop = True,
        #egg_timer__gte=delta
    )
    for b in birds_to_update:
        if b.egg_timer < delta:
            b.egg_timer = timedelta(seconds=0)
        else:
            b.egg_timer -= delta
    
    models.Bird.objects.bulk_update(
        birds_to_update, ['egg_timer']
    )