import re, traceback
from peewee import OperationalError
from model import DI, Signals, HardWare
from general_functions import General_functions


class InDiskrets():
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
                self.logs_msg(f'''SQL. DI. {uso}.A{basket}_{module}, при вычислении номера
                              для pValue и pHealth обнаружено несколько модулей!''', 2)
                return 'NULL'
            return re.findall('\d+', result[0][0])[0], result[0][1]
        except OperationalError as e:
            self.logs_msg(f'''SQL. DI. Ошибка выполнения запроса: {e}''', 1)
            return 'NULL', None

    def new_signal(self, signal, num_through, tag):
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

        DI.insert_many(list_DI).execute()
        self.logs_msg(f'''SQL. DI. Добавлен новый сигнал: {self.count_row}''', 0)

    def reserve_add(self, reserve):
        '''Добавляем пустые строки для резерва.'''
        for i in range(self.count_row + 1, self.count_row + reserve + 1):
            empty_row = dict(id=i,
                             variable=f'DI[{i}]',
                             tag=f'LOGIC_DI_{i}',
                             name='Переменная зарезервирована для логически формируемого сигнала',
                             tabl_msg='TblDiscretes',
                             group_diskrets='Общие',
                             tag_eng=f'LOGIC_DI_{i}')
            DI.insert_many(empty_row).execute()
        self.count_row = self.count_row + reserve

    def update_table(self, signals, discrets):
        '''Обновление тега и названия сигнала в таблице.'''
        try:
            coinciding = (DI
                        .select()
                        .where((DI.tag == signals.tag) & (DI.name == signals.description))
                        .order_by(DI.basket))

            if not bool(coinciding):
                query = (DI
                        .update({'tag': signals.tag, 'name': signals.description})
                        .where((DI.uso == signals.uso)
                                & (DI.basket == signals.basket)
                                & (DI.module == signals.module) 
                                & (DI.channel == signals.channel))
                        )
                query.execute()

                first_discrets = list(discrets.tuples())
                self.logs_msg(f'''SQL. DI. Обновлен сигнал: {first_discrets[0][0]}''', 0)
        except OperationalError as e:
            self.logs_msg(f'''SQL. DI. Ошибка выполнения запроса: {e}''', 1)

    def checking_signal(self, data_signals):
        '''Проверка сигнала на существование в таблице DI.
        По УСО, корзине, модулю и каналу.'''
        for signals in data_signals:
            comparison = (
                (DI.uso == signals.uso)
                & (DI.basket == signals.basket)
                & (DI.module == signals.module)
                & (DI.channel == signals.channel))
            query = (DI
                     .select()
                     .where(comparison)
                     .order_by(DI.basket))

            if bool(query):
                self.update_table(signals, query)
            else:
                self.count_row += 1
                num_through, tag = self.calculating_module(signals.uso, signals.basket, signals.module)
                self.new_signal(signals, num_through, tag)

    def process_request(self):
        '''Обработка нескольких запросов.'''
        try:
            where_1 = (Signals.tag % ('CSC%'))
            where_2 = (Signals.schema % ('DI%')) & (~(Signals.tag % ('CSC%')))
            where_3 = (Signals.schema % ('DM%')) & (Signals.type_signal % ('DI%'))
            where = [where_1, where_2, where_3]

            for order in range(len(where)):
                data = (Signals
                        .select()
                        .where(where[order])
                        .order_by(Signals.description))

                # Проверка: обновляем или добавляем
                self.checking_signal(data)

                # Добавляем резервы
                fl_empty = False if self.count_row > 1 else True
                reserve = 0 if order == 2 else int(len(data) * 0.3)
                if reserve and fl_empty:
                    self.rezerv_add(reserve)
        except Exception:
            self.logs_msg(f'''SQL. DI. Ошибка выполнения {traceback.format_exc()}''', 2)

    def work_func(self):
        try:
            self.count_row = DI.select().count()
            self.process_request()

            self.logs_msg('''SQL. DI. Работа с таблицей завершена''', 0)
        except Exception:
            self.logs_msg(f'''SQL. DI. Ошибка {traceback.format_exc()}''', 2)