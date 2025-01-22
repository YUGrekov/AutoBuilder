from model import db


class RequestSQL():
    '''Отдельный класс с запросами к БД.'''
    def __init__(self):
        self.cursor = db.cursor()

    def information_schema(self, table: str):
        '''Получаем тип столбцов таблицы.'''
        self.cursor.execute(f"""SELECT column_name, data_type
                                FROM information_schema.columns
                                WHERE table_schema = 'public' AND
                                      table_name = '{table}'""")
        return self.cursor.fetchall()

    def where_select(self, table: str,
                     column: str, condit: int, order):
        '''Запрос на выборку данных с условием и сортировкой.'''
        self.cursor.execute(f"""SELECT {column}
                                FROM "{table}"
                                WHERE ({condit})
                                ORDER BY "{order}" """)
        return self.cursor.fetchall()

    def where_id_select(self, table: str, column: str, value_id: int):
        '''Запрос на выборку данных с условием по id.'''
        self.cursor.execute(f"""SELECT "{column}"
                                FROM "{table}"
                                WHERE id = {value_id}""")
        return self.cursor.fetchone()

    def all_select_table(self, table: str):
        '''Запрос на получение полных данных о
        таблице сортированные по столбцу id.'''
        self.cursor.execute(f'SELECT * FROM "{table}" ORDER BY id')
        return self.cursor.description, self.cursor.fetchall()

    def not_all_select_table(self, table: str, column):
        '''Запрос на получение частичных данных о
        таблице сортированные по столбцу id.'''
        self.cursor.execute(f'''SELECT {column}
                                FROM "{table}"
                                ORDER BY id''')
        return self.cursor.fetchall()

    def update_row(self, table: str, column, id_cell, change_value):
        '''Запрос на обновление ячейки строки.'''
        if change_value == 'NULL':
            string = f'SET "{column}"= NULL'
        else:
            string = f'''SET "{column}"= '{change_value}' '''

        self.cursor.execute(f"""UPDATE "{table}"
                                {string}
                                WHERE id={id_cell}""")

    def new_row(self, table: str, row: int):
        '''Запрос на добавление новой строки.'''
        self.cursor.execute(f'''INSERT INTO "{table}" (id)
                                VALUES ({row});''')

    def delete_row(self, id_cell: str, table: str):
        '''Запрос на удаление выбранной строки.'''
        self.cursor.execute(f'''DELETE FROM "{table}"
                                WHERE id={id_cell}''')

    def delete_table(self, table: str):
        '''Запрос на удаление таблицы.'''
        self.cursor.execute(f'DROP TABLE "{table}"')

    def clear_table(self, table: str):
        '''Запрос на очистку таблицы.'''
        self.cursor.execute(f'DELETE FROM "{table}"')

    def new_table(self, models):
        '''Создание новой таблицы по модели.'''
        with db.atomic():
            db.create_tables([models])

    def get_tabl(self):
        '''Сбор таблиц базы'''
        return db.get_tables()

    def max_value_column(self, table: str, column: str):
        '''Нахождение максимального знач-ния в столбце.'''
        self.cursor.execute(f'''SELECT MAX("{column}")
                                FROM "{table.lower()}"''')
        return self.cursor.fetchall()[0][0]

    def max_value_column_cond(self, table: str,
                              column: str, *condition):
        '''Нахождение максимального знач-ния в столбце с условием.'''
        self.cursor.execute(f'''SELECT MAX("{column}")
                                FROM "{table.lower()}"
                                WHERE "{condition[0]}"={condition[1]}''')
        return self.cursor.fetchall()[0][0]

    def select_orm(self, models, where, order):
        '''Запрос Select через ORM.'''
        query = models.select().where(where).order_by(order)
        return query.execute()

    def non_repea_names(self, models, dist, order):
        '''Нахождение неповторяющихся сигналов в таблице.'''
        query = models.select().order_by(order).distinct(dist)
        return query.execute()

    def non_repea_cond(self, models, dist, where, order):
        '''Нахождение неповторяющихся по условию сигналов в таблице.'''
        query = models.select().distinct(dist).where(where).order_by(order)
        return query.execute()

    def write_base_orm(self, data: dict, models):
        '''Запись в базу через ORM peewee.'''
        models.insert_many(data).execute()

    def update_base_orm(self, models, update, where):
        '''Обновление записей базы через ORM peewee.'''
        models.update(update).where(where).execute()

    def count_row_orm(self, models):
        '''Количество строк.'''
        return models.select().count()

    def check_table(self, table: str):
        '''Проверка на существование таблицы в БД.'''
        all_tables = self.get_tabl()
        return True if table in all_tables else False

    def check_row_table(self, table: str):
        '''Проверка наличия строк таблицы в БД.'''
        try:
            if self.max_value_column(table, 'id') > 0:
                return True
            else:
                return False
        except Exception:
            return False

    def new_table_orm(self, table: str):
        '''Добавление новой таблицы.'''
        db.create_tables([table])