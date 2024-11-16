from django.urls import include, path
from os import getenv

from .apis import (
    SolveRetrieveApi,
    CreateSolveApi,
    SubmitSolveApi,
    SolveListBestInEveryDiscipline,
    SingleResultLeaderboardApi,
    ContestLeaderboardApi,
    # RoundSessionCurrentWithSolvesRetrieveApi,
    # RoundSessionRetrieveApi,
    ContestListApi,
    CurrentRoundSessionProgressApi,
    OngoingContestRetrieveApi,
)
from .dev_apis import OwnRoundSessionDeleteApi, NewContestCreateApi

from dotenv import load_dotenv

load_dotenv()

solves_urlpatterns = [
    path('<int:pk>/retrieve/', SolveRetrieveApi.as_view(), name='retrieve'),
    path('single-result-leaderboard', SingleResultLeaderboardApi.as_view(), name='list'),
    path('best-in-every-discipline/', SolveListBestInEveryDiscipline.as_view(), name='list-best-in-every-discipline'),
]

ongoing_contest_urlpatterns = [
    path('current-round-session-progress/', CurrentRoundSessionProgressApi.as_view(), name='retrieve-current'),
    path('retrieve/', OngoingContestRetrieveApi.as_view(), name='retrieve'),
    path('solve/create/', CreateSolveApi.as_view(), name='solve-create'),
    path('<int:solve_id>/submit/', SubmitSolveApi.as_view(), name='submit'),
]

contests_urlpatterns = [
    path('', ContestListApi.as_view(), name='list'),
    path(
        'leaderboard/',
        ContestLeaderboardApi.as_view(),
        name='leaderboard'
    ),
]

round_session_urlpatterns = [
    # path(
    #     'with-solves/<int:user_id>/retrieve/',
    #     RoundSessionRetrieveApi.as_view(),
    #     name='retrieve-with-nested-solves'
    # ),
    # path(
    #     'current/',
    #     RoundSessionCurrentWithSolvesRetrieveApi.as_view(),
    #     name='retrieve-current'
    # ),
]

dev_urlpatterns = [
    path('own-round-session/delete/', OwnRoundSessionDeleteApi.as_view(), name='own-round-session-delete'),
    path('new-contest/create/', NewContestCreateApi.as_view(), name='new-contest-create')
]

urlpatterns = [
    path('solves/', include(solves_urlpatterns)),
    path('contests/', include(contests_urlpatterns)),
    path('round-sessions/', include(round_session_urlpatterns)),
    path('ongoing-contest/', include(ongoing_contest_urlpatterns)),
]

if getenv('RUN_MODE') == 'dev':
    urlpatterns.append(path('dev/', include(dev_urlpatterns)))
