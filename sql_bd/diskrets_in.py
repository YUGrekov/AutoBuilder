import re
import traceback
from model import DI
from model import Signals
from request_sql import RequestSQL
from general_functions import General_functions

T_SIGNALS = 'signals'
T_HW = 'hardware'
T_DI = ' di'


class InDiskrets():
    '''Заполнение таблицы.'''
    def __init__(self, logtext):
        self.logsTextEdit = logtext
        self.request = RequestSQL()
        self.dop_function = General_functions()

    def check_table(self):
        '''Проверяем таблицу signals на наличие и заполненость.'''
        result_tb_signals = self.request.check_table(T_SIGNALS)
        if not result_tb_signals:
            self.logsTextEdit.logs_msg('''SQL. DI. Таблица
                                       signals отсутсвует''', 2)
            return False
        else:
            result_row_signals = self.request.check_row_table(T_SIGNALS)
            if not result_row_signals:
                self.logsTextEdit.logs_msg('''SQL. DI. Таблица
                                           signals не заполнена''', 2)
                return False

            result = self.request.check_table(T_DI)
            if not result:
                self.logsTextEdit.logs_msg('''SQL. DI. Таблица di
                                           отсутсвует''', 2)
                self.request.new_table_orm(DI)
                self.logsTextEdit.logs_msg('''SQL. DI. Таблица di
                                           добавлена''', 0)
            return True

    def module_calc(self, uso, basket, module):
        '''Вычисление сквозного номера модуля для
        заполнения pValue, pHealth из таблицы HW.'''
        try:
            hw = self.request.where_select(T_HW, f'variable_{module}, tag',
                                           f'''"uso"='{uso}' and "basket"='{basket}' ''', 'id')
            if len(hw) > 1:
                self.logsTextEdit.logs_msg(f'''SQL. DI.
                                           {uso}.A{basket}_{module},
                                           при вычислении номера
                                           для pValue и pHealth обнаружено
                                           несколько модулей!''', 2)
                return 'NULL'
            return re.findall('\d+', hw[0][0])[0], hw[0][1]
        except Exception:
            self.logsTextEdit.logs_msg(f'''SQL. DI. {uso}.A{basket}_{module},
                                       номер модуля pValue и
                                       pHealth не найден!''', 1)
            return 'NULL', None

    def process_request(self):
        '''Обработка нескольких запросов.'''
        where_1 = (Signals.tag % ('CSC%'))
        where_2 = (Signals.schema % ('DI%')) & (~(Signals.tag % ('CSC%')))
        where_3 = (Signals.schema % ('DM%')) & (Signals.type_signal % ('DI%'))
        where = [where_1, where_2, where_3]

        fl_empty = False if self.count_row > 1 else True

        for order in range(3):
            data = self.request.select_orm(Signals, where[order],
                                           Signals.description)
            count_rez = 0 if order == 2 else int(len(data) * 0.3)
            # Проверяем, обновляем или добавляем сигнал
            self.check_signal(data)
            # Добавляем резервы
            if count_rez and fl_empty:
                self.add_empty_row(count_rez)

    def check_signal(self, data):
        '''Проверка сигнала на существование в таблице DI.
        По УСО, корзине, модулю и каналу.'''
        for signal in data:
            uso = signal.uso
            basket = signal.basket
            module = signal.module
            channel = signal.channel
            coinc = self.request.select_orm(DI,
                                            (DI.uso == uso) &
                                            (DI.basket == basket) &
                                            (DI.module == module) &
                                            (DI.channel == channel),
                                            DI.basket)
            for i in coinc:
                self.msg_id = i.id

            if bool(coinc):
                self.update_table(signal)
            else:
                self.count_row += 1
                num_through, tag = self.module_calc(signal.uso,
                                                    signal.basket,
                                                    signal.module)
                self.add_new_signal(signal, num_through, tag)

    def add_new_signal(self, signal, num_through, tag):
        '''Добавление нового сигнала.'''
        num = f'0{signal.module}' if signal.module < 10 else f'{signal.module}'
        try:
            if 'CSC' in signal.tag:
                group_di = 'Диагностика'
            elif 'EC' in signal.tag:
                group_di = 'Электроснабжение'
            else:
                group_di = 'Общие'
        except Exception:
            group_di = ''
        short_title = re.sub(r'\sшкаф.+[МНСПТРПСАР].+[0-9)КЦБРУ]', '', signal.description)

        list_DI = dict(id=self.count_row,
                       variable=f'DI[{self.count_row}]',
                       tag=signal.tag,
                       name=signal.description,
                       pValue=f'{tag}_{num}_DI[{signal.channel}]',
                       pHealth=f'mDI_HEALTH[{str(num_through)}]',
                       Inv=0,
                       ErrValue=0,
                       priority_0=1,
                       priority_1=1,
                       Msg=1,
                       tabl_msg='TblDiscretes',
                       group_diskrets=group_di,
                       msg_priority_0=1,
                       msg_priority_1=1,
                       short_title=short_title,
                       tag_eng=self.dop_function.translate(signal.tag),
                       uso=signal.uso,
                       basket=signal.basket,
                       module=signal.module,
                       channel=signal.channel)

        self.request.write_base_orm(list_DI, DI)
        self.logsTextEdit.logs_msg(f'''SQL. DI. Добавлен
                                   новый сигнал: {self.count_row}''', 0)

    def add_empty_row(self, count_rez):
        '''Добавляем пустые строки для резерва.'''
        for i in range(self.count_row + 1, self.count_row + count_rez + 1):
            empty_row = dict(id=i,
                             variable=f'DI[{i}]',
                             tag=f'LOGIC_DI_{i}',
                             name='Переменная зарезервирована для логически формируемого сигнала',
                             tabl_msg='TblDiscretes',
                             group_diskrets='Общие',
                             tag_eng=f'LOGIC_DI_{i}')
            self.request.write_base_orm(empty_row, DI)
        self.count_row = self.count_row + count_rez

    def update_table(self, signal):
        '''Обновление тега и названия сигнала в таблице.'''
        coinc = self.request.select_orm(DI,
                                        (DI.tag == signal.tag) &
                                        (DI.name == signal.description),
                                        DI.basket)
        if not bool(coinc):
            self.request.update_base_orm(DI,
                                         {'tag': signal.tag,
                                          'name': signal.description},
                                         (DI.uso == signal.uso) &
                                         (DI.basket == signal.basket) &
                                         (DI.module == signal.module) &
                                         (DI.channel == signal.channel))
            self.logsTextEdit.logs_msg(f'''SQL. DI.
                                       Строка обновлена:
                                       {self.msg_id}''', 0)

    def work_func(self):
        try:
            self.count_row = self.dop_function.count_row_orm(DI)

            self.process_request()

            self.logsTextEdit.logs_msg('''SQL. DI. Работа
                                       с таблицей завершена''', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'''SQL. DI. Ошибка
                                       {traceback.format_exc()}''', 2)