import sqlite3
import inspect

class Database:
    """
    A database has many tables.
    A database is responsible for creating the tables.
    """
    def __init__(self, path):
        self.conn = sqlite3.Connection(path)
        
    @property
    def tables(self):
        SELECT_TABLES_SQL = "SELECT name FROM sqlite_master WHERE type = 'table';"
        return [x[0] for x in self.conn.execute(SELECT_TABLES_SQL).fetchall()]
    
    
    def create(self, table):
        self.conn.execute(table._get_create_sql())


class Table:
    """Table is responsible for create table in database
    which is ,generate sql then execute the sql
    
    A table has many columns (class variable)
    And a class method, create sql
    Instance method is define in subclass, CRUD operations.
    """
    
    @classmethod
    def _get_create_sql(cls):
        CREATE_TABLE_SQL = """CREATE TABLE IF NOT EXISTS {name} ({fields});"""
        fields = [
            "id INTEGER PRIMARY KEY AUTOINCREMENT"
        ]
        
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(f"{name} {field.sql_type}")
            elif isinstance(field, ForeignKey):
                fields.append(f"{name}_id INTEGER")
                
        fields = ", ".join(fields)
        name = cls.__name__.lower()
        return CREATE_TABLE_SQL.format(name = name, fields =  fields)

class Column:
    """
        A column has a column type.
        which should map to database filed types
    """
    def __init__(self, column_type):
        self.type = column_type
    
    @property
    def sql_type(self):
        SQLITE_TYPE_MAP = {
            int: "INTEGER",
            float: "REAL",
            str: "TEXT",
            bytes: "BLOB",
            bool: "INTEGER",  # 0 or 1
        }
        
        return SQLITE_TYPE_MAP[self.type]

class ForeignKey:
    def __init__(self, table):
        self.table = table
        
    