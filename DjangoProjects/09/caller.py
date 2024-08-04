import os
import django
from django.db.models import QuerySet, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


# from populate_db import populate_model_with_data

# -------------- 1 -------------------

def create_pet(name_arg: str, species_arg: str):
    cur_pet = Pet.objects.create(name=name_arg, species=species_arg)
    return f"{cur_pet.name} is a very cute {cur_pet.species}!"


# -------------- 2 -------------------
def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    cur_artifact = Artifact.objects.create(name=name, origin=origin, age=age,
                                           description=description, is_magical=is_magical)
    return f"The artifact {cur_artifact.name} is {cur_artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts() -> None:
    Artifact.objects.all().delete()


# -------------- 3 -------------------

def show_all_locations() -> str:
    locations = Location.objects.all().order_by('-id')

    return "\n".join(str(loc) for loc in locations)


def new_capital() -> None:
    location = Location.objects.first()
    location.is_capital = True
    location.save()


def get_capitals() -> QuerySet:
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location() -> None:
    Location.objects.first().delete()


# -------------- 4 -------------------
def apply_discount() -> None:
    cars = Car.objects.all()

    for car in cars:
        percentage_off = sum(int(digit) for digit in str(car.year)) / 100  # 2014 => 2 + 0 + 1 + 4 => 7 / 100 => 0.07
        discount = float(car.price) * percentage_off  # 1000 * 0.07 => 70
        car.price_with_discount = float(car.price) - discount  # 1000 - 70 => 930
        car.save()


def get_recent_cars() -> QuerySet:
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car() -> None:
    Car.objects.last().delete()


# -------------- 5 -------------------
# populate_model_with_data(Task)

def show_unfinished_tasks() -> str:
    return '\n'.join(str(task) for task in Task.objects.filter(is_finished=False))


def complete_odd_tasks() -> None:
    tasks = Task.objects.all()

    for task in tasks:
        if task.id % 2 != 0 and not task.is_finished:
            task.is_finished = True

    Task.objects.bulk_update(tasks, ['is_finished'])


def encode_and_replace(text: str, task_title: str) -> None:
    # tasks = Task.objects.filter(title=task_title)

    decoded_text = ''.join(chr(ord(symbol) - 3) for symbol in text)
    Task.objects.filter(title=task_title).update(description=decoded_text)

    # for task in tasks:
    #     task.description = decoded_text
    #
    # Task.objects.bulk_update(tasks, ['description'])


# -------------- 6 -------------------
def get_deluxe_rooms() -> str:
    deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe')
    even_deluxe_rooms_str = [str(r) for r in deluxe_rooms if r.id % 2 == 0]

    return '\n'.join(even_deluxe_rooms_str)


def increase_room_capacity() -> None:
    rooms_db = HotelRoom.objects.all().order_by('id')
    previous_room_cap = None
    for cur_room in rooms_db:
        if not cur_room.is_reserved:
            continue

        if previous_room_cap is not None:
            cur_room.capacity += previous_room_cap
        else:
            cur_room.capacity += cur_room.id

        previous_room_cap = cur_room.capacity

    HotelRoom.objects.bulk_update(rooms_db, ['capacity'])


def reserve_first_room() -> None:
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room() -> None:
    last_room = HotelRoom.objects.last()
    if not last_room.is_reserved:
        last_room.delete()


# -------------- 7 -------------------
def update_characters() -> None:
    Character.objects.filter(class_name="Mage").update(
        level=F('level') + 3,
        intelligence=F('intelligence') + 7
    )
    Character.objects.filter(class_name="Warrior").update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4
    )
    Character.objects.filter(class_name__in=["Assassin", "Scout"]).update(
        inventory="The inventory is empty"
    )


def fuse_characters(first_character: Character, second_character: Character) -> None:
    new_name = first_character.name + " " + second_character.name
    new_class_name = "Fusion"
    new_level = (first_character.level + second_character.level) // 2
    new_strength = (first_character.strength + second_character.strength) * 1.2
    new_dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    new_intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    new_hit_points = first_character.hit_points + second_character.hit_points
    new_inventory = ""
    if first_character.class_name in ["Mage", "Scout"]:
        new_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    elif first_character.class_name in ["Warrior", "Assassin"]:
        new_inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=new_name,
        class_name=new_class_name,
        level=new_level,
        strength=new_strength,
        dexterity=new_dexterity,
        intelligence=new_intelligence,
        hit_points=new_hit_points,
        inventory=new_inventory
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity() -> None:
    Character.objects.update(dexterity=30)


def grand_intelligence() -> None:
    Character.objects.update(intelligence=40)


def grand_strength() -> None:
    Character.objects.update(strength=50)


def delete_characters() -> None:
    Character.objects.filter(inventory="The inventory is empty").delete()
