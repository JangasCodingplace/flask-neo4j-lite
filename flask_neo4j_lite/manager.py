from py2neo.ogm import GraphObject, RelatedObjects
from .config import models, NeoConfig
from . import exceptions


class RelationshipManager(NeoConfig):
    @classmethod
    def get_relationship(cls, start_node=None, end_node=None, r_type=None,
                         *args, **kwargs):
        """
        Returns a single Relationship.
        In case of multiple Matches & not found relationships an error raises

        Properties:
            start_node: Node (not GraphObject), default: None
                        Startnode of relationship.
                        If None: Any Node can be start node
            end_node: Node (not GraphObject), default: None
                      Endnode of relationship
                      If None: Any Node can be end node
            r_type: string, default: None
                    Type of relationship
                    If None: Any relationsship

        Return
            Relationship
        """
        rel = cls.relationship_matcher.match(nodes=[start_node, end_node],
                                             r_type=r_type, **kwargs)
        if not rel.exists():
            raise exceptions.RelationshipMatchError(
                "No Relationship with given properties exists"
            )
        if rel.count() > 1:
            raise exceptions.RelationshipMatchError(
                "To many Relationship Matches"
            )
        return rel.first()

    @classmethod
    def delete(cls, start_obj=None, end_obj=None, r_type=None,
               *args, **kwargs):
        """
        Delete single Relationship by given properties.
        Raise an Error by no existing relationship or multiple relationships.

        Properties:
            start_node: GraphObject, default: None
                        Startnode of relationship.
                        If None: Any Node can be start node
            end_node: GraphObject, default: None
                      Endnode of relationship
                      If None: Any Node can be end node
            r_type: string, default: None
                    Type of relationship
                    If None: Any relationsship
        """
        start_node = None if start_obj is None else start_obj.node
        end_node = None if end_obj is None else end_obj.node

        relationship = cls.get_relationship(start_node=start_node,
                                            end_node=end_node,
                                            r_type=r_type, **kwargs)
        cls.graph.separate(relationship)

    @classmethod
    def delete_all(cls, start_obj=None, end_obj=None, r_type=None,
                   *args, **kwargs):
        """
        Delete multiple Relationships by given properties.

        Properties:
            start_node: GraphObject, default: None
                        Startnode of relationship.
                        If None: Any Node can be start node
            end_node: GraphObject, default: None
                      Endnode of relationship
                      If None: Any Node can be end node
            r_type: string, default: None
                    Type of relationship
                    If None: Any relationsship
        """
        start_node = None if start_obj is None else start_obj.node
        end_node = None if end_obj is None else end_obj.node
        rels = cls.relationship_matcher.match(nodes=[start_node, end_node],
                                              r_type=r_type, **kwargs)

        for rel in rels.all():
            cls.graph.separate(rel)


class Neo4JManager(GraphObject, NeoConfig):
    node = None

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Create Node and return instance.
        """
        obj = cls()
        for key, value in kwargs.items():
            # Check if instane is RelatedObject.
            if isinstance(obj.__getattribute__(key), RelatedObjects):
                # Set RelatedTo Relation To Model.
                rel = cls.get_related_node(attr=key, attr_value=value)
                if isinstance(rel, list):
                    for r in rel:
                        obj.__getattribute__(key).add(r)
                else:
                    obj.__getattribute__(key).add(rel)
            else:
                obj.__setattr__(key, value)
        cls.graph.push(obj)
        obj.node = obj.object_to_node()
        return obj

    @classmethod
    def filter_nodes(cls, *args, **kwargs):
        """
        Get Query for Nodes. Returns NodeMatcher.
        """
        props, rels = cls.split_property_from_relationships(*args, **kwargs)
        nodes = cls.matcher.match(cls.__name__, **props)
        return nodes

    @classmethod
    def filter_object(cls, *args, **kwargs):
        """
        Get Query for Nodes. Returns Object.
        """
        nodes = cls.filter_nodes(*args, **kwargs).all()
        instances = [cls.get_object_from_node(node) for node in nodes]
        return instances

    @classmethod
    def split_property_from_relationships(cls, *args, **kwargs):
        """
        Look into kwargs - split kwargs into Parameters and Relationship Attrs.
        Returns
            list of dictionaries
        """
        properties, relationships = {}, {}
        for key, value in kwargs.items():
            if isinstance(cls().__getattribute__(key), RelatedObjects):
                relationships[key] = value
            else:
                properties[key] = value
        return properties, relationships

    @classmethod
    def get_node(cls, *args, **kwargs):
        """
        Get Query for sigle Node.
        Raise Error if node not found or multiple nodes exist.

        Return:
            Node
        """
        nodes = cls.filter_nodes(*args, **kwargs)
        if nodes.first() is None:
            raise exceptions.DoesNotExist(
                f"Found no instance for {cls.__name__}"
            )
        if nodes.count() > 1:
            raise exceptions.ToManyMatchesError(
                "Found to many nodes."
            )
        return nodes.first()

    @classmethod
    def get_related_node(cls, attr, attr_value, *args, **kwargs):
        """
        Get Related Nodes of object.
        Can be query for just one Node or many nodes - depends on attr_value.

        Parameter:
            attr: string; related property name at class
            attr_value: any type || list of any types
                        Value(s) of related properties (should be primary key)

        Returns:
            RelatedNode || List of RelatedNodes
        """
        obj = cls()
        related_class_obj = obj.__getattribute__(attr).related_class
        model = related_class_obj.__primarylabel__
        model_pk = related_class_obj.__primarykey__
        relatet_cls = models[model]

        if isinstance(attr_value, list):
            rels = []
            for rel in attr_value:
                rels.append(relatet_cls.get_object(**{model_pk: rel}))
            return rels

        rel = relatet_cls.get_object(**{model_pk: attr_value})
        return rel

    @classmethod
    def get_object(cls, *args, **kwargs):
        """
        Get single instance of Node.
        Raise Errors in case of multiple nodes or if node not exists.

        Returns:
            Object
            Class of Node
        """
        props, rels = cls.split_property_from_relationships(*args, **kwargs)
        node = cls.get_node(**props)
        instance = cls.get_object_from_node(node)
        for key, value in rels.items():
            rel = cls.get_related_node(attr=key, attr_value=value)
            if isinstance(rel, list):
                for r in rel:
                    instance.__getattribute__(key).add(r)
            else:
                instance.__getattribute__(key).add(rel)
        instance.node = instance.object_to_node()
        return instance

    @classmethod
    def get_or_create_object(cls, *args, **kwargs):
        """
        Returns an object if exists.
        Create an object if its not exists.

        Returns:
            Object
            Class instance of Node
        """
        try:
            instance = cls.get_object(*args, **kwargs)
        except exceptions.DoesNotExist:
            instance = cls.create(*args, **kwargs)
        return instance

    @classmethod
    def get_object_from_node(cls, node):
        """
        Convert node to object.

        Parameter:
            node: Node object; Should be the node which should be transformed.

        Returns:
            Object
            Class instance of node
        """
        obj = cls()
        for key, value in cls.__dict__.items():
            if not key.startswith('__') and key in node:
                obj.__setattr__(key, node[key])
        return obj

    def object_to_node(self):
        """
        Convert given Object to Node

        Returns:
            Node
        """
        pk = self.__primarykey__
        pk_value = self.__getattribute__(pk)
        identifier = {**{pk: pk_value}}
        node = self.get_node(**identifier)
        return node

    def save(self):
        """
        Save an existing object.
        Object should have exists already befor save.
        Use create if you want to create a new node.
        """
        self.graph.push(self)

    def delete_hard(self):
        """
        Delete given object and all relations.
        """
        self.graph.delete(self.node)

    def delete(self):
        """
        Delete given object if no Nodes are related to this.
        """
        node = self.node
        relationships = self.relationship_matcher.match([None, node])
        if relationships.exists():
            raise exceptions.DeletionError(
                "Can't delete a Node where other nodes are Relating to. "
                "Use `delete_hard` instead or fix it different."
            )
        self.graph.delete(node)

    @classmethod
    def delete_if_exist(cls, *args, **kwargs):
        """
        Delete a Node if exist. This is a soft deletion.
        If there are any Relations to that node, deletion will throw an Err.
        """
        try:
            node = cls.get_node(*args, **kwargs)
            node.delete()
        except exceptions.DoesNotExist:
            pass
