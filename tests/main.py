from py2neo.ogm import (GraphObject, Property, RelatedTo, RelatedFrom)
from manager import Neo4JManager
from config import NeoConfig
from settings import graph, matcher, relationship_matcher, models

"""
**********

To DO:
    - Write Test Cases

**********
"""


class Movie(NeoConfig, GraphObject, Neo4JManager):
    __primarykey__ = "title"

    title = Property()
    tagline = Property()

    actors = RelatedFrom("Person", "ACTED_IN")


class Person(NeoConfig, GraphObject, Neo4JManager):
    __primarykey__ = "name"

    name = Property()
    acted_in = RelatedTo(Movie, "ACTED_IN")


models['Movie'] = Movie
models['Person'] = Person


person = Person.get_object(name="Luke Skywalker", acted_in="Star Wars")
print("")
# movie = Movie.get_object(title="Star Wars")

# end_node2 = Movie.get_object(title="Bachelor")

# RelationshipManager.delete_all(start_node=start_node,
#                                r_type="ACTED_IN")

# Movie.create(title="Star Wars")
# Person.create(name="Chewie", acted_in="Star Wars")
# Person.create(name="Leia", acted_in="Star Wars")
