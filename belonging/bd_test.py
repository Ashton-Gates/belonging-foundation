import pyodbc
conn_str = ('Driver={ODBC Driver 18 for SQL Server};'
            'Server=tcp:belonging-server.database.windows.net,1433;'
            'Database=belonging-prod-database;'
            'UID=belo-admin;'
            'PWD=H1ng3isgro$$;')
connection = pyodbc.connect(conn_str)
print("Connected successfully")
