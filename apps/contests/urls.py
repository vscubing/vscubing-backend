from django.urls import path, include

from .views import (
    # ViewSets
    ContestViewSet,
    DisciplineViewSet,
    SolveViewSet,
    RoundSessionViewSet,
    ScrambleViewSet,

    # Apis
    SolveListApi,
    SolveCreateApi,
    SolveRetrieveApi,
    SolveSubmitApi,
    SolveListBestOfEveryUserApi,
    SolveListBestsInDisciplinesApi,
)


from rest_framework import routers

router = routers.SimpleRouter()
# router.register(r'contests', ContestViewSet, basename='contest')
# router.register(r'disciplines', DisciplineViewSet, basename='discipline')
# router.register(r'rounds_sessions', RoundSessionViewSet, basename='round_session')
# router.register(r'scrambles', ScrambleViewSet, basename='scramble')
urlpatterns = router.urls

solve_urlpatterns = [
    path('', SolveListApi.as_view(), name='list'),
    path('<int:pk>/', SolveRetrieveApi.as_view(), name='detail'),
    path('create/', SolveCreateApi.as_view(), name='create'),
    path('submit/', SolveSubmitApi.as_view(), name='submit'),
    path('list-every-user-best', SolveListBestOfEveryUserApi.as_view(), name='list-best-of-every-user'),
    path('list-bests-in-disciplines', SolveListBestsInDisciplinesApi.as_view(), name='list-bests-in-disciplines'),
]

urlpatterns += [
    path('solves/', include((solve_urlpatterns, 'solves'))),
]
