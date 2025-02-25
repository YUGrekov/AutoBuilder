import re
import traceback
from model_new import AO as Model
from model_new import Signals
from request_sql import RequestSQL
from general_functions import General_functions

T_SIGNALS = 'signals'
T_HW = 'hardware'
T_MOD = ' ao'
TYPE = 'AO'


class OutAnalog():
    '''Заполнение таблицы.'''
    def __init__(self, logtext):
        self.logsTextEdit = logtext
        self.request = RequestSQL()
        self.dop_function = General_functions()

    def check_table(self):
        '''Проверяем таблицу signals на наличие и заполненость.'''
        result_tb_signals = self.request.check_table(T_SIGNALS)
        if not result_tb_signals:
            self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Таблица
                                       signals отсутсвует''', 2)
            return False
        else:
            result_row_signals = self.request.check_row_table(T_SIGNALS)
            if not result_row_signals:
                self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Таблица
                                           signals не заполнена''', 2)
                return False

            result = self.request.check_table(T_MOD)
            if not result:
                self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Таблица do
                                           отсутсвует''', 2)
                self.request.new_table_orm(Model)
                self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Таблица do
                                           добавлена''', 0)
            return True

    def module_calc(self, uso, basket, module):
        '''Вычисление сквозного номера модуля для
        заполнения pValue, pHealth из таблицы HW.'''
        try:
            hw = self.request.where_select(T_HW, f'variable_{module}, tag',
                                           f'''"uso"='{uso}' and "basket"='{basket}' ''', 'id')
            if len(hw) > 1:
                self.logsTextEdit.logs_msg(f'''SQL. {TYPE}.
                                           {uso}.A{basket}_{module},
                                           при вычислении номера
                                           для pValue и pHealth обнаружено
                                           несколько модулей!''', 2)
                return 'NULL'
            return re.findall('\d+', hw[0][0])[0], hw[0][1]
        except Exception:
            self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. {uso}.A{basket}_
                                       {module}, номер модуля pValue и
                                       pHealth не найден!''', 1)
            return 'NULL', None

    def check_signal(self, signal):
        '''Проверка сигнала на существование в таблице.
        По УСО, корзине, модулю и каналу.'''
        uso = signal.uso
        basket = signal.basket
        module = signal.module
        channel = signal.channel
        coinc = self.request.select_orm(Model,
                                        (Model.uso == uso) &
                                        (Model.basket == basket) &
                                        (Model.module == module) &
                                        (Model.channel == channel),
                                        Model.basket)
        for i in coinc:
            self.msg_id = i.id
        return bool(coinc)

    def add_new_signal(self, signal, num_through, tag):
        '''Добавление нового сигнала.'''
        num = f'0{signal.module}' if signal.module < 10 else f'{signal.module}'

        list_AO = dict(id=self.count_row,
                       variable=f'AO[{self.count_row}]',
                       tag=signal.tag,
                       name=signal.description,
                       pValue=f'{tag}_{num}_AO[{signal.channel}]',
                       pHealth=f'mAO_HEALTH[{num_through}]',
                       tag_eng=self.dop_function.translate(signal.tag),
                       uso=signal.uso,
                       basket=signal.basket,
                       module=signal.module,
                       channel=signal.channel)

        self.request.write_base_orm(list_AO, Model)
        self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Добавлен
                                   новый сигнал: {self.count_row}''', 0)

    def update_table(self, signal):
        '''Обновление тега и названия сигнала в таблице.'''
        coinc = self.request.select_orm(Model,
                                        (Model.tag == signal.tag) &
                                        (Model.name == signal.description),
                                        Model.basket)
        if not bool(coinc):
            self.request.update_base_orm(Model,
                                         {'tag': signal.tag,
                                          'name': signal.description},
                                         (Model.uso == signal.uso) &
                                         (Model.basket == signal.basket) &
                                         (Model.module == signal.module) &
                                         (Model.channel == signal.channel))
            self.logsTextEdit.logs_msg(f'''SQL. {TYPE}.
                                       Строка обновлена:
                                       {self.msg_id}''', 0)

    def add_diskrets(self):
        try:
            # Проверяем таблицу signals
            if not self.check_table():
                raise

            self.count_row = self.request.count_row_orm(Model)
            data = self.request.select_orm(Signals,
                                           (Signals.type_signal.contains(TYPE)) |
                                           (Signals.schema.contains(TYPE)),
                                           Signals.description)

            for signal in data:
                exist = self.check_signal(signal)

                if exist:
                    self.update_table(signal)
                else:
                    self.count_row += 1
                    num_through, tag = self.module_calc(signal.uso,
                                                        signal.basket,
                                                        signal.module)
                    self.add_new_signal(signal, num_through, tag)

            self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Работа
                                       с таблицей завершена''', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'''SQL. {TYPE}. Ошибка
                                       {traceback.format_exc()}''', 2)