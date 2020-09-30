from py2neo.ogm import (GraphObject, Property, RelatedTo, RelatedFrom)
from flask_neo4j_lite.manager import Neo4JManager
from flask_neo4j_lite.config import models
from .config import NeoConfig


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
