'''Заполнение таблицы разработки HardWare.'''
import traceback
# from model import HardWare
# from model import Signals
# from request_sql import RequestSQL
from general_functions import General_functions

T_SIGNALS = 'signals'


class AI():
    name_m = 'AI[{}]'
    type_m = 'MK-516-008A'
    count = 0

    def __new__(cls):
        AI.count += 1
        return AI.count


class AO():
    name_m = 'AO[{}]'
    type_m = 'MK-514-008'
    count = 0

    def __new__(cls):
        AO.count += 1
        return AO.count


class DI():
    name_m = 'DI[{}]'
    type_m = 'MK-521-032'
    count = 0

    def __new__(cls):
        DI.count += 1
        return DI.count


class DO():
    name_m = 'DO[{}]'
    type_m = 'MK-531-032'
    count = 0

    def __new__(cls):
        DO.count += 1
        return DO.count


class RS():
    name_m = 'RS[{}];3'
    type_m = 'MK-541-002'
    count = 0

    def __new__(cls):
        RS.count += 1
        return RS.count


class BaseType():
    '''Описания атрибутов и принадлежность классам.'''
    PARAM_MODULE = {
        'ai': AI,
        'ao': AO,
        'di': DI,
        'do': DO,
        'rs': RS}


class ConstValues():
    '''Методы, с постоянные значениями для корзины.
    Контроллеры, БП, и тд.'''
    def position(self, query):
        '''Вычисляем позицию корзин с наличием КК или отсутствием.'''
        list_basket = [i.basket for i in query]
        return min(list_basket) - 1, max(list_basket)

    def add_kc_row(self, uso, request):
        '''Добавление в базу ОСН и РЕЗ КЦ.'''
        for i in range(1, 3):
            const_row = [
                {'id': f'{i}', 'uso': uso, 'variable': f'countsErrDiag[{i}]',
                 'basket': f'{i}',
                 'type_0': 'MK-550-024', 'variable_0': 'PSU',
                 'type_1': 'MK-546-010', 'variable_1': 'MN;3',
                 'type_2': 'MK-504-120', 'variable_2': 'CPU;7'}
            ]
            request.write_base_orm(const_row, HardWare)

    def add_kk_row(self, uso, request, num_max: int):
        '''Добавление в базу KK по необходимости.'''
        count = num_max + 1
        for i in range(2):
            const_row = [
                {'id': f'{count + i}', 'uso': uso,
                 'variable': f'countsErrDiag[{count + i}]',
                 'basket': f'{count + i}',
                 'type_0': 'MK-550-024', 'variable_0': 'PSU',
                 'type_1': 'MK-544-040', 'variable_1': 'EthEx;3',
                 'type_2': 'MK-504-120', 'variable_2': 'CPU;7'}
            ]
            request.write_base_orm(const_row, HardWare)

    def assembly_row(self, counErr: int, pwl_id: int,
                     num_b: int, name_uso: str):
        """Повторное значение строк.
        Args:
            countsErr (int): Счетчик ошибок для СУ.
            pwl_id (int): PowerLink_ID для СУ.

        Returns:
            dict: Словарь строки для добавления
        """
        return {'id': counErr,
                'variable': f'countsErrDiag[{counErr}]',
                'uso': name_uso,
                'basket': f'{num_b}',
                'powerLink_ID': pwl_id,
                'type_0': 'MK-550-024',
                'variable_0': 'PSU',
                'type_1': 'MK-545-010',
                'variable_1': 'CN;3',
                }

    def add_const_sql(self, kk_flag: bool, name: str,
                      total: int, request):
        """Добавляем строки КЦ и КК.
        Args:
            kk_flag (bool): Флаг налиция КК.
            name (_type_): Название шкафа.
            total (int): Выборка из базы п окорзине и шкафу.
            request (_type_): Объект листа запроса
        Returns:
            _type_: Мин и Мах номер корзины, флаг одного захода
        """
        num_min, num_max = self.position(total)
        self.add_kc_row(name, request)
        if kk_flag:
            self.add_kk_row(name, request, num_max)
            num_max = num_max + 2
        t_flag = True
        return num_min, num_max, t_flag


class HW(ConstValues, BaseType):
    '''Заполнение таблицы Hardware.'''
    def __init__(self, mainwindow: None):

        self.m_window = mainwindow
        self.db = self.m_window.tab_1.db_dev.get_database()
        self.logs_msg = self.m_window.logsTextEdit.logs_msg

        self.dop_function = General_functions()

    def check_table(self):
        '''Проверяем таблицу signals на наличие и заполненость.'''
        result = self.request.check_table(T_SIGNALS)
        if not result:
            self.logsTextEdit.logs_msg('''SQL. Hardware. Таблица
                                       signals отсутсвует
                                       или не заполнена''', 2)
            return False
        return True

    def write_row(self, data_basket, write_array):
        """Добавляем новую строку с заполненой корзиной в SQL.
        Args:
            data_basket (_type_): Данные для формирования строки из Signals.
            write_array (_type_): Массив с начальными данными корзины.
        """
        for data in data_basket:
            module_s = data.module
            type_s = data.type_signal

            for type_m, variable_m in self.PARAM_MODULE.items():

                if (str(type_s).lower() in type_m):

                    write_array[f'type_{module_s}'] = variable_m.type_m
                    write_array[f'variable_{module_s}'] = f'{variable_m.name_m}'.format(variable_m())
        self.request.write_base_orm(write_array, HardWare)
        print(f'SQL. Hardware. Корзина {data.uso}.A{data.basket} добавлена')
        # self.logsTextEdit.logs_msg(f'''SQL. Hardware. Корзина
        #                            {data.uso}.A{data.basket} добавлена''', 1)

    def work_func(self, kk_flag: bool = False):
        """Заполнение таблицы.
        Args:
            kk_flag (bool): Нужен ли КК
        """
        t_flag = False
        powerLink_ID = 0
        counts_uso = 0
        # try:
        #     # Проверяем таблицу signals
        #     if not self.check_table():
        #         raise
        #     # Находим названия неповторяющихся шкафов
        #     all_uso = self.request.non_repea_names(Signals,
        #                                            Signals.uso,
        #                                            Signals.uso)
        #     print('SQL. Hardware. Заполнение таблицы')
        #     # self.logsTextEdit.logs_msg('''SQL. Hardware.
        #     #                            Заполнение таблицы''', 1)
        #     for name in all_uso:
        #         counts_uso += 1
        #         # Кол-во корзин в УСО
        #         total = self.request.non_repea_cond(Signals, Signals.basket,
        #                                             Signals.uso == name.uso,
        #                                             Signals.basket)
        #         # Выполняется 1 раз, постоянные строки - КЦ, КК
        #         if not t_flag:
        #             err_1, err_all, t_flag = self.add_const_sql(kk_flag,
        #                                                         name.uso,
        #                                                         total,
        #                                                         self.request)
        #         if counts_uso <= 2:
        #             countsErr = err_1 if counts_uso == 1 else err_all

        #         for number in total:
        #             powerLink_ID += 1
        #             countsErr += 1
        #             # Сортируем неповторяющиеся сигналы по шкафу и корзине
        #             data_basket = self.request.non_repea_cond(Signals,
        #                                                       Signals.module,
        #                                                       (Signals.uso == number.uso) & (Signals.basket == number.basket),
        #                                                       Signals.module)
        #             # Начальные данные корзины: бп, контролл, усо и тд.
        #             write_array = self.assembly_row(countsErr, powerLink_ID,
        #                                             number.basket, number.uso)
        #             # Формирование корзины и запись в SQL
        #             self.write_row(data_basket, write_array)

        #     print('SQL. Hardware. Таблица заполнена')
        #     # self.logsTextEdit.logs_msg('''SQL. Hardware.
        #     #                            Таблица заполнена''', 1)
        # except Exception:
        #     print({traceback.format_exc()})
        #     # self.logsTextEdit.logs_msg(f'''SQL. Hardware. Ошибка
        #     #                            {traceback.format_exc()}''', 2)