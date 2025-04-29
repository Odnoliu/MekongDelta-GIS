import psycopg2

def connection():
    try:
        connection = psycopg2.connect(
            dbname="NLN_WEB-GIS-FLASK&VUE",  
            user="postgres",         
            password="12345",     
            host="localhost",              
            port="5432"               
        )
        return connection
    except Exception as e:
        return str(e)
    