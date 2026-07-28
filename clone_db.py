from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import urllib.parse
import sys

def clone_db():
    print("Starting database clone process...")
    # Fix the password if needed for the connection strings
    source_url = "mysql+pymysql://sanjeev:newLimited%401998@82.29.161.183:3306/techpath_web_dev"
    dest_url = "mysql+pymysql://techpath:sanjeev123@192.168.0.102:3306/techpath_pods_dev"
    
    try:
        source_engine = create_engine(source_url)
        dest_engine = create_engine(dest_url)
        
        meta = MetaData()
        print("Reflecting source database schema...")
        meta.reflect(bind=source_engine)
        
        print("Creating tables in destination database...")
        meta.drop_all(bind=dest_engine) # Ensure it's clean if there's any partial state
        meta.create_all(bind=dest_engine)
        
        print("Starting data transfer...")
        with source_engine.connect() as src_conn:
            with dest_engine.connect() as dest_conn:
                for table in meta.sorted_tables:
                    print(f"Copying data for table: {table.name}")
                    result = src_conn.execute(table.select())
                    data = [dict(row._mapping) for row in result]
                    if data:
                        # Batch insert if data is large
                        batch_size = 1000
                        for i in range(0, len(data), batch_size):
                            batch = data[i:i+batch_size]
                            dest_conn.execute(table.insert(), batch)
                        dest_conn.commit()
                        print(f"  -> Copied {len(data)} rows.")
                    else:
                        print(f"  -> Table is empty.")
                        
        print("Clone completed successfully!")
    except Exception as e:
        print(f"Error during cloning: {e}")
        sys.exit(1)

if __name__ == '__main__':
    clone_db()
