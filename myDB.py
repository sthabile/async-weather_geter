def create_table(db, sql_query):
    try:
        cur = db.cursor()
        cur.execute(sql_query)
    except Exception as e:
        print(e)
        db.rollback()


def insert(db, weather_data):  # weather_data is an array
    insert_qry = "insert into City_Weather_Data (City_Name, Cloud, temperature,wind_speed,humidity,country) " \
                 "values(?,?,?,?,?,?); "
    try:
        cur = db.cursor()
        cur.execute(insert_qry, weather_data)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


def selectAllRows(db, table_name):
    query = "SELECT * from " + table_name
    try:
        cur = db.cursor()
        cur.execute(query)
        table = cur.fetchall()
        return table
    except Exception as e:
        print(e)


def delete_table(db, table_name):
    query = "DROP TABLE " + table_name
    try:
        cur = db.cursor()
        cur.execute(query)
    except Exception as e:
        print(e)