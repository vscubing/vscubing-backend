from rest_framework.exceptions import APIException


def solve_paginator(queryset, params):
    # TODO add limit
    try:
        page_number = int(params.get('page', 1))
        page_size = int(params.get('page_size', 20))
    except ValueError:
        APIException.default_detail = "Invalid page or page_size value. These should be integers."
        APIException.status_code = 400
        raise APIException

    start = (page_number - 1) * page_size
    end = start + page_size
    queryset = queryset[start:end]

    return queryset
