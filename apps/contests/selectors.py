import math
from time import time_ns

from django.db.models import Avg, Min, Max
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from django.db.models import Q


from config import SOLVE_SUBMITTED_STATE, SOLVE_CHANGED_TO_EXTRA_STATE, SOLVE_PENDING_STATE
from .models import (
    RoundSessionModel,
    SolveModel,
    ContestModel,
    DisciplineModel,
    ScrambleModel,
    SingleResultLeaderboardModel,
    User
)
from .filters import (
    RoundSessionFilter,
    ContestFilter,
)
from .paginators import page_size_page_paginator
from .general_selectors import retrieve_current_scramble_avg5, current_contest_retrieve


class RoundSessionSelector:

    def list_contest_leaderboard(self, contest_slug, filters=None):
        filters = filters or {}
        # TODO add prefetch_related & select_related
        round_session_set = RoundSessionModel.objects.all()

        return RoundSessionFilter(filters, round_session_set).qs

    def contest_leaderboard(self, contest_slug, filters=None):
        filters = filters or {}
        # TODO add prefetch_related & select_related
        round_session_set = RoundSessionModel.objects.filter(contest__slug=contest_slug)

        return RoundSessionFilter(filters, round_session_set).qs

    def retrieve_with_solves(self, params, user_id):
        round_session = RoundSessionModel.objects.get(
            user_id=user_id,
            contest_id=params['contest_id'],
            discipline_id=params['discipline_id']
        )
        return round_session

    def retrieve_place(self, params, user_id):
        # Assuming the rating field in the Rating model is named 'value'
        round_session = RoundSessionModel.objects.filter(
            user_id=user_id,
            contest_id=params['contest_id'],
            discipline_id=params['discipline_id']
        ).aggregate(Avg('avg_ms'))['avg_ms__avg']

        higher_rated_round_sessions = RoundSessionModel.objects.filter(
            avg_ms__lt=round_session,
            contest_id=params['contest_id'],
            discipline_id=params['discipline_id']
        )
        print(higher_rated_round_sessions)
        place = higher_rated_round_sessions.count() + 1
        return place

    def retrieve_current(self, params, user_id):
        round_session = RoundSessionModel.objects.get(
            user=user_id, contest__slug=params['contest_slug'],
            discipline_slug=params['discipline_slug'],
            user_id=user_id
        )
        return round_session

    def is_finished(self, discipline_id, contest_id, user_id):
        round_session = RoundSessionModel.objects.get(
            user=user_id, contest__slug=contest_id,
            discipline_id=discipline_id,
            user_id=user_id
        )
        is_finished = round_session.is_finished
        return is_finished


class SolveSelector:
    def list(self, filters=None):
        pass

    def retrieve(self, pk):
        # TODO add select_related and prefetch_related
        try:
            solve = SolveModel.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404
        return solve

    def list_best_in_every_discipline(self):

        disciplines = DisciplineModel.objects.all()
        solve_set = []
        # TODO add select related and prefetch related
        for discipline in disciplines:
            solve = discipline.solve_set.order_by('time_ms').filter(submission_state='submitted',
                                                                    contest__is_ongoing=False,
                                                                    round_session__is_finished=True,
                                                                    is_dnf=False).first()
            if solve:
                solve_set.append(solve)
        return solve_set

    def list_best_of_every_user(self, params):

        solve_set = SolveModel.objects.annotate(best_time_ms=Min('time_ms'))
        return solve_set

    def onging_contest_submitted(self, contest_slug, discipline_slug, user_id):
        solve_set = SolveModel.objects.filter(
            user=user_id,
            # contest__slug=contest_slug,
            # discipline__slug=discipline_slug,
            # submission_state='submitted',
        )
        return solve_set

    def retrieve_current(self, contest_slug, discipline_slug, user_id):
        try:
            solve = SolveModel.objects.get(
                contest__slug=contest_slug,
                discipline__slug=discipline_slug,
                user=user_id,
                submission_state='pending'
            )
        except ObjectDoesNotExist:
            solve = None
        return solve

    def can_change_current_to_extra(self, contest_slug, discipline_slug, user_id):
        solve_set = SolveModel.objects.filter(
            contest__slug=contest_slug,
            discipline__slug=discipline_slug,
            user=user_id,
            submission_state='changed_to_extra'
        )
        if len(solve_set) >= 2:
            return False
        else:
            return True


# class that shows info about current solve and submitted solves
class CurrentRoundSessionProgressSelector:
    def __init__(self, user_id, discipline_slug):
        try:
            self.user = User.objects.get(id=user_id)
            self.discipline = DisciplineModel.objects.get(slug=discipline_slug)
            self.contest = ContestModel.objects.filter(is_ongoing=True).last()
        except ObjectDoesNotExist:
            raise Http404

    def _can_change_to_extra(self):
        solve_set = SolveModel.objects.filter(
            contest=self.contest,
            discipline=self.discipline,
            user=self.user,
            submission_state='changed_to_extra'
        )
        if len(solve_set) >= 2:
            return False
        else:
            return True

    def _retrieve_current_solve(self):
        try:
            current_solve = SolveModel.objects.get(
                user=self.user,
                contest=self.contest,
                discipline=self.discipline,
                submission_state='pending'
            )
        except ObjectDoesNotExist:
            current_solve = None
        return current_solve

    def _list_submitted_solve_set(self):
        solve_set = self.contest.solve_set.filter(
            user=self.user,
            discipline=self.discipline,
            submission_state='submitted',
        ).order_by('id')
        return solve_set

    def _round_session_is_finished(self):
        try:
            round_session = RoundSessionModel.objects.get(
                user=self.user,
                contest=self.contest,
                discipline=self.discipline
            )
            if round_session.is_finished:
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False

    def retrieve_data(self):
        if self._round_session_is_finished():
            raise PermissionDenied()
        current_solve = self._retrieve_current_solve()
        current_scramble = retrieve_current_scramble_avg5(contest=self.contest, discipline=self.discipline, user=self.user)
        can_change_to_extra = self._can_change_to_extra()
        solve_set = self._list_submitted_solve_set()

        data = {'current_solve': {'solve': current_solve,
                                        'scramble': current_scramble,
                                        'can_change_to_extra': can_change_to_extra},
                'submitted_solve_set': ({'solve': solve, 'scramble': current_scramble} for solve in solve_set)}

        return data


class ContestSelector:
    def current_retrieve(self):
        current_contest = ContestModel.objects.filter(is_ongoing=True).last()
        return current_contest

    def list(self, filters=None):
        filters = filters or {}

        contest_set = ContestModel.objects.filter(is_ongoing=False,
                                                  discipline_set__slug=filters.get('discipline_slug')).order_by('-id')
        return ContestFilter(filters, contest_set).qs


class ScrambleSelector:
    def retrieve_current(self, contest, discipline, user):
        scrambles = contest.scramble_set.all()
        previous_solve = None
        for scramble in scrambles:
            solve = scramble.solve_set.filter(user=user).first()
            if not solve:
                if not previous_solve:
                    return scramble
                elif previous_solve.state == SOLVE_SUBMITTED_STATE:
                    return scramble
                elif previous_solve.state == SOLVE_CHANGED_TO_EXTRA_STATE:
                    while True:
                        extra_scramble = ScrambleModel.objects.get(id=previous_solve.extra_id)
                        extra_solve = extra_scramble.solve_set.filter(user=user).first()
                        if not extra_solve:
                            return extra_scramble
                        elif extra_solve.state == SOLVE_PENDING_STATE:
                            return extra_scramble
                        elif extra_solve.state == SOLVE_SUBMITTED_STATE:
                            return scramble
                        elif extra_solve.state == SOLVE_CHANGED_TO_EXTRA_STATE:
                            previous_solve = extra_solve

            elif solve.submission_state == SOLVE_PENDING_STATE:
                return scramble


class SingleResultLeaderboardSelector:
    def __init__(self, user_id, discipline_slug):
        try:
            # self.user = User.objects.get(id=user_id)
            self.discipline = DisciplineModel.objects.get(slug=discipline_slug)
        except ObjectDoesNotExist:
            raise Http404

    def list(self, own_solve_id=None):
        solve_set = (SingleResultLeaderboardModel.objects.filter(solve__discipline=self.discipline)
                     .exclude(id=own_solve_id).order_by('time_ms'))
        return solve_set

    def own_solve_retrieve(self, user_id):
        try:
            own_solve = SingleResultLeaderboardModel.objects.get(solve__user_id=user_id, solve__discipline=self.discipline)
            return own_solve
        except ObjectDoesNotExist:
            return None

    def get_place(self, solve):
        position = SingleResultLeaderboardModel.objects.filter(time_ms__lt=solve.time_ms,
                                                               solve__discipline=self.discipline).count() + 1
        return position

    def add_places(self, solve_set):
        solve_set_with_places = []
        for solve in solve_set:
            solve_set_with_places.append({'solve': solve.solve, 'place': self.get_place(solve)})

        return solve_set_with_places

    def get_page(self, page_size, solve):
        place = self.get_place(solve)
        page = math.ceil(place / page_size)
        return page

    def is_displayed_separately(self, own_solve, page, page_size):
        start = (page - 1) * page_size
        end = page * page_size
        solve_set = self.list()[start:end]

        if own_solve in solve_set:
            return False
        elif own_solve is None:
            return False
        elif own_solve not in solve_set:
            return True

    def leaderboard_retrieve(self, page_size, page, user_id=None):
        data = {}

        results = {}
        own_solve = {}

        own_solve_data = self.own_solve_retrieve(user_id=user_id)
        if own_solve_data:
            page_size = page_size - 1
            solve_set = self.list(own_solve_id=own_solve_data.id)
        else:
            solve_set = self.list()

        extra_page_result = 0
        if own_solve_data:
            if self.is_displayed_separately(
                own_solve=own_solve_data,
                page_size=page_size,
                page=page
            ):
                pass
            else:
                # extra_page_result = 1
                pass
        elif not own_solve_data:
            pass

        pagination_info = self._get_pagination_info(
            queryset=solve_set,
            page_size=page_size,
            page=page
        )
        paginated_solve_set = page_size_page_paginator(
            queryset=solve_set,
            page_size=page_size,
            page=page,
            extra=extra_page_result
        )

        if own_solve_data:
            own_solve['solve'] = own_solve_data.solve
            own_solve['page'] = self.get_page(page_size=page_size, solve=own_solve_data)
            own_solve['place'] = self.get_place(solve=own_solve_data)
            own_solve['is_displayed_separately'] = self.is_displayed_separately(
                own_solve=own_solve_data,
                page_size=page_size,
                page=page
            )
        data.update(pagination_info)  # adding pagination fields to response

        if not self.is_displayed_separately(own_solve=own_solve_data,
                                        page_size=page_size,
                                        page=page):
            if own_solve_data:
                paginated_solve_set = SingleResultLeaderboardModel.objects.filter(
                    Q(id=own_solve_data.id) | Q(id__in=paginated_solve_set.values_list('id', flat=True))
                ).order_by('time_ms')
            else:
                pass

        paginated_solve_set_with_solves = self.add_places(paginated_solve_set)

        if own_solve:
            results['own_result'] = own_solve
        else:
            results['own_result'] = None
        results['solve_set'] = paginated_solve_set_with_solves
        data['results'] = results
        return data

    def _get_pagination_info(self, queryset, page_size, page):
        total_items = queryset.count()
        total_pages = math.ceil(total_items / page_size)

        info = {
            'page_size': page_size,
            'page': page,
            'pages': total_pages,
        }

        return info


class ContestLeaderboardSelector:
    def get_place(self, round_session, contest, discipline):
        if round_session:
            if not round_session.is_dnf:
                position = RoundSessionModel.objects.filter(
                    avg_ms__lt=round_session.avg_ms,
                    contest=contest,
                    discipline=discipline,
                    is_finished=True
                ).count() + 1
            elif round_session.is_dnf:
                position = RoundSessionModel.objects.filter(
                    contest=contest,
                    discipline=discipline,
                    is_finished=True
                ).exclude(id=round_session.id).count() + 1
        elif round_session is None:
            position = None
        else:
            position = None
        return position

    def add_places(self, round_session_set, contest, discipline):
        round_session_set_with_places = []
        for round_session in round_session_set:
            round_session_set_with_places.append({'round_session': round_session, 'place': self.get_place(
                round_session,
                contest=contest,
                discipline=discipline,
            )})

        return round_session_set_with_places

    def get_page(self, page_size, round_session, contest, discipline):
        if round_session:
            place = self.get_place(round_session, contest, discipline)
            page = math.ceil(place / page_size)
        else:
            page = None
        return page

    def is_displayed_separately(self, own_round_session, page_size, page, discipline, contest):
        round_session_set = self.round_session_list(discipline=discipline, contest=contest)
        start = (page - 1) * page_size
        end = page * page_size
        round_session_set = round_session_set[start:end]

        if own_round_session in round_session_set:
            return False
        elif own_round_session is None:
            return True
        elif own_round_session not in round_session_set:
            return True

    def round_session_list(self, discipline, contest, own_round_session_id=None):
        round_session_set = RoundSessionModel.objects.filter(
            discipline=discipline,
            contest=contest,
            is_finished=True,
        ).order_by('avg_ms').exclude(id=own_round_session_id)
        return round_session_set

    def round_session_set_retrieve(self, discipline, contest, page_size, page, user_id):
        try:
            own_round_session = contest.round_session_set.get(user_id=user_id, discipline=discipline)
            own_round_session_id = own_round_session.id
        except ObjectDoesNotExist:
            own_round_session = None
            own_round_session_id = None
        round_session_set = RoundSessionModel.objects.filter(
            discipline=discipline,
            contest=contest,
            is_finished=True
        ).order_by('avg_ms').exclude(id=own_round_session_id)
        paginated_round_session_set = page_size_page_paginator(round_session_set, page_size, page)
        if not self.is_displayed_separately(own_round_session=own_round_session,
                                            page_size=page_size,
                                            page=page,
                                            discipline=discipline,
                                            contest=contest
                                            ):

            paginated_round_session_set = RoundSessionModel.objects.filter(
                Q(id=own_round_session.id) | Q(id__in=paginated_round_session_set.values_list('id', flat=True))
            ).order_by('avg_ms')

        paginated_round_session_set_with_places = self.add_places(
            paginated_round_session_set,
            contest,
            discipline,
        )
        return paginated_round_session_set_with_places

    def own_round_session_retrieve(self, discipline, contest, page_size, page, user_id):
        try:
            round_session = RoundSessionModel.objects.get(
                contest=contest,
                discipline=discipline,
                user_id=user_id,
                is_finished=True,
            )

        except ObjectDoesNotExist:
            round_session = None
            return round_session
        is_displayed_separately = self.is_displayed_separately(
            own_round_session=round_session,
            page_size=page_size,
            page=page,
            discipline=discipline,
            contest=contest
        )

        own_round_session = {
            'round_session': round_session,
            'place': self.get_place(round_session, contest, discipline),
            'is_displayed_separately': is_displayed_separately,
            'page': self.get_page(page_size, round_session, contest, discipline)
        }

        return own_round_session

    def get_pagination_info(self, discipline, contest, page_size, page, user_id):
        queryset = self.round_session_list(discipline, contest).exclude(user__id=user_id)
        total_items = queryset.count()
        total_pages = math.ceil(total_items / page_size)

        info = {
            'page_size': page_size,
            'page': page,
            'pages': total_pages,
        }

        return info

    def check_permission(self, contest, user_id, discipline):
        if not contest.is_ongoing:
            return True
        elif contest.is_ongoing:
            try:
                contest.round_session_set.get(user_id=user_id, is_finished=True, discipline=discipline)
                return True
            except ObjectDoesNotExist:
                raise PermissionDenied()

    def leaderboard_retrieve(self, discipline_slug, contest_slug, page_size, page, user_id):
        try:
            discipline = DisciplineModel.objects.get(slug=discipline_slug)
        except ObjectDoesNotExist:
            raise Http404
        try:
            contest = ContestModel.objects.get(slug=contest_slug)
            self.check_permission(contest=contest, user_id=user_id, discipline=discipline)
        except ObjectDoesNotExist:
            raise Http404

        try:
            own_round_session = contest.round_session_set.get(user_id=user_id, discipline=discipline)
            page_size = page_size - 1
        except ObjectDoesNotExist:
            pass

        data = {'results': {}}
        data.update(self.get_pagination_info(discipline, contest, page_size, page, user_id))
        data['results']['own_result'] = self.own_round_session_retrieve(discipline, contest, page_size, page, user_id)
        data['results']['contest'] = contest
        data['results']['round_session_set'] = self.round_session_set_retrieve(discipline, contest, page_size, page,
                                                                               user_id)
        return data

class AvailableDisciplinesListSelector:
    def discipline_set_retrieve(self):
        discipline_set = DisciplineModel.objects.all()
        return discipline_set

