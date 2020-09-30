from flask_neo4j_lite.config import NeoConfig
from py2neo import Graph, NodeMatcher, RelationshipMatcher


NeoConfig.graph = Graph(password="neo4JPassword", port="11005")
NeoConfig.matcher = NodeMatcher(NeoConfig.graph)
NeoConfig.relationship_matcher = RelationshipMatcher(NeoConfig.graph)


from py2neo.ogm import (Property, RelatedTo, RelatedFrom)
from flask_neo4j_lite.manager import Neo4JManager
from flask_neo4j_lite.config import models


class Movie(Neo4JManager):
    __primarykey__ = "title"

    title = Property()
    tagline = Property()

    actors = RelatedFrom("Person", "ACTED_IN")


class Person(Neo4JManager):
    __primarykey__ = "name"

    name = Property()
    acted_in = RelatedTo(Movie, "ACTED_IN")


models['Movie'] = Movie
models['Person'] = Person
