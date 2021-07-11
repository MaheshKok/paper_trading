from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from extensions import db
from models.future import Future
from schema.future import FutureSchema


class FutureList(ResourceList):
    def query(self, view_kwargs):
        query_ = self.session.query(Future)
        if view_kwargs.get("id") is not None:
            try:
                self.session.query(Future).filter_by(id=view_kwargs["id"]).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"},
                    "Person: {} not found".format(view_kwargs["id"]),
                )
            else:
                query_ = query_.join(Future).filter(Future.id == view_kwargs["id"])
        return query_

    def before_create_object(self, data, view_kwargs):
        if view_kwargs.get("id") is not None:
            person = self.session.query(Future).filter_by(id=view_kwargs["id"]).one()
            data["person_id"] = person.id

    schema = FutureSchema
    data_layer = {
        "session": db.session,
        "model": Future,
        "methods": {
            "query": query,
        },
    }


class FutureDetail(ResourceDetail):
    schema = FutureSchema
    data_layer = {
        "session": db.session,
        "model": Future,
    }
