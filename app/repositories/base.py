from abc import ABC, abstractmethod
from fastapi import Depends
from sqlalchemy import desc, or_, and_
from sqlalchemy.orm import Session

from config import NOT_FILTER_FIELDS
from database import get_db_session


class BaseRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_session)) -> None:
        self.db = db

    def create(self, item):
        self.db.add(item)
        self.db.commit()
        return item

    def update(self, item):
        self.db.merge(item)
        self.db.commit()
        return item

    def delete(self, item):
        self.db.delete(item)
        self.db.commit()
        return "Delete this item successfully"

    # Apply sort filter search

    def paginate(self, query, params):
        if params["paginate"] != "all":
            return query.offset((params["page"]-1)*int(params["paginate"])).limit(int(params["paginate"]))
        return query

    def sort(self, query, model, params):
        if params["order"] == "desc":
            return query.order_by(desc(getattr(model, params["sort"])))
        return query.order_by(getattr(model, params["sort"]))

    def search(self, query, model, params):
        if params['search']['value'] is None:
            return query
        search_args = [params['search']['value'] == getattr(model, field)
                       for field in params['search']['fields']]
        return query.filter(or_(*search_args))

    def filter(self, query, model, params):
        filters_args = [params[key] == getattr(
            model, key) for key in params if key not in NOT_FILTER_FIELDS and params[key] is not None]
        return query.filter(and_(*filters_args))


class InterfaceRepository(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def show(self, id):
        pass

    @abstractmethod
    def create(self, item):
        pass

    @abstractmethod
    def update(self, item):
        pass

    @abstractmethod
    def delete(self, item):
        pass

    @abstractmethod
    def paginate(self, query, params):
        pass
