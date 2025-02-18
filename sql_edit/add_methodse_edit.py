import traceback
import json


class Editing_SQL():
    def __init__(self, active_table):
        self.table = active_table

    def read_json(self, path_rus_text) -> tuple:
        '''Русификация шапки таблицы из файла .json.'''
        with open(path_rus_text, "r", encoding='utf-8') as outfile:
            return json.load(outfile)

    def exist_check_array(self, array: dict, table: str):
        '''Проверка на существование данных столбцов из файла.'''
        try:
            return array[table]
        except Exception:
            return {}

    def editing_sql(self, eng_name_column, value, path_rus_text):
        '''Сбор данных для построения(столбцы, значения ячеек)'''
        try:
            dict_rus = self.exist_check_array(self.read_json(path_rus_text), self.table)

            rus_eng_name = self.russian_name_column(dict_rus, eng_name_column)

            count_column = self.exist_check_int(self.read_json(path_rus_text), self.table)

            return len(eng_name_column), len(value), rus_eng_name, value, count_column
        except Exception:
            print(traceback.format_exc())
            return 0, 0, 0, 0, 0

    def type_column(self, inf_data, path_rus_text):
        '''Собираем тип столбцов, и названия на рус и англ.'''
        type_list = []
        try:
            dict_rus = self.exist_check_array(self.read_json(path_rus_text), self.table)

            for i in inf_data:
                column_name = i[0]
                data_type = i[1]
                try:
                    list_a = [column_name, dict_rus[column_name], data_type]
                except Exception:
                    list_a = [column_name, '', data_type]
                type_list.append(list_a)
        except Exception:
            print(f'Окно тип данных: ошибка: {traceback.format_exc()}')

        return type_list

    def russian_name_column(self, dict_rus, name_column):
        '''Расшифровка с английского на русский.'''
        return [dict_rus[eng_t.name] if eng_t.name in dict_rus else eng_t.name for eng_t in name_column]

    def russian_name_column_over(self, dict_rus, name_column):
        '''Расшифровка с английского на русский другого формата.'''
        return [dict_rus[eng_t] if eng_t in dict_rus else eng_t for eng_t in name_column]

    def exist_check_int(self, array: dict, table: str):
        '''Проверка на существование данных для
          видимости столбцов левой таблицы в params_visible_column.'''
        try:
            value = array['params_visible_column']
            return value[table]
        except Exception:
            return 4