import pymysql

class SQLCommand:
  conn = pymysql.connect(
    host = 'db',
    database = 'chi101',
    user = 'root',
    password = 'root',
    charset = 'utf8mb4'
  )
  cursor = conn.cursor()

  def get(self, sql: str) -> tuple:
    self.cursor.execute(sql)
    data = self.cursor.fetchall()
    return data

  def modify(self, sql: str) -> None:
    self.cursor.execute(sql)
    self.conn.commit()
