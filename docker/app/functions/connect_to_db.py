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
  SQLcommand().modify("""
    UPDATE products_info
    SET shop_name = CASE
        WHEN shop_id = '3045968' THEN '開心農元'
        WHEN shop_id = '7432754' THEN '小李植栽'
        WHEN shop_id = '369371665' THEN '糀町植葉'
        WHEN shop_id = '268986085' THEN '南犬植栽'
        WHEN shop_id = '161364427' THEN '沐時園藝'
        WHEN shop_id = '15227497' THEN '珍奇植物'
        WHEN shop_id = '4877504' THEN '麗都花園'
        WHEN shop_id = '145300134' THEN '宅栽工作室'
        ELSE shop_name
    END;
""")