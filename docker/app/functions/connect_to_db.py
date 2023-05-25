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

# if __name__ == '__main__':
#   start = '2023-05-01'
#   end = '2023-05-23'
#   data = SQLcommand().get(f'SELECT date, shop_name AS name, rating_counts AS rating FROM offical_data WHERE date >= "{start}" AND date <= "{end}"')
#   print(data)