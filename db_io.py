from sqlalchemy import create_engine

def db_connect():
    """
    Connect to a local sqlite DB and return the connection
    """
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    return engine


if __name__ == '__main__':
    pass
