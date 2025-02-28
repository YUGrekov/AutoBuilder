import re, traceback
from functools import reduce
from peewee import OperationalError, fn
from model import ZD, DI, DO, Signals, HardWare
from general_functions import General_functions


class InitValves():
    def __init__(self, parent=None):
        '''Состовляем новый список задвижек.'''
        # Список ключевых слов для поиска
        keywords = ['задвижк', 'клап', 'клоп', 'кран шар', 'заслон', 'жалюз']
        # Создаем условия для поиска
        conditions = []
        for keyword in keywords:
            conditions.append(fn.LOWER(DI.name).contains(keyword.lower()))
        # Объединяем условия с помощью OR
        self.query = (DI
                      .select(DI.name)
                      .where(reduce(lambda a, b: a | b, conditions))
                      .order_by(DI.id))

    def get_list(self):
        return self.query


class Valves():
    '''Заполнение таблицы.'''
    def __init__(self, mainwindow, parent=None):
        self.parent = parent
        self.mainwindow = mainwindow
        self.logs_msg = self.mainwindow.logsTextEdit.logs_msg
        self.db_manager = self.mainwindow.tab_1.db_dev
        self.db_orm = self.mainwindow.tab_1.db_dev.get_database()
        self.dop_function = General_functions()
    
    def normalize_equipment_name(self, name):
        '''Функция для преобразования названий.'''
        name = re.sub(r'\s*-\s*[^№]*', '', name)  # Удаляем всё после " - "
        name = re.sub(r'\.\s*[^№]*', '', name)    # Удаляем всё после точки
        name = re.sub(r'\s*\([^)]*\)', '', name)  # Удаляем всё в скобках
        name = re.sub(r'\s*№\s*', ' №', name)     # Приводим "№" к единому формату
        name = name.strip()  # Убираем лишние пробелы
        return name

    def sort_key(self, name):
        '''Функция для сортировки: сначала "Задвижка", затем остальные.'''
        return (0, name) if name.startswith('Задвижка') else (1, name)

    def process_request(self):
        '''Составляем новый список задвижек.'''
        array_str_valves = self.parent.selections.get('ZD', [])  # Получаем список или пустой список по умолчанию
        if not array_str_valves:  # Если список пустой
            init_zd = InitValves(self)
            array_str_valves = [signals.name for signals in init_zd.get_list()]  # Создаем список имен

        normalized_names = [self.normalize_equipment_name(name) for name in array_str_valves]

        # Удаляем дубликаты
        unique_names = list(set(normalized_names))

        # Сортируем список
        sorted_equipment_list = sorted(unique_names, key=self.sort_key)

        # Выводим результат
        for name in sorted_equipment_list:
            print(name)
        
        # if not self.count_row:
        
        #     init_zd = InitValves(self)
        #     init_zd.get_list()
        # elif  

        # # Выполняем запрос
        # for item in query:
        #     print(item.name)


        # new_zd = []
        # name_klapan = ['продувк', 'воздушн', 'Воздушн', 'соленоидн', 'приточн']

        # where = (ZD.name % ('%задвижк%') | ZD.name % ('%клап%') | ZD.name % ('%клоп%') |
        #          ZD.name % ('%кран шар%') | ZD.name % ('%заслон%') | ZD.name % ('%жалюз%'))

        # list_zd = self.request.select_orm(DI, where, DI.name)
        # for zd in list_zd:
        #     fl_repl = True
        #     valves = zd.name.split(' - ')[0]
        #     valves = re.sub(r'(открыт)+[аы]|(закрыт)+[аы]|(открыт)|(закрыт)', '', valves)
        #     for name in name_klapan:
        #         if name in valves:
        #             fl_repl = False
        #     if fl_repl:
        #         valves = re.sub(r'( Клапан)|( клапан)|(. Клапан)', '', valves)
        #     new_zd.append(valves)
        # for i in sorted(set(new_zd)):
        #     print(i)

    def work_func(self):
        try:
            self.count_row = ZD.select().count()
            self.process_request()

            self.logs_msg('''SQL. ZD. Работа с таблицей завершена''', 0)
        except Exception:
            self.logs_msg(f'''SQL. ZD. Ошибка {traceback.format_exc()}''', 2)