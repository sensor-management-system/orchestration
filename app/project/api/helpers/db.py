import logging

from ..models.base_model import db


def save_to_db(item):
    """Wrap a safe way to save an item to session
    :param item: will be saved to database
    :return boolean: True if success.
    """
    try:
        logging.info("Trying to add item to session")
        db.session.add(item)
        logging.info("added to session")
        db.session.commit()
        logging.info("Done!")
        return True
    except Exception as e:
        logging.exception("DB Exception!")
        logging.exception(repr(e))
        db.session.rollback()
        return False
