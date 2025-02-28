import re, traceback
from peewee import OperationalError
from model import RS, Signals, HardWare
from general_functions import General_functions


class Interface():
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
                self.logs_msg(f'''SQL. RS. {uso}.A{basket}_{module}, при вычислении номера
                              для pValue и pHealth обнаружено несколько модулей!''', 2)
                return 'NULL'
            return re.findall('\d+', result[0][0])[0], result[0][1]
        except OperationalError as e:
            self.logs_msg(f'''SQL. RS. Ошибка выполнения запроса: {e}''', 1)
            return 'NULL', None

    def new_signal(self, signal, num_through, tag):
        '''Добавление нового сигнала.'''
        num = f'0{signal.module}' if signal.module < 10 else f'{signal.module}'

        list_RS = dict(id=self.count_row,
                       variable=f'RS[{self.count_row}]',
                       name=signal.description,
                       pValue=f'{tag}_{num}.COM_CH[{signal.channel}]',
                       uso=signal.uso,
                       basket=signal.basket,
                       module=signal.module,
                       channel=signal.channel)

        RS.insert_many(list_RS).execute()
        self.logs_msg(f'''SQL. RS. Добавлен новый сигнал: {self.count_row}''', 0)

    def update_table(self, signals, discrets):
        '''Обновление тега и названия сигнала в таблице.'''
        try:
            coinciding = (RS
                          .select()
                          .where((RS.tag == signals.tag) & (RS.name == signals.description))
                          .order_by(RS.basket))

            if not bool(coinciding):
                query = (RS
                         .update({'tag': signals.tag, 'name': signals.description})
                         .where((RS.uso == signals.uso)
                                & (RS.basket == signals.basket)
                                & (RS.module == signals.module) 
                                & (RS.channel == signals.channel))
                        )
                query.execute()

                first_discrets = list(discrets.tuples())
                self.logs_msg(f'''SQL. RS. Обновлен сигнал: {first_discrets[0][0]}''', 0)
        except OperationalError as e:
            self.logs_msg(f'''SQL. RS. Ошибка выполнения запроса: {e}''', 1)

    def checking_signal(self, data_signals):
        '''Проверка сигнала на существование в таблице DO.
        По УСО, корзине, модулю и каналу.'''
        for signals in data_signals:
            comparison = (
                (RS.uso == signals.uso)
                & (RS.basket == signals.basket)
                & (RS.module == signals.module)
                & (RS.channel == signals.channel))
            query = (RS
                     .select()
                     .where(comparison)
                     .order_by(RS.basket))

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
                    .where((Signals.type_signal.contains('RS')) | (Signals.schema.contains('RS')))
                    .order_by(Signals.description))
            # Проверка: обновляем или добавляем
            self.checking_signal(data)
        except Exception:
            self.logs_msg(f'''SQL. RS. Ошибка выполнения {traceback.format_exc()}''', 2)

    def work_func(self):
        try:
            self.count_row = RS.select().count()
            self.process_request()

            self.logs_msg('''SQL. RS. Работа с таблицей завершена''', 0)
        except Exception:
            self.logs_msg(f'''SQL. RS. Ошибка {traceback.format_exc()}''', 2)