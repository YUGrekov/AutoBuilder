import re, traceback
from peewee import OperationalError
from model import DO, Signals, HardWare
from general_functions import General_functions


class OutDiskrets():
    '''Заполнение таблицы.'''
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.logs_msg = self.mainwindow.logsTextEdit.logs_msg
        self.db_manager = self.mainwindow.tab_1.db_dev
        self.db_orm = self.mainwindow.tab_1.db_dev.get_database()
        self.dop_function = General_functions()

    def calculating_module(self, uso, basket, module):
        '''Вычисление сквозного номера модуля для
        заполнения pValue, pHealth из таблицы HW.'''
        try:          
            query = (HardWare
                     .select(getattr(HardWare, f'variable_{module}'), HardWare.tag)
                     .where((HardWare.uso == uso) & (HardWare.basket == basket))
                     .order_by(HardWare.id)
                     .tuples())
            result = list(query)
    
            if len(result) > 1:
                self.logs_msg(f'''SQL. DO. {uso}.A{basket}_{module}, при вычислении номера
                              для pValue и pHealth обнаружено несколько модулей!''', 2)
                return 'NULL'
            return re.findall('\d+', result[0][0])[0], result[0][1]
        except OperationalError as e:
            self.logs_msg(f'''SQL. DO. Ошибка выполнения запроса: {e}''', 1)
            return 'NULL', None

    def new_signal(self, signal, num_through, tag):
        '''Добавление нового сигнала.'''
        num = f'0{signal.module}' if signal.module < 10 else f'{signal.module}'

        list_DO = dict(id=self.count_row,
                       variable=f'DO[{self.count_row}]',
                       tag=signal.tag,
                       name=signal.description,
                       pValue=f'{tag}_{num}_DO[{signal.channel}]',
                       pHealth=f'mDO_HEALTH[{num_through}]',
                       short_title=signal.description,
                       tag_eng=self.dop_function.translate(signal.tag),
                       uso=signal.uso,
                       basket=signal.basket,
                       module=signal.module,
                       channel=signal.channel)

        DO.insert_many(list_DO).execute()
        self.logs_msg(f'''SQL. DO. Добавлен новый сигнал: {self.count_row}''', 0)

    def update_table(self, signals, discrets):
        '''Обновление тега и названия сигнала в таблице.'''
        try:
            coinciding = (DO
                          .select()
                          .where((DO.tag == signals.tag) & (DO.name == signals.description))
                          .order_by(DO.basket))

            if not bool(coinciding):
                query = (DO
                         .update({'tag': signals.tag, 'name': signals.description})
                         .where((DO.uso == signals.uso)
                                & (DO.basket == signals.basket)
                                & (DO.module == signals.module) 
                                & (DO.channel == signals.channel))
                        )
                query.execute()

                first_discrets = list(discrets.tuples())
                self.logs_msg(f'''SQL. DO. Обновлен сигнал: {first_discrets[0][0]}''', 0)
        except OperationalError as e:
            self.logs_msg(f'''SQL. DO. Ошибка выполнения запроса: {e}''', 1)

    def checking_signal(self, data_signals):
        '''Проверка сигнала на существование в таблице DO.
        По УСО, корзине, модулю и каналу.'''
        for signals in data_signals:
            comparison = (
                (DO.uso == signals.uso)
                & (DO.basket == signals.basket)
                & (DO.module == signals.module)
                & (DO.channel == signals.channel))
            query = (DO
                     .select()
                     .where(comparison)
                     .order_by(DO.basket))

            if bool(query):
                self.update_table(signals, query)
            else:
                self.count_row += 1
                num_through, tag = self.calculating_module(signals.uso, signals.basket, signals.module)
                self.new_signal(signals, num_through, tag)

    def process_request(self):
        '''Обработка нескольких запросов.'''
        try:
            data = (Signals
                    .select()
                    .where((Signals.type_signal.contains('DO')) | (Signals.schema.contains('DO')))
                    .order_by(Signals.description))
            # Проверка: обновляем или добавляем
            self.checking_signal(data)
        except Exception:
            self.logs_msg(f'''SQL. DO. Ошибка выполнения {traceback.format_exc()}''', 2)

    def work_func(self):
        try:
            self.count_row = DO.select().count()
            self.process_request()

            self.logs_msg('''SQL. DO. Работа с таблицей завершена''', 0)
        except Exception:
            self.logs_msg(f'''SQL. DO. Ошибка {traceback.format_exc()}''', 2)