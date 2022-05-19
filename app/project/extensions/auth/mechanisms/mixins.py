from ....api.models import User, Contact
from ....api.models.base_model import db


class CreateNewUserByUserinfoMixin:
    """
    Mixin to create new users if we need to do so.

    As we rely on the data that we get from the idp, we
    create new users in case there is the very first request.
    If we find existing ones, we can go on with those.
    """
    @staticmethod
    def get_user_or_create_new(identity, attributes):

        # We check if we find a user for this identity entry.
        found_user = db.session.query(User).filter_by(subject=identity).one_or_none()
        if found_user:
            return found_user

        # We haven't found any user with the subject.
        # But as we rely on the IDP, we will insert it in the database.
        # However, every user gets a contact.
        # Do we have one already?
        email = attributes["email"]
        contact = db.session.query(Contact).filter_by(email=email).one_or_none()
        if contact:
            if not contact.active:
                contact.given_name=attributes["given_name"]
                contact.familiy_name=attributes["familiy_name"]
                contact.active = True
                db.session.add(contact)
        if not contact:
            contact = Contact(
                given_name=attributes["given_name"],
                family_name=attributes["family_name"],
                email=attributes["email"],
            )
            db.session.add(contact)
        user = User(subject=identity, contact=contact)
        db.session.add(user)
        db.session.commit()
        return user
