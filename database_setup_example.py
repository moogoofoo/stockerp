


"""
Example usage of database utilities for setting up databases and tables.

This file demonstrates how to use the new database utilities for:
1. Creating the database if it doesn't exist
2. Creating tables with different names
3. Handling the full setup process
"""

import sys
import os

# Add core to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from core.database_utils import (
    create_database_if_not_exists,
    create_table_if_not_exists,
    setup_database_and_table,
    create_stock_data_table,
    create_all_default_tables,
    check_database_connectivity
)

def main():
    """Demonstrate database utilities usage"""
    
    print("🔧 Database Utilities Demo for stockerp")
    print("=" * 50)
    
    # 1. Check database connectivity
    print("\n1. Testing database connectivity...")
    connected, msg = check_database_connectivity()
    print(f"   {msg}")
    
    if connected:
        print("\n2. Setting up default database and table...")
        # 2. Setup database and default table
        results = create_all_default_tables()
        
        for table_type, (created, message) in results.items():
            print(f"   📊 {table_type}: {'✓' if created else '→'} {message}")
        
        print("\n3. Demonstrating custom table creation...")
        # 3. Create custom tables
        custom_tables = [
            'portfolio_1_stock_data',
            'backup_stock_data',
            'test_env_data'
        ]
        
        for table_name in custom_tables:
            result = create_stock_data_table(table_name)
            print(f"   🏗️  {table_name}: {'✓' if result[0] else '→'} {result[1]}")
        
        print("\n4. Listing all tables...")
        # 4. List all tables (requires db connection)
        from core.database import get_engine
        engine = get_engine()
        
        with engine.connect() as conn:
            result = conn.execute(
                """
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = DATABASE()
                """
            )
            tables = [row[0] for row in result.fetchall()]
            print(f"   📋 Available tables: {', '.join(tables)}")
    
    else:
        print("\n❌ Database connection failed. Please check your configuration.")
        print("\nTo setup database manually:")
        print("   python core/database_utils.py --setup-defaults")
    
    print("\n🎉 Database utilities demo complete!")

if __name__ == "__main__":
    main()


