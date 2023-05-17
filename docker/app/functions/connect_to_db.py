import pymysql

class SQLcommand:
  def __init__(self):
    self.conn = pymysql.connect(
      host='db',
      database='chi101',
      user='chi101',
      password='chi101',
      charset='utf8mb4'
    )

  def get(self, sql: str) -> list:
    with self.conn.cursor() as cursor:
      cursor.execute(sql)
      data = cursor.fetchall()
    return list(data)
  
  def modify(self, sql: str) -> None:
    with self.conn.cursor() as cursor:
      cursor.execute(sql)
    self.conn.commit()

if __name__ == '__main__':
  pass
