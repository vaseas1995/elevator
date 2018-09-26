import mysql.connector
class ConnectionError(Exception):
    pass
class CredentialsError(Exception):
    pass
class SQLError(Exception):
    pass

class UseDatabase:
    def __init__(self, config: dict) -> None:
        self.configuration = config
    try:    
        def __enter__(self) ->'cursor':
            self.conn = mysql.connector.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
    except mysql.connector.errors.InterfaceError as err:
        raise ConnectionError(err)
    except mysql.connector.errors.ProgrammingErrors as err:
        raise CredentialsError(err)
    def __exit__(self, exc_type, exc_value, exctrace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if ext_type is mysql.connector.errors.ProgrammingError:
            raise SQLError(exc_value)
        elif exc_tipe:
            raise exc_type(exc_value)
