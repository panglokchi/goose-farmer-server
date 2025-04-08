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

def update_daily_missions(user=None):
    if (user is None):
        missions_to_delete = models.Mission.objects.filter(
            repeat=REPEAT.DAILY.name
        ).prefetch_related('objectives')
    else:
        missions_to_delete = models.Mission.objects.filter(
            player=user.player,
            repeat=REPEAT.DAILY.name
        ).prefetch_related('objectives')

    for m in missions_to_delete:
        # Delete all objectives related to the mission
        m.objectives.all().delete()
        missions_to_delete.delete()

    if (user is None):
        players = models.Player.objects.all()
    else:
        players = [models.Player.objects.get(user=user)]

    for player in players:
        mission = models.Mission.objects.create(
            player=player,
            name="Log In",
            description="Log in to the game",
            repeat=REPEAT.DAILY.name,
            exp_reward=20,
            egg_reward=10,
            feed_reward=10,
            summon_reward=1
        )
        models.MissionObjective.objects.create(
            mission=mission,
            name="Log in",
            short_name="log_in",
            progress=1,
            target=1
        )
        mission = models.Mission.objects.create(
            player=player,
            name="Summon a Bird",
            description="Summon a bird to your farm",
            repeat=REPEAT.DAILY.name,
            exp_reward=20,
            egg_reward=0,
            feed_reward=0,
            summon_reward=3
        )
        models.MissionObjective.objects.create(
            mission=mission,
            name="Summon a bird",
            short_name="summon",
            progress=0,
            target=1
        )
        mission = models.Mission.objects.create(
            player=player,
            name="Feed a Bird",
            description="Early bird gets the worm",
            repeat=REPEAT.DAILY.name,
            exp_reward=20,
            egg_reward=0,
            feed_reward=20,
            summon_reward=0
        )
        models.MissionObjective.objects.create(
            mission=mission,
            name="Feed a bird",
            short_name="feed",
            progress=0,
            target=1
        )
        mission = models.Mission.objects.create(
            player=player,
            name="Release a Bird",
            description="See me fly, I'm proud to fly up high",
            repeat=REPEAT.DAILY.name,
            exp_reward=20,
            egg_reward=0,
            feed_reward=0,
            summon_reward=5
        )
        models.MissionObjective.objects.create(
            mission=mission,
            name="Release a bird",
            short_name="release",
            progress=0,
            target=1
        )

