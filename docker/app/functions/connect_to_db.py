import pymysql

class SQLcommand:
  conn = pymysql.connect(
    host = 'db',
    database = 'chi101',
    user = 'chi101',
    password = 'chi101',
    charset = 'utf8mb4'
  )

  def get(self, sql: str) -> tuple:
    with self.conn.cursor() as cursor:
      cursor.execute(sql)
      data = cursor.fetchall()
    return data
  
  def modify(self, sql: str) -> None:
    with self.conn.cursor() as cursor:
      cursor.execute(sql)
    self.conn.commit()

  def modify_tuple(self, sql: str, values: tuple) -> None:
    with self.conn.cursor() as cursor:
      cursor.execute(sql, values)
    self.conn.commit()

if __name__ == '__main__':
  pass