from django.urls import include, path

from .apis import (
    SolveListApi,
)

solve_urlpatterns = [
    path('', SolveListApi.as_view(), name='list'),
    # path('retrieve')
]


urlpatterns = [
    path('solves/', include(solve_urlpatterns))
]
