from flask_jwt_extended import get_jwt_identity
from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.api.models.user import User


def add_create_by_id(data):
    """
    Use jwt to add user id to dataset
    :param data:
    :param args:
    :param kwargs:
    :return:
    """
    current_user = get_jwt_identity()
    u = db.session.query(User).filter_by(subject=current_user).first()
    data["created_by_id"] = u.id


def add_contact_to_object(d):
    u = db.session.query(User).filter_by(id=d.created_by_id).first()
    contact_id = u.contact_id
    c = db.session.query(Contact).filter_by(id=contact_id).first()
    d.contacts.append(c)
    db.session.add(d)
    db.session.commit()
