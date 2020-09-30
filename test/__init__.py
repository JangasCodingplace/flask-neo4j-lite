from flask_neo4j_lite.config import NeoConfig
from py2neo import Graph, NodeMatcher, RelationshipMatcher


NeoConfig.graph = Graph(password="neo4JPassword", port="11005")
NeoConfig.matcher = NodeMatcher(NeoConfig.graph)
NeoConfig.relationship_matcher = RelationshipMatcher(NeoConfig.graph)