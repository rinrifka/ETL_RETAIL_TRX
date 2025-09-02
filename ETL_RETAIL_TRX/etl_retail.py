import pandas as pd
import mysql.connector
from datetime import datetime
import logging
import os

# Config
CSV_FILE = r"Z:\ETL_RETAIL_TRX\database_retail.csv"  # Ganti sesuai path CSV
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',              # username bawaan
    'password': 'your_pass',     # GANTI password
    'database': 'dw_retail'  
}
TABLE_NAME = 'dw_retail_trx'

# Setup log
LOG_FILE = r"Z:\ETL_RETAIL_TRX\etl_retail_log.txt" 

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

try :
    # Connect to MySQL
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    # Read CSV
    df = pd.read_csv(CSV_FILE, sep=';')

    # Datetime columns
    for col in ['created_at', 'updated_at', 'deleted_at']:
        df[col] = pd.to_datetime(df[col], format='%d/%m/%Y %H:%M', errors='coerce')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # ETL process
    for _, row in df.iterrows():
        receipt_id = row['id']
    
        # Check if row exists
        cursor.execute(f"SELECT id, last_status, created_at FROM {TABLE_NAME} WHERE id = %s", (receipt_id,))
        result = cursor.fetchone()
    
        # Create timestamps
        created_at = row['created_at'].strftime('%Y-%m-%d %H:%M:%S') if pd.notna(row['created_at']) else now
        updated_at = row['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if pd.notna(row['updated_at']) else now
        deleted_at = row['deleted_at'].strftime('%Y-%m-%d %H:%M:%S') if pd.notna(row['deleted_at']) else (now if row['last_status']=='DELIVERED' else None)
    
        #update
        if result:
            cursor.execute(f"""
                UPDATE {TABLE_NAME}
                SET customer_id=%s,
                    last_status=%s,
                    pos_origin=%s,
                    pos_destination=%s,
                    updated_at=%s,
                    deleted_at=%s
                WHERE id=%s
            """, (row['customer_id'], row['last_status'], row['pos_origin'], row['pos_destination'],
                updated_at, deleted_at, receipt_id))
        else:
            cursor.execute(f"""
                INSERT INTO {TABLE_NAME} 
                (id, customer_id, last_status, pos_origin, pos_destination, created_at, updated_at, deleted_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (receipt_id, row['customer_id'], row['last_status'], row['pos_origin'], row['pos_destination'],
                created_at, updated_at, deleted_at))

    conn.commit()
    cursor.close()
    conn.close()

# log info
    logging.info("ETL completed successfully")
except Exception as e:
    logging.error(f"ETL failed: {str(e)}")


print("ETL completed successfully at", datetime.now())