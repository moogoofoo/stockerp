
"""
Database and table creation utilities for stockerp application.

This module provides functions to:
1. Create the database if it doesn't exist
2. Create specific tables if they don't exist
3. Handle utility operations for database administration
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from mysql.connector import errorcode
import mysql.connector
import pymysql
from core.pickle_models import PickledStockData

from config import (
    DB_USER, 
    DB_PASSWORD, 
    DB_HOST, 
    DB_PORT, 
    DB_NAME,
    DATABASE_URI
)

# Remove the database name for connection to create databases
BASE_URI = DATABASE_URI.rsplit('/', 1)[0]

def create_database_if_not_exists(database_name=None):
    """
    Create the MySQL database if it doesn't exist.
    
    Args:
        database_name (str): Name of database to create. 
                           Uses DB_NAME from config if None.
    
    Returns:
        bool: True if database was created, False if already exists
        str: Status message
    """
    if database_name is None:
        database_name = DB_NAME
    
    try:
        # Connect to MySQL server without specifying database
        connection = create_engine(BASE_URI)
        
        with connection.connect() as conn:
            # Check if database exists
            result = conn.execute(
                text("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = :db_name"),
                {"db_name": database_name}
            )
            
            if not result.fetchone():
                # Create the database
                conn.execute(text(f"CREATE DATABASE `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                conn.commit()
                return True, f"Database '{database_name}' created successfully"
            else:
                return False, f"Database '{database_name}' already exists"
                
    except SQLAlchemyError as e:
        error_msg = str(e)
        if "Can't connect" in error_msg:
            return False, f"Cannot connect to MySQL server: {error_msg}"
        elif "Access denied" in error_msg:
            return False, f"Access denied for user {DB_USER}: {error_msg}"
        else:
            return False, f"Error creating database: {error_msg}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def create_table_if_not_exists(table_name, model_class=None, table_schema=None):
    """
    Create a specific table if it doesn't exist.
    
    Args:
        table_name (str): Name of the table to create
        model_class (class, optional): SQLAlchemy model class. 
                                     If provided, uses model.create_all()
        table_schema (dict, optional): Custom table schema as a mapping
    
    Returns:
        bool: True if table was created, False if already exists or error
        str: Status message
    """
    from core.database import get_engine
    
    try:
        engine = get_engine()
        
        # Check if table exists
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = :db_name AND TABLE_NAME = :table_name
                """),
                {"db_name": DB_NAME, "table_name": table_name}
            )
            
            if result.fetchone():
                return False, f"Table '{table_name}' already exists in database '{DB_NAME}'"
        
        # Create table using model if provided
        if model_class:
            from sqlalchemy import MetaData
            model_class.metadata.create_all(bind=engine, tables=[model_class.__table__])
            return True, f"Table '{table_name}' created successfully using model class"
        
        elif table_schema:
            # Create custom table from schema
            with engine.connect() as conn:
                columns = []
                for col_name, col_type in table_schema.items():
                    columns.append(f"`{col_name}` {col_type}")
                
                create_sql = f"""
                CREATE TABLE IF NOT EXISTS `{table_name}` (
                    {', '.join(columns)}
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """
                
                conn.execute(text(create_sql))
                conn.commit()
                return True, f"Table '{table_name}' created successfully with custom schema"
        else:
            return False, "No model class or schema provided for table creation"
            
    except SQLAlchemyError as e:
        return False, f"Error creating table '{table_name}': {str(e)}"
    except Exception as e:
        return False, f"Unexpected error creating table: {str(e)}"

def setup_database_and_table(table_name, model_class=None, table_schema=None):
    """
    Combined function to set up database and table in one call.
    
    Args:
        table_name (str): Name of table to create
        model_class (class, optional): SQLAlchemy model
        table_schema (dict, optional): Custom table schema
    
    Returns:
        dict: Results of database and table creation attempts
    """
    results = {"database": None, "table": None}
    
    # Try to create database
    db_created, db_msg = create_database_if_not_exists()
    results["database"] = {"created": db_created, "message": db_msg}
    
    # Try to create table
    table_created, table_msg = create_table_if_not_exists(table_name, model_class, table_schema)
    results["table"] = {"created": table_created, "message": table_msg}
    
    return results

def check_database_connectivity():
    """
    Test database connectivity.
    
    Returns:
        bool: True if connection successful
        str: Status message
    """
    try:
        from core.database import get_engine
        engine = get_engine()
        
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            return True, "Database connectivity check successful"
    except Exception as e:
        return False, f"Database connectivity failed: {str(e)}"

# Convenience functions for common table creation
def create_stock_data_table(table_name='pickled_stock_data'):
    """Create the stock data table using the default model"""
    return create_table_if_not_exists(table_name, PickledStockData)

def create_all_default_tables():
    """Create all default system tables"""
    results = {}
    
    # Create stock data table
    result = create_stock_data_table()
    results['stock_data'] = result
    
    return results

# Used for CLI execution
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database utilities for stockerp")
    parser.add_argument(
        "--setup-defaults",
        action="store_true",
        help="Setup database and all default tables"
    )
    parser.add_argument(
        "--create-table",
        type=str,
        help="Create a specific table"
    )
    parser.add_argument(
        "--check-connection",
        action="store_true",
        help="Test database connectivity"
    )
    
    args = parser.parse_args()
    
    if args.setup_defaults:
        print("Setting up database and default tables...")
        results = setup_database_and_table('pickled_stock_data', PickledStockData)
        print("Database setup results:")
        print(f"  Database: {results['database']['message']}")
        print(f"  Table: {results['table']['message']}")
    
    elif args.create_table:
        print(f"Creating table: {args.create_table}")
        result = create_stock_data_table(args.create_table)
        print(result[1])
    
    elif args.check_connection:
        connected, msg = check_database_connectivity()
        print(msg)
    
    else:
        print("Database utilities for stockerp")
        print("Usage:")
        print("  python core/database_utils.py --setup-defaults")
        print("  python core/database_utils.py --create-table <table_name>")
        print("  python core/database_utils.py --check-connection")

