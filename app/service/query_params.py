from .base import BaseService


class QueryParamsService(BaseService):

    def transform_query_params(self, params):
        params = self.transform_default_query_params(params)
        # params = self.transform_filter_query_params(params)
        params = self.transform_search_query_params(params)
        return self.transform_null_query_values(params)

    def transform_default_query_params(self, params):
        params.sort = params.get_sort_field(params.sort)
        params.order = params.get_order_value(params.order)
        params.paginate = params.get_paginate_value(params.paginate)
        params.page = params.get_page_value(params.page)
        return params

    # def transform_filter_query_params(self, params):
    #     return self.get_filter_query_values(
    #         params, params.get_filter_fields())

    def transform_search_query_params(self, params):
        value = params.search if params.search != "" and params.search != None else None
        params.search = {
            "fields": params.get_search_fields(),
            "value": value
        }
        return params

    def transform_null_query_values(self, params):
        params = dict(params)
        for key in params:
            params[key] = self.get_null_query_value(params[key])
        return params

    def get_null_query_value(self, value):
        if value is None or value == "":
            return None
        return value

    # def get_filter_query_values(self, params, fields):
    #     for field in fields:
    #         values = getattr(params, field)
    #         if values != "" and values != None:
    #             setattr(params, field, values.split(" "))
    #     return params
