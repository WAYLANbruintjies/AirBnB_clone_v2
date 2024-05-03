#!/usr/bin/python3
"""New engine DBStorage"""
from sqlalchemy.orm import sessionmaker, scoped_session
from create import create_engine
from os import getenv
from models.base_model import Base, BaseModel
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models.review import Review


class DBStorage():
    """
    Class containing private class attributes
    """
    __engine = None
    __sessions = None

    def __init__(self): 
        """Public instance methods"""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')

        database_url = "mysql+mysqldb://{}:{}@{}/()".format(user, password, host, database)

        self.__engine = create_engine(database_url, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self. __engine)

    def all(self, cls=None):
        """
        Query current database session(self.__session) all objects depending of the cls
        If cls=None, query all types of objects

        Return: dictionary
        """
        obj_list = []
        if cls:
            if isinstance(cls, str):
                try:
                    cls = globals()[cls]
                except KeyError:
                    pass
            if issubclass(cls, Base):
                obj_list = self.__session.query(cls).all()
            else:
                for subclass in Base.__subclasses__():
                   obj_list.extend(self.__session.query(subclass).all())
            obj_dict = {}
            for obj in obj_list:
                key = "{}:{}".format(obj.__class__.__name__, obj.id)
                try:
                    if obj.__class__.__name__ == 'State':
                        del obj._sa_instance_state
                        obj_dict[key] = obj
                    else:
                        obj_dict[key] = obj
                except Exception:
                    pass
            return obj_dict

    def new(self, obj):
        """Add the object to the current database session (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session (self.__session)"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database,
        Create the current database session (self.__session) from the engine (self.__engine)
        by using a sessionmaker with option (expire_on_commit) set to false
        
        Scoped_session - to make sure your Session is thread-safe
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
