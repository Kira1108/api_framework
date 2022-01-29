import sqlite3
import pytest
import os

from bumbo.orm import Database, Column, Table, ForeignKey

@pytest.fixture
def Author():
    """Test create a class Author table class
    """
    class Author(Table):
        name = Column(str)
        age = Column(int)
        
    return Author

@pytest.fixture
def db():
    DB_PATH = "./test.db"
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    db = Database(DB_PATH)
    return db

@pytest.fixture
def Book(Author):
    """Test create a Book table class"""
    class Book(Table):
        title = Column(str)
        published = Column(bool)
        author = ForeignKey(Author)
    return Book


def test_create_db(db):
    """Test create database"""
    db = Database("./test.db")
    
    assert isinstance(db.conn, sqlite3.Connection)
    assert db.tables == []
    

def test_define_tables(Author, Book):
    """Test table attributes."""
    assert Author.name.type == str
    assert Book.author.table == Author
    assert Author.name.sql_type =="TEXT"
    assert Author.age.sql_type == "INTEGER"
    
    
def test_create_tables(Author, Book):
    if os.path.exists("./test.db"):
        os.remove("./test.db")
        
    db = Database("./test.db")
    db.create(Author)
    db.create(Book)
    
    assert Author._get_create_sql() == "CREATE TABLE IF NOT EXISTS author (id INTEGER PRIMARY KEY AUTOINCREMENT, age INTEGER, name TEXT);"
    assert Book._get_create_sql() == "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY AUTOINCREMENT, author_id INTEGER, published INTEGER, title TEXT);"
    
    for table in ("author",'book'):
        assert table in db.tables
    