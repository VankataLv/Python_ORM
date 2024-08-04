import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match
from django.db.models import Q, Count, F


# Create queries within functions
def get_tennis_players(search_name=None, search_country=None) -> str:
    query_name = Q(full_name__icontains=search_name)
    query_country = Q(country__icontains=search_country)

    if search_name is not None and search_country is not None:
        query = Q(query_name & query_country)

    elif search_name is not None and search_country is None:
        query = query_name

    elif search_name is None and search_country is not None:
        query = query_country

    else:
        return ""

    players = TennisPlayer.objects.filter(query).order_by('ranking')

    if players:
        result = []
        for player in players:
            result.append(f"Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}")

        return '\n'.join(result)

    else:
        return ""


def get_top_tennis_player():
    player_top = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if player_top:
        return f"Top Tennis Player: {player_top.full_name} with {player_top.wins} wins."
    else:
        return ""


def get_tennis_player_by_matches_count():
    player = TennisPlayer.objects.annotate(matches=Count('match')).order_by('-matches', 'ranking').first()

    if player is None or player.matches == 0:
        return ""

    return f"Tennis Player: {player.full_name} with {player.matches} matches played."


# ---------------------------------------------------------------------------------------------------
def get_tournaments_by_surface_type(surface=None):
    if surface is None or Tournament.objects.count() == 0:
        return ""

    query = Q(surface_type__icontains=surface)
    tournaments = (Tournament.objects.prefetch_related('matches_tournament')
                   .annotate(matches_count=Count('matches_tournament'))
                   .filter(query).order_by('-start_date'))

    if not tournaments:
        return ""

    result = []
    for tour in tournaments:
        result.append(f"Tournament: {tour.name}, start date: {tour.start_date}, matches: {tour.matches_count}")

    return '\n'.join(result)


def get_latest_match_info():
    if Match.objects.count() == 0:
        return ""

    last_match = Match.objects.order_by('date_played', 'id').last()
    tour_name = last_match.tournament.name
    players = [p.full_name for p in last_match.players.order_by('full_name')]
    if last_match.winner:
        winner = last_match.winner.full_name
    else:
        winner = "TBA"

    return (f"Latest match played on: {last_match.date_played}, tournament: {tour_name}, score: {last_match.score}, "
            f"players: {players[0]} vs {players[1]}, winner: {winner}, summary: {last_match.summary}")


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None or Tournament.objects.count() == 0:
        return "No matches found."

    matches = (Match.objects.select_related('tournament', 'winner')
               .filter(tournament__name__exact=tournament_name)
               .order_by('-date_played'))

    if not matches:
        return "No matches found."

    result = []
    for match in matches:

        if match.winner:
            winner = match.winner.full_name
        else:
            winner = "TBA"

        result.append(f'Match played on: {match.date_played}, score: {match.score}, winner: {winner}')
    return '\n'.join(result)


# print(get_matches_by_tournament(tournament_name='Tournament 1'))
