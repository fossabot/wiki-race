import math
from typing import Dict, Any, List, Optional

from django.db.models import F
from django.forms import model_to_dict
from django.http import HttpRequest
from django.utils import timezone

from wiki_app.models import User, Party, PartyMember, AdminRole, Round, MemberRound
from wiki_race.settings import USER_COOKIE_NAME, POINTS_FOR_SOLVING
from wiki_race.wiki_api.parse import generate_round, check_valid_transition, compare_titles


def get_user(request: HttpRequest) -> User:
    user_id = request.COOKIES.get(USER_COOKIE_NAME)
    if user_id is None:
        new_user = User()
        new_user.save()
        return new_user
    return User.objects.get(uid=user_id)


def _create_party(admin_user: User, form: Dict) -> Party:
    time_limit = int(form["time_limit_seconds"])
    admin_name = form["name"]
    party = Party(time_limit=time_limit)
    party.save()
    member = PartyMember(name=admin_name, user=admin_user, party=party)
    member.save()
    admin_role = AdminRole(party=party, admin_member=member)
    admin_role.save()
    return party


def _join_party(user: User, form: Dict) -> str:
    game_id = form["game_id"]
    name = form["name"]

    party = Party.objects.get(uid=game_id)
    PartyMember(user=user, name=name, party=party).save()

    return game_id


def is_admin(party: Party, user: User) -> bool:
    try:
        return party.adminrole.admin_member.user == user
    except:
        return False


def check_is_member(party: Party, user: User) -> bool:
    try:
        return party.members.filter(user=user).count() > 0
    except:
        return False


def new_round(party: Party) -> Round:
    start, end, solution = generate_round()

    party_round = Round(party=party, start_page=start, end_page=end, solution=solution)
    party_round.save()

    for member in party.members.all():
        member_round = MemberRound(member=member, round=party_round, current_page=start)
        member_round.save()

    return party_round


def get_round_info(party_round: Round) -> dict:
    res = model_to_dict(party_round, fields=["start_page", "end_page"])
    res['time_limit'] = party_round.party.time_limit
    return res


def get_member_round_info(member_round: MemberRound) -> dict:
    res = get_round_info(member_round.round)
    res['time_limit'] = get_left_seconds(member_round)
    return res


def generate_leaderboards(party: Party) -> List[dict]:
    admin = party.adminrole.admin_member
    res = [{
        'name': member.name,
        'is_admin': admin == member,
        'points': member.points
    } for member in party.members.all()]
    # TODO: try speeding up with query
    res.sort(key=(lambda x: x['points']), reverse=True)
    return res


def finish_round(party_round: Round) -> dict:
    party = party_round.party

    party_round.running = False
    party_round.save(update_fields=["running"])

    leaderboards = generate_leaderboards(party)
    return {
        "solution": party_round.solution,
        "leaderboards": leaderboards
    }


def get_latest_party_round(party: Party) -> Optional[Round]:
    try:
        return party.rounds.latest("start_time")
    except Round.DoesNotExist:
        pass


def get_latest_member_round(party: Party, user: User) -> Optional[MemberRound]:
    party_round = get_latest_party_round(party)
    if not party_round:
        return
    try:
        return party_round.member_rounds.get(member__user=user)
    except Round.DoesNotExist:
        pass
    except MemberRound.DoesNotExist:
        pass


def get_left_seconds(member_round: MemberRound) -> int:
    seconds_since_start = math.floor((timezone.now() - member_round.round.start_time).total_seconds())
    return member_round.round.party.time_limit - seconds_since_start


def member_click(member_round: MemberRound, clicked_page: str) -> bool:
    member_solved = compare_titles(clicked_page, member_round.round.end_page)
    if member_solved:
        member_round.solved_at = get_left_seconds(member_round)
        member_round.member.points = F("points") + POINTS_FOR_SOLVING + member_round.solved_at
        member_round.member.save(update_fields=["points"])

    member_round.current_page = clicked_page
    member_round.save(update_fields=["solved_at", "current_page"])

    return member_solved
