from py2neo import Graph, NodeMatcher, RelationshipMatcher


class NeoConfig:
    graph = Graph(password="neo4JPassword", port="11005")
    matcher = NodeMatcher(graph)
    relationship_matcher = RelationshipMatcher(graph)
