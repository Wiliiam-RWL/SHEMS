from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config import Config

class Database:
    # Creating an SQLAlchemy engine with connection pool settings
    engine = create_engine(Config.DATABASE_URI, pool_size=10, max_overflow=20)

    # Using scoped_session to ensure thread safety
    db_session = scoped_session(sessionmaker(bind=engine))

    @staticmethod
    def execute_query(query, params=None):
        """
        Executes a SQL query.

        :param query: SQL query string
        :param params: Parameters for the query
        :return: The result of the query execution
        """
        if params is None:
            params = {}
        result = Database.db_session.execute(query, params)
        Database.db_session.commit()
        return result

    @staticmethod
    def init_db():
        """
        Initializes the database, such as creating tables if necessary.
        """
        # Place database initialization code here, if needed
        pass

    @staticmethod
    def close_session():
        """
        Closes the current database session.
        """
        Database.db_session.remove()
