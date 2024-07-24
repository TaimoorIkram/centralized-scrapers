from datetime import datetime
import sqlite3

"""
- This module is to be used only as a standalone. The purpose of this
    module is to execute some query on the db.sqlite3 file to change records.

- Take caution while using this file. It is to be used only for testing 
    purposes and not to be altered in production. 
"""

db_conn = sqlite3.connect('db.sqlite3')
db_conn.execute(f"UPDATE scraper_deadlines SET deadline = ? WHERE market_name = 'daraz'", (datetime.now(), ))
db_conn.commit()