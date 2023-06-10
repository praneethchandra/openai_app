
from flask import abort, make_response
from config import db
from models import Person, people_schema, person_schema, PersonSchema
"""
From Part1: 
# from datetime import datetime
"""

""" From Part1:
# def get_timestamp():
#     return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
"""

""" From Part1:
PEOPLE= {
    "Fairy": {
        "fname": "Tooth",
        "lname": "Fairy",
        "timestamp": get_timestamp(),
    },
    "Ruprecht": {
        "fname": "Knecht",
        "lname": "Ruprecht",
        "timestamp": get_timestamp(),
    },
    "Bunny": {
        "fname": "Easter",
        "lname": "Bunny",
        "timestamp": get_timestamp(),
    }
}
"""


def read_all():
    """ From Part1:
    return list(PEOPLE.values())
    """
    people = Person.query.all()
    person_schema = PersonSchema(many=True)
    return person_schema.dump(people)

def create(person):
    """ From Part1:
    lname = person.get("lname")
    fname = person.get("fname", "")

    if lname and lname not in PEOPLE:
        PEOPLE[lname] = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp()
        }
        return PEOPLE[lname], 201
    else:
        abort(
            406,
            f"Person with last name {lname} already exists",
        )
    """
    lname = person.get("lname")
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()
    if existing_person is None:
        new_person = person_schema.load(person, session=db.session)
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person), 201
    else:
        abort(406, f"Person with last name {lname} already exists")

def read_one(lname):
    """ From Part1:
    if lname in PEOPLE:
        return PEOPLE[lname]
    else:
        abort(
            404, f"Person with last name {lname} not found"
        )
    """
    person = Person.query.filter(Person.lname == lname).one_or_more()
    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404, f"Person with last name {lname} not found")


def update(lname, person):
    """ From Part1:
    if lname in PEOPLE:
        PEOPLE[lname]["fname"] = person.get("fname", PEOPLE[lname]["fname"])
        PEOPLE[lname]["timestamp"] = get_timestamp()
        return PEOPLE[lname]
    else:
        abort(
            404,
            f"Person with last name {lname} not found"
        )
    """
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        db.session.merge(existing_person)
        db.session.commit()
        return person_schema.dump(existing_person), 201
    else:
        abort(404, f"Person with last name {lname} not found")

def delete(lname):
    """ From Part1:
    if lname in PEOPLE:
        del PEOPLE[lname]
        return make_response(
            f"{lname} successfully deleted", 200
        )
    else:
        abort(
            404,
            f"Person with last name {lname} not found"
        )
    """
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()
        return make_response(f"{lname} successfully deleted", 200)
    else:
        abort(404, f"Person with last name {lname} not found")
