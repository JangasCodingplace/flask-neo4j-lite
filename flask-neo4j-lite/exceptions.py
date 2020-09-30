class FieldTypeError(Exception):
    """Value has wrong datatype"""
    pass


class ToManyMatchesError(Exception):
    """Found multiple Nodes instead of one."""
    pass


class DoesNotExist(Exception):
    """Object Does not exist."""
    pass


class RelationshipMatchError(Exception):
    """Err with Relationships."""
    pass


class DeletionError(Exception):
    """Err by deleting an instance"""
