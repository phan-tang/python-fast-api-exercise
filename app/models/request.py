from pydantic import BaseModel, Field
from typing import Optional

from config import DEFAULT_PAGINATE, DEFAULT_SORT, DEFAULT_ORDER


class BaseQueryRequest(BaseModel):
    sort: Optional[str] = Field(default="id")
    order: Optional[str] = Field(default="asc")
    paginate: Optional[str] = Field(default='10')
    page: Optional[str] = Field(default='1')
    search: Optional[str] = Field()

    def get_sort_field(self, field: str):
        if field not in self.get_sort_fields() or field == '':
            return DEFAULT_SORT["default_value"]
        return field

    def get_order_value(self, value: str):
        if value not in self.get_order_values() or value == '':
            return DEFAULT_ORDER["default_value"]
        return value

    def get_paginate_value(self, value: str):
        if value.isnumeric() or value == 'all':
            return value
        return DEFAULT_PAGINATE["default_value"]

    def get_page_value(self, value: str):
        if value != None and value.isnumeric():
            return int(value)
        return 1

    def get_order_values(self):
        return DEFAULT_ORDER["values"]

    def get_sort_fields(self):
        return DEFAULT_SORT["values"]

    def get_filter_fields(self):
        return []

    def get_search_fields(self):
        return []
