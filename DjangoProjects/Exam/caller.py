import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Mission, Spacecraft
from django.db.models import Q, Count, F


# Create queries within functions


def get_astronauts(search_string=None):
    if search_string is None:
        return ""

    query = Q(name__icontains=search_string) |\
    Q(phone_number__icontains=search_string)

    astronauts = Astronaut.objects.filter(query).order_by('name')

    if not astronauts.exists():
        return ""

    result = []
    for astro in astronauts:
        status = ""
        if astro.is_active:
            status = "Active"
        else:
            status = "Inactive"
        result.append(f"Astronaut: {astro.name}, phone number: {astro.phone_number}, status: {status}")

    return '\n'.join(result)


def get_top_astronaut():

    if Mission.objects.all().count() == 0 or Astronaut.objects.all().count() == 0:
        return "No data."

    top_a = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not top_a:
        return "No data."

    return f"Top Astronaut: {top_a.name} with {top_a.mission_count} missions."


def get_top_commander():
    if Mission.objects.all().count() == 0 or Astronaut.objects.all().count() == 0:
        return "No data."

    commander_assigned = False
    for mis in Mission.objects.all():
        if mis.commander:
            commander_assigned = True

    if not commander_assigned:
        return "No data."

    top_com = Astronaut.objects.prefetch_related('commander_mission').annotate(
        commands_count=Count('commander_mission'),
    ).order_by('phone_number').first()

    if not top_com:
        return ""

    return f"Top Commander: {top_com.name} with {top_com.commands_count} commanded missions."

# ------------------------------------------------------------------------------------------------------


def get_last_completed_mission():
    last_mission = Mission.objects.filter(status="Completed").last()
    if not last_mission:
        return "No data."
    astronauts_names = [a.name for a in last_mission.astronauts.order_by('name').all()]
    all_astronauts_spacewalks = sum([int(a.spacewalks) for a in last_mission.astronauts.all()])

    if last_mission.commander:
        com = last_mission.commander.name
    else:
        com = "TBA"

    return f"The last completed mission is: {last_mission.name}. Commander: {com}. "\
           f"Astronauts: {', '.join(astronauts_names)}. Spacecraft: {last_mission.spacecraft.name}. "\
           f"Total spacewalks: {all_astronauts_spacewalks}."


def get_most_used_spacecraft():
    if Mission.objects.all().count() == 0:
        return "No data."

    junk_ship = Spacecraft.objects\
        .prefetch_related('ship_missions')\
        .annotate(missions_count=Count('ship_missions'))\
        .order_by('-missions_count', 'name').first()

    missions = Mission.objects.filter(spacecraft_id=junk_ship.id)

    astro_ids = set()
    for mis in missions:
        cur_mis = mis.astronauts.prefetch_related('crew_mission').annotate(astro_count=Count('crew_mission'))
        for astro_obj in cur_mis:
            astro_ids.add(astro_obj.id)

    return f"The most used spacecraft is: {junk_ship.name}, manufactured by {junk_ship.manufacturer}, "\
           f"used in {junk_ship.missions_count} missions, astronauts on missions: {len(astro_ids)}."


def decrease_spacecrafts_weight():
    planned_missions = Mission.objects.prefetch_related('spacecraft').filter(status="Planned")
    if not planned_missions:
        return "No changes in weight."
    ship_ids = set()
    for mis in planned_missions:
        ship_ids.add(mis.spacecraft_id)

    for ship in ship_ids:
        ship_to_be_updated = Spacecraft.objects.filter(id=ship, weight__gte=200)
        for ship_obj in ship_to_be_updated:
            ship_obj.weight -= 200
            ship_obj.save()

    if len(ship_ids) == 0:
        return "No changes in weight."

    total_weight = 0
    avg_weight = 0
    all_ships = Spacecraft.objects.all()
    for ship_obj in all_ships:
        total_weight += ship_obj.weight
    if all_ships:
        avg_weight = total_weight / all_ships.count()

    return f"The weight of {len(ship_ids)} spacecrafts has been decreased. "\
           f"The new average weight of all spacecrafts is {avg_weight:.1f}kg"

print(decrease_spacecrafts_weight())

