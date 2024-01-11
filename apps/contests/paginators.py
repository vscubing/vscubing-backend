

def solve_paginator(queryset, params):
    page_number = int(params.get('page', 1))
    page_size = int(params.get('page_size', 20))
    start = (page_number - 1) * page_size
    end = start + page_size
    queryset = queryset[start:end]

    return queryset
