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
    CurrentSolveApi,
    SubmittedSolvesApi,
    OngoingContestRetrieveApi,
)

solves_urlpatterns = [
    path('<int:pk>/retrieve/', SolveRetrieveApi.as_view(), name='retrieve'),
    path('single-result-leaderboard', SingleResultLeaderboardApi.as_view(), name='list'),
    # path('create/', SolveCreateApi.as_view(), name='create'),
    # path('submit/<int:pk>/', SolveSubmitApi.as_view(), name='submit'),
    path('best-in-every-discipline/', SolveListBestInEveryDiscipline.as_view(), name='list-best-in-every-discipline'),
]

ongoing_contest_urlpatterns = [
    # path('submitted-solves/', SubmittedSolvesApi.as_view(), name='list-submitted'),
    path('current-solve/', CurrentSolveApi.as_view(), name='retrieve-current'),
    path('retrieve/', OngoingContestRetrieveApi.as_view(), name='retrieve')
]

contests_urlpatterns = [
    path('', ContestListApi.as_view(), name='list'),
    path(
        '<str:contest_slug>/leaderboard/',
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
