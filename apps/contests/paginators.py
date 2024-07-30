import math
from collections import OrderedDict

from django.http import Http404
from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.core.exceptions import NotFoundException


class LimitOffsetPagination(_LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

    def get_paginated_data(self, data):
        return OrderedDict([
            ('limit', self.limit),
            ('offset', self.offset),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])

    def get_paginated_response(self, data):
        """
        We redefine this method in order to return `limit` and `offset`.
        This is used by the frontend to construct the pagination itself.
        """
        return Response(OrderedDict([
            ('limit', self.limit),
            ('offset', self.offset),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class LimitPagePagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_data(self, data):
        self.page_size = int(self.request.query_params.get('page_size'))
        """
        We redefine this method in order to return `limit` and `page`.
        This is used by the frontend to construct the pagination itself.
        """
        return OrderedDict([
            ('page_size', self.page_size),
            ('page', self.page.number),
            ('count', self.page.paginator.count),
            ('pages', math.ceil(self.page.paginator.count / self.page_size)),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])



def get_paginated_response(*, pagination_class, serializer_class, queryset, request, view):
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)

    return Response(data=serializer.data)


def get_paginated_data(*, pagination_class, queryset, request, view):
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        return paginator.get_paginated_data(page)

    return page


def page_size_page_paginator(queryset, page_size, page):
    total_items = queryset.count()
    total_pages = math.ceil(total_items / page_size)
    if total_pages < page:
        raise NotFoundException('Invalid Page')

    start = (page - 1) * page_size
    end = page * page_size
    paginated_queryset = queryset[start:end]

    return paginated_queryset
