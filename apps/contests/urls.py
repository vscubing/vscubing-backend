from django.urls import include, path

from .apis import (
    SolveListApi,
    SolveRetrieveApi,
    SolveCreateApi,
    SolveSubmitApi,
    SolveListBestInDisciplineList,
    SolveListBestOfEveryUser,
    RoundSessionWithSolvesListApi,
    RoundSessionProgresStateApi,
    ContestListApi,
)

solves_urlpatterns = [
    path('', SolveListApi.as_view(), name='list'),
    path('retrieve/<int:pk>/', SolveRetrieveApi.as_view(), name='retrieve'),
    path('create/', SolveCreateApi.as_view(), name='create'),
    path('submit/<int:pk>/', SolveSubmitApi.as_view(), name='submit'),
    path('best-in-discipline/', SolveListBestInDisciplineList.as_view(), name='list-best-in-discipline'),
    path('best-of-every-user/', SolveListBestOfEveryUser.as_view(), name='list-best-of-every-user'),
]

contests_urlpatterns = [
    path('', ContestListApi.as_view(), name='list'),
]

round_session_urlpatterns = [
    path('with-solves', RoundSessionWithSolvesListApi.as_view(), name='list-with-nested-solves'),
    path('list-best-of-every-user', RoundSessionProgresStateApi.as_view(), name='list-best-of-every-user'),
]

urlpatterns = [
    path('solves/', include(solves_urlpatterns)),
    path('contests/', include(contests_urlpatterns)),
    path('round-sessions', include(round_session_urlpatterns)),
]
