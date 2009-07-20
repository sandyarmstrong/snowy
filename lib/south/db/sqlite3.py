
from django.db import connection
from south.db import generic

class DatabaseOperations(generic.DatabaseOperations):

    """
    SQLite3 implementation of database operations.
    """

    # SQLite ignores foreign key constraints. I wish I could.
    supports_foreign_keys = False
    
    # You can't add UNIQUE columns with an ALTER TABLE.
    def add_column(self, table_name, name, field, *args, **kwds):
        # Run ALTER TABLE with no unique column
        unique, field._unique, field.db_index = field.unique, False, False
        # If it's not nullable, and has no default, raise an error (SQLite is picky)
        if not field.null and (not field.has_default() or field.get_default() is None):
            raise ValueError("You cannot add a null=False column without a default value.")
        generic.DatabaseOperations.add_column(self, table_name, name, field, *args, **kwds)
        # If it _was_ unique, make an index on it.
        if unique:
            self.create_index(table_name, [name], unique=True)
    
    # SQLite doesn't have ALTER COLUMN
    def alter_column(self, table_name, name, field, explicit_name=True):
        """
        Not supported under SQLite.
        """
        raise NotImplementedError("SQLite does not support altering columns.")
    
    # Nor DROP COLUMN
    def delete_column(self, table_name, name):
        """
        Not supported under SQLite.
        """
        raise NotImplementedError("SQLite does not support deleting columns.")
    
    # Nor RENAME COLUMN
    def rename_column(self, table_name, old, new):
        """
        Not supported under SQLite.
        """
        raise NotImplementedError("SQLite does not support renaming columns.")
    
    # No cascades on deletes
    def delete_table(self, table_name, cascade=True):
        generic.DatabaseOperations.delete_table(self, table_name, False)
    