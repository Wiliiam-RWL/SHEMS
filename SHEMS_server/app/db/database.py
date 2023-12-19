from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config import Config

class Database:
    # Creating an SQLAlchemy engine with connection pool settings
    engine = create_engine(Config.DATABASE_URI, pool_size=10, max_overflow=20)

    # Using scoped_session to ensure thread safety
    db_session = scoped_session(sessionmaker(bind=engine))

    @staticmethod
    def begin_transaction():
        """
        Begins a new transaction.
        """
        return Database.db_session.begin_nested()

    @staticmethod
    def commit_transaction():
        """
        Commits the current transaction.
        """
        Database.db_session.commit()

    @staticmethod
    def rollback_transaction():
        """
        Rolls back the current transaction.
        """
        Database.db_session.rollback()

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
        return result

    @staticmethod
    def handle_transaction(queries_params):
        """
        Execute a series of queries as transaction

        If successful, commit
        If failed, rollback

        :param queries_params: {'query': the query to be execute, 'params': the parameters}
        """
        try:
            transaction = Database.begin_transaction()
            for qp in queries_params:
                Database.execute_query(qp["query"], qp["params"])
            Database.commit_transaction()
            return True
        except Exception as e:
            print(e)
            Database.rollback_transaction()
            return False

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

    