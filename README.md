# ETL_RETAIL_TRX
ETL pipeline for Lion Parcel retail transactions (using dummy data): reads CSV source data, transforms it, and loads into MySQL data warehouse. Supports hourly automation and soft delete for historical tracking.

## Folder
    ETL_RETAIL_TRX/
    ├─ .venv/                  # Virtual environment with Python and libraries
    ├─ database_retail.csv     # Source CSV data → user can update anytime
    ├─ etl_retail.py           # Python ETL script → Read CSV, transform, insert/update MySQL, handle soft delete
    ├─ etl_retail.bat          # Batch file to run ETL
    ├─ etl_retail_log.txt      # File log for ETL execution


## Requirements
1. Python 3.x
2. Libraries (installed in .venv): pandas mysql-connector-python
3. MySQL server running with database and table setup:

        CREATE DATABASE IF NOT EXISTS dw_retail;
         USE dw_retail;
         CREATE TABLE IF NOT EXISTS dw_retail_trx (
           id INT PRIMARY KEY,
           customer_id INT NOT NULL,
           last_status VARCHAR(50) NOT NULL,
           pos_origin VARCHAR(50),
           pos_destination VARCHAR(50),
           created_at DATETIME,
           updated_at DATETIME,
           deleted_at DATETIME
           );
## Config 
           MYSQL_CONFIG = {
           'host': 'localhost',
           'user': 'root',              # username
           'password': 'your_pass',     # CHANGE password
           'database': 'dw_retail'
           }
           TABLE_NAME = 'dw_retail_trx'
           
           CSV_FILE = r"Z:\ETL_RETAIL_TRX\database_retail.csv"  #  path CSV
           LOG_FILE = r"Z:\ETL_RETAIL_TRX\etl_retail_log.txt"   #  path TXT

## Automatic Run via Task Scheduler
1. Open Task Scheduler → Create Task
2. General tab → Name: 'anything you want'
3. Trigger tab → New :
   - Begin the task: On a schedule → Daily
   - Repeat task every: 1 hour
   - Duration: Indefinitely
4. Action tab → New:
   - Action: Start a program
   - Program/script: browse etl_retail.bat (ex. : Z:\ETL_RETAIL_TRX\etl_retail.bat)
5. Save → ETL runs automatically every hour

## Notes
- Ensure MySQL server is running before executing ETL and DONT FORGET TO FILL YOUR PASSWORD on .py script
- Verify any paths in script and .bat file correspond to your folder structure
- Task Scheduler ensures hourly automated ETL runs
- Log file etl_retail_log.txt records all success and error messages

## Result Checking on MySQL
Do :
SELECT * FROM dw_retail_trx;
    
