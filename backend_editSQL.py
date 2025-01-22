import traceback
import json
import re
from sql_metadata import Parser
from model import db
from model import connect
from general_functions import General_functions
from request_sql import RequestSQL


class Editing_SQL():
    '''Редактирование базы SQL.'''
    def __init__(self):
        self.dop_function = General_functions()
        self.query = RequestSQL()

    def editing_sql(self, table: str):
        '''Сбор данных для построения(столбцы, значения ячеек)'''
        try:
            eng_name_column, fetchall = self.column_names(table)

            dict_rus = self.exist_check_array(self.read_json(), table)
            rus_eng_name = self.russian_name_column(dict_rus, eng_name_column)

            count_column = self.exist_check_int(self.read_json(), table)

            value = fetchall
            return len(eng_name_column), len(value), rus_eng_name, value, count_column
        except Exception:
            return 0, 0, 0, 0, 0

    def read_json(self) -> tuple:
        '''Русификация шапки таблицы из файла .json.'''
        with open(connect.path_rus_text, "r", encoding='utf-8') as outfile:
            return json.load(outfile)

    def russian_name_column(self, dict_rus, name_column):
        '''Расшифровка с английского на русский.'''
        return [dict_rus[eng_t] if eng_t in dict_rus.keys() else eng_t for eng_t in name_column]

    def exist_check_array(self, array: dict, table: str):
        '''Проверка на существование данных столбцов из файла.'''
        try:
            return array[table]
        except Exception:
            return {}

    def exist_check_int(self, array: dict, table: str):
        '''Проверка на существование данных для
          видимости столбцов левой таблицы в params_visible_column.'''
        try:
            value = array['params_visible_column']
            return value[table]
        except Exception:
            return 4

    def search_name(self, table: str, value):
        '''Поиск подписи к ячейке.'''
        try:
            isdigit_num = re.findall('\d+', str(value))
            fetchone = self.query.where_id_select(table,
                                                  "name",
                                                  int(isdigit_num[0]))
            return fetchone[0]
        except Exception:
            return ''

    def column_names(self, table: str):
        '''Собираем название колонок.'''
        description, fetchall = self.query.all_select_table(table)
        return next(zip(*description)), fetchall

    def apply_request_select(self, request, table_used: str, logging):
        '''Обраблотка запроса от пользователя.'''
        def column_table(table: str, query_column):
            if query_column[0] == '*':
                column_used, fetchall = self.column_names(table)
            else:
                column_used = ', '.join(query_column)
            return column_used

        try:
            cursor = db.cursor()
            cursor.execute(f'''{request}''')
            value = cursor.fetchall()

            query_table = Parser(f'''{request}''').tables
            query_column = Parser(f'''{request}''').columns
            name_column = next(zip(*cursor.description))

            table_used = query_table[0]

            dict_rus = self.exist_check_array(self.read_json(), table_used)
            rus_eng_name = self.russian_name_column(dict_rus, column_table(table_used, query_column))

            c_col = self.exist_check_int(self.read_json(), table_used)

            count_column = len(name_column)
            count_row = len(value)
            return table_used, count_column, count_row, rus_eng_name, value, c_col
        except Exception:
            logging.logs_msg(f'Таблица: {table_used} некорректный запрос: {traceback.format_exc()}', 2)
            return 'error', 'error', 'error', 'error', 'error', 'error'

    def update_row_tabl(self, column: int, text_cell: str, text_cell_id: int,
                        table: str, hat_name: list, logging):
        """Обновление строки.
        Args:
            column (int): номер столбца
            text_cell (str): значение ячейки
            text_cell_id (int): номер ячейки изменения
            table_used (str): таблица изменения
            hat_name (list): описание столбцов
            logging (_type_): логирование
        """
        active_column = list(hat_name)[column]
        try:
            change_value = "NULL" if text_cell is None or text_cell == '' else f'{text_cell}'
            self.query.update_row(table, active_column,
                                  text_cell_id, change_value)
            return
        except Exception:
            logging.logs_msg(f'Таблица: {table}, ошибка при изменении ячейки: {traceback.format_exc()}', 2)
            return

    def add_new_row(self, table: str, row: int):
        '''Добавление новой строки.'''
        self.query.new_row(table, row)

    def delete_row(self, text_cell_id: str, table: str):
        '''Удаление выбранной строки.'''
        self.query.delete_row(text_cell_id, table)

    def clear_tabl(self, table: str):
        '''Очистка таблицы.'''
        self.query.clear_table(table)

    def drop_tabl(self, table: str):
        '''Удаление таблицы.'''
        self.query.delete_table(table)

    def type_column(self, table: str, logging):
        '''Собираем тип столбцов, и названия на рус и англ.'''
        type_list = []
        try:
            inf_data = self.query.information_schema(table)
            dict_rus = self.exist_check_array(self.read_json(), table)

            for i in inf_data:
                column_name = i[0]
                data_type = i[1]
                try:
                    list_a = [column_name,  dict_rus[column_name], data_type]
                except Exception:
                    list_a = [column_name,  '', data_type]
                type_list.append(list_a)
        except Exception:
            logging.logs_msg(f'Окно тип данных: ошибка: {traceback.format_exc()}', 2)

        return type_list

    def dop_window_signal(self, table: str):
        type_list = []
        try:
            if table == 'ktpra':
                column = '"id", "variable", "name"'
            else:
                column = '"id", "tag", "name"'
            data = self.query.not_all_select_table(table, column)
            for i in data:
                id_ = i[0]
                tag = i[1]
                name = i[2]

                list_a = [id_, tag, name]
                type_list.append(list_a)
            msg = ' Таблица открыта '
            color = '#6bdb84'
        except Exception:
            msg = ' Для типа сигнала нет таблицы '
            color = 'yellow'

        return type_list, msg, color

    def filter_text(self, text, list_signal):
        '''Поиск сигналов в окне ссылки.'''
        list_request = []
        for i in list_signal:
            id_ = i[0]
            tag = i[1]
            name = i[2]

            if self.dop_function.str_find(str(name).lower(), {text}):
                list_temp = [id_, tag, name]
                list_request.append(list_temp)
        return list_request