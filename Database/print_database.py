from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base


def print_database():
    engine = create_engine('postgresql://postgres:pokemon@localhost:5432/Pokemon')
    inspector = inspect(engine)

    schemas = inspector.get_schema_names()
    for schema in schemas:
        # information_schema: base schema object that hold parent Sql tables, that all tables are derived from
        if schema != "information_schema":
            print(f"schema: {schema}")
            for table_name in inspector.get_table_names(schema=schema):
                print(f"table name: {table_name}")
                for column in inspector.get_columns(table_name, schema=schema):
                    print(f"Column: {column}")


if __name__ == "__main__":
    print_database()
