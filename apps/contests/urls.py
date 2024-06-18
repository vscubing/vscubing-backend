from django.urls import include, path

from .apis import (
    SolveRetrieveApi,
    SolveCreateApi,
    SolveSubmitApi,
    SolveListBestInEveryDiscipline,
    SingleResultLeaderboardApi,
    ContestLeaderboardApi,
    # RoundSessionCurrentWithSolvesRetrieveApi,
    # RoundSessionRetrieveApi,
    ContestListApi,
    CurrentRoundSessionProgressApi,
    OngoingContestRetrieveApi,
)

solves_urlpatterns = [
    path('<int:pk>/retrieve/', SolveRetrieveApi.as_view(), name='retrieve'),
    path('single-result-leaderboard', SingleResultLeaderboardApi.as_view(), name='list'),
    path('best-in-every-discipline/', SolveListBestInEveryDiscipline.as_view(), name='list-best-in-every-discipline'),
]

ongoing_contest_urlpatterns = [
    path('current-round-session-progress/', CurrentRoundSessionProgressApi.as_view(), name='retrieve-current'),
    path('retrieve/', OngoingContestRetrieveApi.as_view(), name='retrieve'),
    path('solve/create/', SolveCreateApi.as_view(), name='solve-create'),
    # path('submit/<int:pk>/', SolveSubmitApi.as_view(), name='submit'),
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

urlpatterns = [
    path('solves/', include(solves_urlpatterns)),
    path('contests/', include(contests_urlpatterns)),
    path('round-sessions/', include(round_session_urlpatterns)),
    path('ongoing-contest/', include(ongoing_contest_urlpatterns)),
]
