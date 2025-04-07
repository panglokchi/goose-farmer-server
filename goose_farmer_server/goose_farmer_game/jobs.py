from . import models
from .defines import REPEAT

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

def update_daily_missions():
    missions_to_delete = models.Mission.objects.filter(
        repeat=REPEAT.DAILY.name
    ).prefetch_related('objectives')

    for m in missions_to_delete:
        # Delete all objectives related to the mission
        m.objectives.all().delete()

    missions_to_delete.delete()

    players = models.Player.objects.all()
    for player in players:
        mission = models.Mission.objects.create(
            player=player,
            name="Daily Mission",
            description="Complete your daily mission!",
            repeat=REPEAT.DAILY.name,
            exp_reward=100,
            egg_reward=10,
            feed_reward=5,
            summon_reward=1
        )
        models.MissionObjective.objects.create(
            mission=mission,
            name="Complete Daily Mission",
            short_name="Daily",
            progress=0,
            target=1
        )

