from sqlalchemy import MetaData
# A collection of metadata entities is stored in an object aptly named MetaData:
"""
MetaData is a container object that keeps together many different features of a database (or multiple databases) being described.

To represent a table, use the Table class. 
Its two primary arguments are the table name, then the MetaData object which it will be associated with. 
The remaining positional arguments are mostly Column objects describing each column:
"""

metadata = MetaData()