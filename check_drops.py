import pymysql

conn = pymysql.connect(host='192.168.0.102', port=3306, user='techpath', password='sanjeev123', database='techpath_pods_dev')
try:
    with conn.cursor() as cursor:
        cursor.execute("SHOW BINLOG EVENTS IN 'binlog.000091'")
        rows = cursor.fetchall()
        
        drops = [row for row in rows if 'DROP TABLE' in str(row[5])]
        print(f"Found {len(drops)} DROP TABLE events.")
        for d in drops:
            print(d[5])
finally:
    conn.close()
