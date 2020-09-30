from .setup.models import Movie, Person
from py2neo.ogm import RelatedObjects


class TestBasic:
    """
    Test Cases expected functional get node Feature
    """
    def test_create_node_without_relation(self):
        person = Person.create(name="Test1")
        assert person.name == "Test1"

        person_node = Person.get_node(name="Test1")
        assert person_node == person.node

        person.delete()

    def test_create_node_with_relation(self):
        movie = Movie.create(title="TestM")
        person = Person.create(name="Test1", acted_in="TestM")
        assert person.name == "Test1"
        assert isinstance(person.acted_in, RelatedObjects)
        person.delete()
        movie.delete_hard()

    def test_get_node_without_relation(self):
        Person.create(name="Test1")
        person = Person.get_object(name="Test1")
        assert person.name == "Test1"

        person_node = Person.get_node(name="Test1")
        assert person_node == person.node
        person.delete()

    def test_get_node_with_relation(self):
        movie = Movie.create(title="TestM")
        Person.create(name="Test1", acted_in="TestM")
        person = Person.get_object(name="Test1", acted_in="TestM")
        assert person.name == "Test1"
        assert isinstance(person.acted_in, RelatedObjects)
        person.delete()
        movie.delete_hard()

    def test_get_or_create_create(self):
        person = Person.get_or_create_object(name="Test1")
        assert person.name == "Test1"
        person.delete()

    def test_get_or_create_get(self):
        Person.create(name="Test1")
        person = Person.get_or_create_object(name="Test1")
        assert person.name == "Test1"
        person.delete()

    def test_update_node(self):
        person = Person.get_or_create_object(name="Test1")
        person.name = "UpdatedName"
        person.save()
        person = Person.get_or_create_object(name="UpdatedName")
        assert person.name == "UpdatedName"
        person.delete()
