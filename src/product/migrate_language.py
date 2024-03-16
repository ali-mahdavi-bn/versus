from inspect import getmembers, isclass

from product.domain import language
from product.domain.entities import Language


def migrate_language(session_maker=None):
    with session_maker() as session:
        for p, c in getmembers(language, isclass):
            if members := c.members():
                for member in members:
                    try:
                        session.add(language_factory(name=member.name, language_id=member.value))
                        session.commit()
                    except Exception:
                        session.rollback()


def language_factory(name=None, language_id=None):
    language: Language = Language()
    language.name = name
    language.id = language_id

    return language
