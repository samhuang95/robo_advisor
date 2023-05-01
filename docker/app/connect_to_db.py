import pymysql

def sql_command(sql: str) -> tuple:
  conn = pymysql.connect(
    host = 'db',
    database = 'chi101',
    user = 'chi101',
    password = 'chi101',
    charset = 'utf8mb4'
  )

  with conn.cursor() as cursor:
    cursor.execute(sql)
    data = cursor.fetchall()
  return data
