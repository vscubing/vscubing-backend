import math

from django.db.models import Avg, Min, Max
from django.core.exceptions import ObjectDoesNotExist

from config import SOLVE_SUBMITTED_STATE, SOLVE_CHANGED_TO_EXTRA_STATE, SOLVE_PENDING_STATE
from .models import (
    RoundSessionModel,
    SolveModel,
    ContestModel,
    DisciplineModel,
    ScrambleModel,
    SingleResultLeaderboardModel
)
from .filters import (
    RoundSessionFilter,
    ContestFilter,
)


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
        solve = SolveModel.objects.get(id=pk)
        return solve

    def list_best_in_every_discipline(self):

        disciplines = DisciplineModel.objects.all()
        solve_set = []
        # TODO add select related and prefetch related
        for discipline in disciplines:
            solve = discipline.solve_set.order_by('time_ms').filter(submission_state='submitted',
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


class ContestSelector:
    def current_retrieve(self):
        current_contest = ContestModel.objects.filter(is_ongoing=True).last()
        return current_contest

    def list(self, filters=None):
        filters = filters or {}

        contest_set = ContestModel.objects.all()
        return ContestFilter(filters, contest_set).qs


class ScrambleSelector:
    def retrieve_current(self, contest_slug, discipline_slug, user_id):
        scrambles = ContestModel.objects.get(slug=contest_slug).scramble_set.all()
        previous_solve = None
        for scramble in scrambles:
            solve = scramble.solve_set.filter(user=user_id).first()
            if not solve:
                if not previous_solve:
                    return scramble
                elif previous_solve.state == SOLVE_SUBMITTED_STATE:
                    return scramble
                elif previous_solve.state == SOLVE_CHANGED_TO_EXTRA_STATE:
                    while True:
                        extra_scramble = ScrambleModel.objects.get(id=previous_solve.extra_id)
                        extra_solve = extra_scramble.solve_set.filter(user=user_id).first()
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
    def list(self):
        solve_set = SingleResultLeaderboardModel.objects.order_by('time_ms')
        return solve_set

    def own_solve_retrieve(self, user_id):
        try:
            own_solve = SingleResultLeaderboardModel.objects.get(solve__user_id=user_id)
            return own_solve
        except ObjectDoesNotExist:
            return None

    def get_place(self, solve):
        position = SingleResultLeaderboardModel.objects.filter(time_ms__lt=solve.time_ms).count() + 1
        return position

    def add_places(self, solve_set):
        solve_set_with_places = []
        for solve in solve_set:
            solve_set_with_places.append({'solve': solve.solve, 'place': self.get_place(solve)})

        return solve_set_with_places

    def get_page(self, limit, solve):
        place = self.get_place(solve)
        page = math.ceil(place / limit)
        return page

    def is_displayed_separately(self, own_solve, solve_set):
        if own_solve in solve_set:
            return False
        elif own_solve is None:
            return False
        elif own_solve not in solve_set:
            return True

    def cut_last_solve(self, limit, own_solve, solve_set):
        if own_solve in solve_set:
            return solve_set
        else:
            return solve_set[:limit-1]

    def leaderboard_retrieve(self, limit, page, user_id=None):
        data = {}

        results = {}
        own_solve = {}

        solve_set = self.list()

        own_solve_data = self.own_solve_retrieve(user_id=user_id)
        if own_solve_data:
            own_solve['solve'] = own_solve_data.solve
            own_solve['page'] = self.get_page(limit=limit, solve=own_solve_data)
            own_solve['place'] = self.get_place(solve=own_solve_data)

        pagination_info = self._get_pagination_info(
            queryset=solve_set,
            limit=limit,
            page=page
        )
        paginated_solve_set = self._get_paginated_data(
            queryset=solve_set,
            limit=limit,
            page=page
        )
        own_solve['is_displayed_separately'] = self.is_displayed_separately(
            own_solve=own_solve_data,
            solve_set=paginated_solve_set
        )
        paginated_solve_set = self.cut_last_solve(limit, own_solve_data, paginated_solve_set)
        data.update(pagination_info)  # adding pagination fields to response
        paginated_solve_set_with_solves = self.add_places(paginated_solve_set)

        results['own_solve'] = own_solve
        results['solve_set'] = paginated_solve_set_with_solves
        data['results'] = results

        return data

    def _get_pagination_info(self, queryset, limit, page):
        total_items = queryset.count()
        total_pages = math.ceil(total_items / limit)

        info = {
            'limit': limit,
            'page': page,
            'pages': total_pages,
        }

        return info

    def _get_paginated_data(self, queryset, limit, page):
        start = (page - 1) * limit
        end = page * limit

        return queryset[start:end]


class ContestLeaderboardSelector:
    def get_place(self, round_session, contest, discipline):
        position = RoundSessionModel.objects.filter(
            avg_ms__lt=round_session.avg_ms,
            contest=contest,
            discipline=discipline
        ).count() + 1
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

    def get_page(self, limit, round_session, contest, discipline):
        place = self.get_place(round_session, contest, discipline)
        page = math.ceil(place / limit)
        return page

    def is_displayed_separately(self, own_round_session, round_session_set):
        if own_round_session in round_session_set:
            return False
        elif own_round_session is None:
            return False
        elif own_round_session not in round_session_set:
            return True

    def round_session_list(self, discipline, contest):
        round_session_set = RoundSessionModel.objects.filter(
            discipline=discipline,
            contest=contest
        ).order_by('avg_ms')
        return round_session_set

    def cut_last_round_session(self, round_session_set, ):

    def round_session_set_retrieve(self, discipline, contest, limit, page, user_id):
        round_session_set = RoundSessionModel.objects.filter(
            discipline=discipline,
            contest=contest,
        ).order_by('avg_ms')
        paginated_round_session_set = self._get_paginated_data(round_session_set, limit, page)
        paginated_round_session_set_with_places = self.add_places(
            paginated_round_session_set,
            contest,
            discipline,
        )
        cutted_paginated_round_session_set_with_places = self.cut_
        return paginated_round_session_set_with_places

    def own_round_session_retrieve(self, discipline, contest, limit, page, user_id):
        round_session = RoundSessionModel.objects.first()
        round_session_set = RoundSessionModel.objects.filter(
            discipline=discipline,
            contest=contest,
        )
        paginated_round_session_set = self._get_paginated_data(round_session_set, limit, page)
        is_displayed_separately = self.is_displayed_separately(round_session, paginated_round_session_set)
        own_round_session = {
            'round_session': round_session,
            'place': self.get_place(round_session, contest, discipline),
            'is_displayed_separately': is_displayed_separately,
            'page': self.get_page(limit, round_session, contest, discipline)
        }
        return own_round_session

    def get_pagination_info(self, discipline, contest, limit, page):
        queryset = self.round_session_list(discipline, contest)
        total_items = queryset.count()
        total_pages = math.ceil(total_items / limit)

        info = {
            'limit': limit,
            'page': page,
            'pages': total_pages,
        }

        return info

    def leaderboard_retrieve(self, discipline_slug, contest_slug, limit, page, user_id):
        contest = ContestModel.objects.get(slug=contest_slug)
        discipline = DisciplineModel.objects.get(slug=discipline_slug)
        data = {'results': {}}
        data.update(self.get_pagination_info(discipline, contest, limit, page))
        data['results']['own_round_session'] = self.own_round_session_retrieve(discipline, contest, limit, page,
                                                                               user_id)
        data['results']['round_session_set'] = self.round_session_set_retrieve(discipline, contest, limit, page, user_id)
        print(data)
        return data

    def _get_paginated_data(self, queryset, limit, page):
        start = (page - 1) * limit
        end = page * limit

        return queryset[start:end]
