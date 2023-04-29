import pymysql

def sql_command(sql: str) -> tuple:
  conn = pymysql.connect(
    host = 'db',
    database = 'chi101',
    user = 'root',
    password = 'root',
    charset = 'utf8mb4'
  )

  with conn.cursor() as cursor:
    cursor.execute(sql)
    data = cursor.fetchall()
  return data
