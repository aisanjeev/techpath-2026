import pymysql

def drop_all_tables():
    conn = pymysql.connect(host='192.168.0.102', port=3306, user='techpath', password='sanjeev123', database='techpath_pods_dev')
    try:
        with conn.cursor() as cursor:
            # Disable foreign key checks to allow dropping tables with dependencies
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            
            # Fetch all tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                print(f"Dropping table {table_name}...")
                cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
                
            # Re-enable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            conn.commit()
            print("All tables dropped successfully.")
    except Exception as e:
        print(f"Error dropping tables: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    drop_all_tables()
