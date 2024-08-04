import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count, Avg, F
from main_app.models import Director, Actor, Movie


# Create queries within functions
def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)
    if search_name is None and search_nationality is not None:
        query = query_nationality
    elif search_name is not None and search_nationality is None:
        query = query_name
    else:
        query = Q(query_name & query_nationality)

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors.exists():
        return ""

    result = []
    for director in directors:
        result.append(f"Director: {director.full_name}, nationality: {director.nationality}, "
                      f"experience: {director.years_of_experience}")

    return '\n'.join(result)


def get_top_director():
    top_dir = Director.objects.get_directors_by_movies_count().first()

    if not top_dir:
        return ""

    return f"Top Director: {top_dir.full_name}, movies: {top_dir.director_movies.count()}."


def get_top_actor():
    top_actor = (Actor.objects.prefetch_related('star_movies')
                 .annotate(star_count=Count('star_movies'),
                           avg_rat=Avg('star_movies__rating'))
                 .order_by('-star_count', 'full_name')).first()

    if not top_actor or not top_actor.star_count:
        return ""

    movies_starred = top_actor.star_movies.all()
    movie_titles = []
    for movie in movies_starred:
        movie_titles.append(movie.title)

    return f"Top Actor: {top_actor.full_name}, " \
           f"starring in movies: {', '.join(movie_titles)}, " \
           f"movies average rating: {top_actor.avg_rat:.1f}"


# print(get_top_actor())
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_actors_by_movies_count():
    actors = (Actor.objects.prefetch_related('cast')
                   .annotate(cast_count=Count('cast'))
                   .order_by('-cast_count', 'full_name'))[0:3]

    if not actors or not actors[0].cast_count:
        return ""

    result = []
    for actor in actors:
        result.append(f'{actor.full_name}, participated in {actor.cast_count} movies')

    return '\n'.join(result)


def get_top_rated_awarded_movie():
    top_movie = (Movie.objects.prefetch_related('actors')
                 .select_related('starring_actor')
                 .filter(is_awarded=True)
                 .order_by('-rating', 'title')
                 ).first()

    if not top_movie:
        return ""

    if top_movie.starring_actor:
        star = top_movie.starring_actor.full_name
    else:
        star = 'N/A'

    cast = [actor.full_name for actor in top_movie.actors.order_by('full_name')]

    return f"Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating:.1f}. "\
           f"Starring actor: {star}. "\
           f"Cast: {', '.join(cast)}."


def increase_rating():
    movies_to_update = (Movie.objects
                        .filter(rating__lte=9.9, is_classic=True)
                        .update(rating=F('rating') + 0.1))

    if not movies_to_update:
        return "No ratings increased."

    return f"Rating increased for {movies_to_update} movies."


# print(increase_rating())
