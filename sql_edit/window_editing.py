import re
import traceback
from enum import Enum
from sql_metadata import Parser
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QMainWindow, QTableWidget, QPushButton, QComboBox, QLabel, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QSplitter, QTableWidgetItem, QAbstractItemView, QHeaderView
from sql_edit.add_methodse_edit import Editing_SQL
from connect_log.logging_text import LogsTextEdit


class ConstSize(Enum):
    WIN_SIZE_MAIN_W = 1600
    WIN_SIZE_MAIN_H = 860
    WIN_SIZE_TYPETABLE_W = 500
    WIN_SIZE_TYPETABLE_H = 600
    WIDTH_BORDER = 5
    COUNT_ONE = 1
    CONTEXT_W = 800
    CONTEXT_H = 675
    SIZE_SPLITTER = [500, 100]


USED_TABLE = [('AI', 'ai'), ('AO', 'ao'), ('DI', 'di'), ('DO', 'do'),
              ('ctrlDO', 'do'), ('ctrlAO', 'ao'), ('NA', 'umpna'),
              ('ZD', 'zd'), ('VS', 'vs'), ('VSGRP', 'vsgrp'), ('BUF', 'buf'),
              ('RSreq', 'rsreq'), ('KTPR', 'ktpr'), ('KTPRA', 'ktpra'),
              ('KTPRS', 'ktprs'), ('NPS', 'nps'), ('AIVisualValue', 'ai'),
              ('Facility', ''), ('PI', 'pi'), ('BUFr', 'bufr'), ('UTS', 'uts'),
              ('UPTS', 'upts')]

LIST_TYPE = {'AI': ['Norm', 'Warn', 'Avar', 'Ndv', 'LTMin', 'MTMax', 'Min6',
                    'Min5', 'Min4', 'Min3_IsMT10Perc', 'Min2_IsNdv2ndParam',
                    'Min1_IsHighVibStat', 'Max1_IsHighVibStatNMNWR',
                    'Max2_IsHighVibNoStat', 'Max3_IsAvarVibStat',
                    'Max4_IsAvarVibStatNMNWR', 'Max5_IsAvarVibNoStat',
                    'Max6_IsAvar2Vib', 'Status'],
             'DI': ['Value', 'Break', 'KZ', 'NC'],
             'BUF': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                     '11', '12', '13', '14', '15'],
             'ZD': ['State_1_Opening', 'State_2_Opened', 'State_3_Middle',
                    'State_4_Closing', 'State_5_Closed', 'Dist', 'Imit',
                    'NOT_EC', 'Open', 'Close', 'Stop',
                    'StopClose', 'KVO', 'KVZ', 'MPO', 'MPZ', 'CorrCO',
                    'CorrCZ', 'VMMO', 'VMMZ', 'NOT_ZD_EC_KTP', 'Local',
                    'Mufta', 'Avar_BUR', 'CorrCOCorrCZ', 'ErrMPO',
                    'ErrMPZ', 'EC', 'RS_OK', 'Blink', 'Neisprav',
                    'NeispravVU', 'Close_Fail', 'Open_Fail', 'Stop_Fail',
                    'Unpromted_Open', 'Unpromted_Close', 'Avar', 'Diff',
                    'WarnClose', 'ECsign'],
             'VSGRP': ['REZ_EXIST', 'REM', 'OTKL'],
             'VS': ['State_1_VKL', 'State_2_OTKL', 'State_3_ZAPUSK',
                    'State_4_OSTANOV', 'Mode_1_OSN', 'Mode_2_REZ',
                    'Mode_3_RUCH', 'Mode_4_REM', 'NEISPRAV', 'SEC_EC',
                    'EC', 'MP', 'Imit', 'BLOCK_WORK_IS_ACTIVE',
                    'BLOCK_STOP_IS_ACTIVE', 'WAITING_FOR_FUTURE_PUSK',
                    'WAITING_FOR_APV', 'STARTED_AS_DOP', 'REORDER_REZ',
                    'PC', 'WarnOff', 'PC_FALL', 'PC_NOT_UP', 'MPC_CONTROL',
                    'PC_CONTROL', 'MPC_CEPI_OTKL', 'MPC_CEPI_VKL',
                    'EC_CONTROL', 'EC_FALL', 'MPC_FALL', 'MPC_NOT_FALL',
                    'MPC_CONTROL_RUCH', 'PC_CONTROL_RUCH', 'EC_CONTROL_RUCH',
                    'MPC_NOT_UP', 'EXTERNAL'],
             'NA': ['MainState_1_VKL', 'MainState_2_OTKL', 'MainState_3_PUSK',
                    'MainState_4_OSTANOV', 'SubState_1_GP',
                    'SubState_2_GORREZ', 'SubState_3_PP', 'SubState_4_PO',
                    'Mode_1_OSN', 'Mode_2_TU', 'Mode_3_REZ', 'Mode_4_REM',
                    'KTPRA_P', 'SimAgr', 'Prog_1', 'Prog_2', 'HIGHVIB',
                    'HIGHVIBNas', 'QF3A', 'QF1A', 'BBon', 'BBoff',
                    'KTPRA_FNM', 'KTPRA_M', 'GMPNA_M', 'BBErrOtkl_All',
                    'BBErrOtkl', 'BBErrOtkl1', 'BBErrVkl', 'SAR_Ramp',
                    'StartWork', 'StopWork', 'StopNoCmd_1', 'StopNoCmd_2',
                    'StartNoCmd', 'StateAlarm', 'StateAlarm_ChRP',
                    'StateAlarm_All', 'ChRPRegError', 'LogicalChRPCrash',
                    'StateAlarm_VV', 'StopErr', 'StopErr2', 'StopErr_All',
                    'StartErr', 'StartErr2', 'StartErr3', 'StartErr_All',
                    'KKCAlarm1', 'KKCAlarm2', 'KKCAlarm3', 'KKCAlarm4',
                    'InputPath', 'OutputPath', 'OIPVib', 'GMPNA_F',
                    'GMPNA_P', 'KTPR_ACHR', 'KTPR_SAON', 'ZD_Unprompted_Close',
                    'needRez', 'needOverhaul', 'ED_IsMT10Perc',
                    'ED_IsNdv2ndParam', 'ED_IsHighVibStat',
                    'ED_IsHighVibNoStat', 'ED_IsAvarVibStat',
                    'ED_IsAvarVibNoStat', 'ED_IsAvar2Vib', 'Pump_IsMT10Perc',
                    'Pump_IsNdv2ndParam', 'Pump_IsHighVibStat',
                    'Pump_IsHighVibStatNMNWR', 'Pump_IsHighVibNoStat',
                    'Pump_IsAvarVibStat', 'Pump_IsAvarVibStatNMNWR',
                    'Pump_IsAvarVibNoStat', 'Pump_IsAvar2Vib'],
             'KTPR': ['P', 'F', 'M', 'NP'], 'KTPRA': ['P', 'F', 'M', 'NP'],
             'KTPRS': ['P', 'F', 'M', 'NP'],
             'NPS': ['ModeNPSDst', 'MNSInWork', 'IsMNSOff', 'IsNPSModePsl',
                     'IsPressureReady', 'NeNomFeedInterval', 'OIPHighPressure',
                     'KTPR_P', 'KTPR_M', 'CSPAWorkDeny', 'TSstopped',
                     'stopDisp', 'stopCSPA', 'stopARM', 'CSPAlinkOK'],
             'Facility': ['ndv2Gas', 'gasKTPR', 'activeGas',
                          'startExcessHeat', 'stopExcessHeat', 'warnGasPoint1',
                          'warnGasPoint2', 'warnGasPoint3', 'warnGasPoint4',
                          'warnGasPoint5', 'warnGasPoint6', 'warnGasPoint7',
                          'warnGasPoint8', 'longGasPoint1', 'longGasPoint2',
                          'longGasPoint3', 'longGasPoint4', 'longGasPoint5',
                          'longGasPoint6', 'longGasPoint7', 'longGasPoint8'],
             'DO': ['Value'], 'RSreq': ['ok'], 'ctrlDO': [''], 'ctrlAO': [''],
             'AO': [''], 'BUFr': [''], 'AIVisualValue': ['']}


class TableWidget(QTableWidget):
    def __init__(self, edit_SQL, table_used, logging,
                 tw_dub: bool = False, parent=None):
        super(TableWidget, self).__init__(parent)
        self.setStyleSheet("""
                           QTableWidget{
                           font:13px times;
                           border: 1px solid #a19f9f;
                           border-bottom-left-radius: 5;
                           border-bottom-right-radius: 5;
                           }""")

        self.table_us = table_used
        self.tw_dub = tw_dub
        self.edit_SQL = edit_SQL
        self.logging = logging
        self.parent = parent
        column, row, hat_name, value, end = self.object_data_table()

        self.init_table(column, row, hat_name, value, end)

    def object_data_table(self) -> tuple:
        '''Данные из базы SQL для построения таблицы'''
        value = self.parent.db_dev.execute_query(f'SELECT * FROM "{self.table_us}" ORDER BY id')
        eng_name_column = self.parent.db_dev.execute_query_desc(f'SELECT * FROM "{self.table_us}" ORDER BY id')
        path_rus_text = self.parent.connect.path_rus_text

        return self.edit_SQL.editing_sql(eng_name_column, value, path_rus_text)

    def init_table(self, column: int, row: int,
                   hat_name: list, value: list, end: int):
        """Построение таблицы с данными

        Args:
            column (int): кол-во столбцов
            row (int): кол-во строк
            hat_name (list): заголовки столбцов
            value (list): значения ячеек
            end (list): видимость столбцов в левой таблице
        """
        self.setColumnCount(column)
        self.setRowCount(row)
        self.setHorizontalHeaderLabels(hat_name)
        self.verticalHeader().setVisible(False)
        self.installEventFilter(self)
        style = "::section {""background-color: #dbcaba;}"
        self.horizontalHeader().setStyleSheet(style)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        for tw_row in range(row):
            for tw_column in range(column):
                if value[tw_row][tw_column] is None:
                    item = QTableWidgetItem('')
                else:
                    item = QTableWidgetItem(str(value[tw_row][tw_column]))
                    # Подсказки к ячейкам
                    self.search_text(str(value[tw_row][tw_column]), "di", item)
                    self.search_text(str(value[tw_row][tw_column]), "do", item)
                    self.search_text(str(value[tw_row][tw_column]), "ai", item)

                if not tw_column:
                    item.setFlags(Qt.ItemIsEnabled)
                self.setItem(tw_row, tw_column, item)
        # Видимость столбцов
        if not self.tw_dub:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            if end:
                [self.setColumnHidden(idx, True) for idx in range(0, end)]
            else:
                [self.setColumnHidden(idx, False) for idx in range(0, column)]
        else:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            if end:
                [self.setColumnHidden(idx, True) for idx in range(end, column)]
                if not self.isVisible():
                    self.setVisible(True)
            else:
                self.setVisible(False)

        self.blockSignals(False)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        # Events
        self.itemChanged.connect(self.click_position)

    def width_column(self) -> int:
        '''Получаем значение ширины 4 колонок'''
        width = 0
        for i in range(4):
            width += self.columnWidth(i) + ConstSize.WIDTH_BORDER.value
        return width

    def tw_clear_lines(self, rowcount: int):
        """Очистка таблицы виджета QTableWidget

        Args:
            rowcount (int): кол-во строк
        """
        if not rowcount:
            while rowcount >= 0:
                self.removeRow(rowcount)
                rowcount -= 1

    def data_cell(self):
        '''Текущая позиция ячейки'''
        return self.currentRow(), self.currentColumn()

    def row_count_tabl(self):
        '''Общее кол-во строк в таблице'''
        return self.rowCount()

    def column_count_tabl(self):
        '''Общее кол-во столбцов в таблице'''
        return self.columnCount()

    def text_cell(self, row: int, column: int) -> str:
        """Значение в текущей ячейке

        Args:
            row (int): Строка ячейки
            column (int): Столбец ячейки

        Returns:
            str: Значение
        """
        return self.item(row, column).text()

    def search_text(self, value_cell: str, what_looking: str, item):
        """Функция поиска описания ячейки

        Args:
            value_cell (str): значчение яччейки
            what_looking (str): что ищем
            item (_type_): элемент qtablewidget
        """
        if value_cell.lower().find(what_looking) != -1:

            try:
                isdigit_num = re.findall('\d+', str(value_cell))
                value = self.parent.db_dev.execute_query_one(f"""
                                                            SELECT "name"
                                                            FROM "{self.table_us}"
                                                            WHERE id = {int(isdigit_num[0])}""")
                # fetchone = self.query.where_id_select(self.table_us,
                #                                     "name",
                #                                     int(isdigit_num[0]))
                item.setToolTip(value[0])
            except Exception:
                return ''

    def click_position(self):
        '''Отработка события при изменении ячейки'''
        row, column = self.data_cell()
        # При добавлении новой строки она == -1
        if row == -1:
            return
        try:
            value = self.text_cell(row, column)
            value_id = self.text_cell(row, 0)
        except Exception:
            value = None
            # value_id = None
            value_id = self.text_cell(row, 0)
        # Переход на нижнюю строку
        if (row + 1) == self.row_count_tabl():
            self.setCurrentCell(row, column)
        else:
            self.setCurrentCell(row + 1, column)

        hat_name = self.parent.db_dev.execute_query_desc(f'SELECT * FROM "{self.table_us}" ORDER BY id')

        active_column = list(hat_name)[column]
        try:
            change_value = "NULL" if value is None or value == '' else f'{value}'

            if change_value == 'NULL':
                string = f'SET "{active_column.name}"= NULL'
            else:
                string = f'''SET "{active_column.name}"='{change_value}' '''

            self.parent.db_dev.query_no_return(f"""UPDATE "{self.table_us}" {string} WHERE id={value_id}""")

            return
        except Exception:
            self.logging.logs_msg(f'Таблица: {self.table_us}, ошибка при изменении ячейки: {traceback.format_exc()}', 2)
            return

    def value_change(self, value):
        '''Отработка события при изменении ячейки'''
        row, column = self.data_cell()
        value_id = self.text_cell(row, 0)
        hat_name = self.parent.db_dev.execute_query_desc(f'SELECT * FROM "{self.table_us}" ORDER BY id')

        self.setItem(row, column, QTableWidgetItem(value))

        active_column = list(hat_name)[column]
        try:
            change_value = "NULL" if value is None or value == '' else f'{value}'

            if change_value == 'NULL':
                string = f'SET "{active_column.name}"= NULL'
            else:
                string = f'''SET "{active_column.name}"= '{change_value}' '''

            self.parent.db_dev.query_no_return(f"""UPDATE "{self.table_us}" {string} WHERE id={value_id}""")

            return
        except Exception:
            self.logging.logs_msg(f'Таблица: {self.table_us}, ошибка при изменении ячейки: {traceback.format_exc()}', 2)
            return

    def setColorOldRow(self, row, column):
        '''Закрашиваем предыдущую строку.'''
        try:
            for i in range(1, column):
                self.item(row, i).setBackground(QColor(240, 240, 240))
                self.item(row, i).setForeground(QColor(0, 0, 0))
        except Exception:
            return

    def setColorNewRow(self, row, column):
        '''Закрашиваем выделенную строку.'''
        try:
            for j in range(1, column):
                self.item(row, j).setBackground(QColor(0, 120, 215))
                self.item(row, j).setForeground(QColor(255, 255, 255))
        except Exception:
            return


class TableWidgetLinks(QTableWidget):
    '''Макет таблицы для работы с ссылками'''
    def __init__(self, parent=None):
        super(TableWidgetLinks, self).__init__(parent)

        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setColumnCount(3)

        tabl = ['№', 'Тэг', 'Название']
        self.setHorizontalHeaderLabels(tabl)

        style = "::section {""background-color: #bbbabf; }"
        self.horizontalHeader().setStyleSheet(style)

    def row_count(self) -> int:
        '''Кол-во строк в таблице.'''
        return self.rowCount()

    def data_cell(self):
        '''Текущая позиция ячейки.'''
        return self.currentRow(), self.currentColumn()

    def tw_clear_lines(self, rowcount: int):
        """Очистка таблицы виджета QTableWidget.

        Args:
            rowcount (int): кол-во строк
        """
        if not rowcount:
            while rowcount >= 0:
                self.removeRow(rowcount)
                rowcount -= 1

    def filling_table(self, table_list):
        '''Заполнение таблицы данными.'''
        self.setRowCount(len(table_list))

        for row_t in range(len(table_list)):
            for column_t in range(3):
                value = table_list[row_t][column_t]

                if value is None:
                    item = QTableWidgetItem('')
                else:
                    item = QTableWidgetItem(str(value))
                self.setItem(row_t, column_t, item)


class ComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super(ComboBox, self).__init__(*args, **kwargs)
        self.setStyleSheet('''
                           background: #f0f0f0;
                           padding: 0px;
                           font: 15px consolas;''')


class PushButton(QPushButton):
    '''Конструктор класса кнопки.'''
    def __init__(self, text: str, color: str, parent=None):
        super(PushButton, self).__init__(parent)

        self.text = text

        self.setText(self.text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("*{"
                           "font:13px times;"
                           "border: 1px solid #a19f9f;"
                           "border-radius: 4px;"
                           f"background: {color};"
                           "padding: 4px;}"
                           "*:hover{"f"background:'#e0e0e0';""color:'black'}"
                           "*:pressed{background: '#e0e0e0'}")


class LineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super(LineEdit, self).__init__(*args, **kwargs)

        self.setStyleSheet('''
                           font:13px times;
                           border: 1px solid #666665;
                           border-radius: 4px;
                           padding: 4px;''')


class WindowContexMenuSQL(QMainWindow):
    '''Отдельная форма для работы с ссылками.'''
    def __init__(self):
        super(WindowContexMenuSQL, self).__init__()

        self.setWindowTitle('Ссылки')
        self.setStyleSheet("background-color: #e1e5e5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.resize(ConstSize.CONTEXT_W.value,
                    ConstSize.CONTEXT_H.value)

        self.editSQL = Editing_SQL()

    def initObject(self, parent):
        '''Инициализация объектов макета.'''
        self.parent = parent
        self.tw_links = TableWidgetLinks(self)
        self.combo_table = ComboBox(self)
        self.combo_type = ComboBox(self)
        open_table = PushButton('Открыть таблицу', '#bfd6bf')
        confirm = PushButton('  Добавить  ', '#bfd6bf')
        self.req_base = LineEdit(self,
                                 placeholderText='Поиск сигнала',
                                 clearButtonEnabled=True)
        self.link_value = LineEdit(self,
                                   placeholderText='Значение ссылки',
                                   clearButtonEnabled=True)
        self.data_load = QLabel('', self)

        # Events
        open_table.clicked.connect(self.open_tabl)
        confirm.clicked.connect(self.broadcast_text)
        self.req_base.textChanged.connect(self.search_text)
        self.tw_links.cellClicked.connect(self.click_position)

        [self.combo_table.addItem(value1) for value1, value2 in USED_TABLE]

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.layout_g_top = QGridLayout()
        self.layout_g_top.addWidget(self.combo_table, 0, 0)
        self.layout_g_top.addWidget(open_table, 0, 1)
        self.layout_g_top.addWidget(self.combo_type, 0, 2)
        self.layout_g_top.addWidget(self.req_base, 0, 3, 1, 3)

        self.layout_g_bottom = QGridLayout()
        self.layout_g_bottom.addWidget(self.data_load, 0, 0)
        self.layout_g_bottom.addWidget(self.link_value, 0, 1)
        self.layout_g_bottom.addWidget(confirm, 0, 2)

        self.layout_v = QVBoxLayout(self.centralwidget)
        self.layout_v.addLayout(self.layout_g_top)
        self.layout_v.addWidget(self.tw_links)
        self.layout_v.addLayout(self.layout_g_bottom)

    def open_tabl(self):
        '''Событие по нажатию кнопки открыть таблицу.'''
        name_table = self.combo_table.currentText()
        rowcount = self.tw_links.row_count()
        self.tw_links.tw_clear_lines(rowcount)

        need_open = ''.join([table for desc, table in USED_TABLE if desc == name_table])

        self.list_signal, msg, color = self.editSQL.dop_window_signal(need_open)

        self.data_load.setText(msg)
        self.data_load.setStyleSheet(f"background-color: {color}")

        self.tw_links.filling_table(self.list_signal)

        self.combo_type.clear()
        [self.combo_type.addItem(str(i)) for table, sign in LIST_TYPE.items() for i in sign if table == name_table]

    def search_text(self):
        '''Поиск сигналов в таблице по запросу.'''
        request = self.req_base.text()
        if request == '':
            return

        rowcount = self.tw_links.row_count()
        self.tw_links.tw_clear_lines(rowcount)

        list_filter = self.editSQL.filter_text(request, self.list_signal)
        self.tw_links.filling_table(list_filter)

    def click_position(self):
        '''Отработка действий по клику.'''
        row, column = self.tw_links.data_cell()

        try:
            value_cell = self.tw_links.item(row, 0).text()
            value_cell_ktpra = self.tw_links.item(row, 1).text()

            if column == 0:
                self.link_value.setText(str(row + 1))
            else:
                if self.combo_table.currentText() in ['ctrlDO', 'AO',
                                                      'AIVisualValue',
                                                      'ctrlAO', 'BUFr']:
                    self.link_value.setText(f'{self.combo_table.currentText()}[{value_cell}]')
                elif self.combo_table.currentText() == 'Facility':
                    self.link_value.setText(f'{self.combo_table.currentText()}[].{self.combo_type.currentText()}')
                elif self.combo_table.currentText() == 'KTPRA':
                    self.link_value.setText(f'{value_cell_ktpra}.{self.combo_table.currentText()}')
                else:
                    self.link_value.setText(f'{self.combo_table.currentText()}[{value_cell}].{self.combo_type.currentText()}')
        except Exception:
            return

    def broadcast_text(self):
        '''Передача текста в родительский объект.'''
        self.parent.update_text(self.link_value.text())


class WindowTypeTableSQL(QMainWindow):
    """Отдельно окно с типами столбцов, применяемое для запроса."""
    def __init__(self, table_list):
        super(WindowTypeTableSQL, self).__init__()

        self.setWindowTitle('Тип столбцов таблицы')
        self.setStyleSheet("background-color: #e1e5e5;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(ConstSize.WIN_SIZE_TYPETABLE_W.value,
                    ConstSize.WIN_SIZE_TYPETABLE_H.value)

        self.t_w = QTableWidget(self)
        self.t_w.verticalHeader().setVisible(False)
        self.t_w.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.t_w.setColumnCount(3)
        self.t_w.setFocusPolicy(Qt.NoFocus)
        self.t_w.setRowCount(len(table_list))
        column = ['Имя_eng', 'Имя_rus', 'Тип']
        self.t_w.setHorizontalHeaderLabels(column)
        style = "::section {""background-color: #bbbabf; }"
        self.t_w.horizontalHeader().setStyleSheet(style)

        for row_t in range(len(table_list)):
            for column_t in range(3):
                item = QTableWidgetItem(table_list[row_t][column_t])
                item.setFlags(Qt.ItemIsEnabled)
                self.t_w.setItem(row_t, column_t, item)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.layout_v = QVBoxLayout(self.centralwidget)
        self.layout_v.addWidget(self.t_w)


class MainWindow(QMainWindow):
    def __init__(self, bd_connect, active_table: str):
        super(MainWindow, self).__init__()

        # Инициализация окна
        self._init_window()
        # Инициализация атрибутов
        self._init_attributes(bd_connect, active_table)
        # Создание виджетов
        self._create_widgets()
        # Настройка событий
        self._setup_events()
        # Компоновка интерфейса
        self._setup_layout()
        # Логирование запуска
        self.logsTextEdit.logs_msg('Редактор базы данных запущен', 1)
        self.logsTextEdit.logs_msg(f'Открыта таблица: {self.table_us}', 0)

    def _init_window(self):
        """Инициализация основных параметров окна."""
        self.setWindowTitle('Редактор базы данных')
        self.setStyleSheet("background-color: #f0f0f0;")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(ConstSize.WIN_SIZE_MAIN_W.value,
                    ConstSize.WIN_SIZE_MAIN_H.value)

    def _init_attributes(self, bd_connect, active_table):
        """Инициализация атрибутов класса."""
        self.bd_manager = bd_connect.tab_1
        self.table_us = self.table_old = active_table
        self.editSQL = Editing_SQL(self.table_us)
        self.old_row_1 = self.old_row_2 = 0
        self.fl_actives_windows = 0

    def _create_widgets(self):
        """Создание всех виджетов."""
        self.logsTextEdit = LogsTextEdit(self)
        self.logsTextEdit.setStyleSheet('''
                                        font: 13px times;
                                        background-color: #f0f0f0;
                                        border-radius: 5px;
                                        border: 1px solid #a19f9f;''')

        self.tableWidget = TableWidget(self.editSQL, self.table_us, self.logsTextEdit, False, self.bd_manager)
        self.tableWidget_dub = TableWidget(self.editSQL, self.table_us, self.logsTextEdit, True, self.bd_manager)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.l_enter_req = LineEdit(self, placeholderText='Введите запрос', clearButtonEnabled=True)

        # Создание кнопок
        self.buttons = {
            'b_addrow': PushButton('Добавить строку', '#92c486'),
            'b_delrow': PushButton('Удалить строку', '#eb6574'),
            'b_cleartabl': PushButton('Очистить таблицу', '#f0f0f0'),
            'b_deltabl': PushButton('Удалить таблицу', '#f0f0f0'),
            'b_apply_query': PushButton('Применить запрос', '#92c486'),
            'b_reset_query': PushButton('Сбросить запрос', '#f0f0f0'),
            'b_type_data': PushButton('Тип данных таблицы', '#92c486'),
            'b_links': PushButton('Ссылки', '#faf5cd')
        }

    def _setup_events(self):
        """Настройка событий для кнопок и виджетов."""
        self.buttons['b_addrow'].clicked.connect(self.add_row)
        self.buttons['b_delrow'].clicked.connect(self.delete_row)
        self.buttons['b_cleartabl'].clicked.connect(self.clear_table)
        self.buttons['b_deltabl'].clicked.connect(self.drop_table)
        self.buttons['b_apply_query'].clicked.connect(self.apply_query)
        self.buttons['b_reset_query'].clicked.connect(self.reset_query)
        self.buttons['b_type_data'].clicked.connect(self.type_table)
        self.buttons['b_links'].clicked.connect(self.link_table)

        self.tableWidget.selectionModel().selectionChanged.connect(lambda: self.on_change(1))
        self.tableWidget_dub.selectionModel().selectionChanged.connect(lambda: self.on_change(2))
        self.tableWidget.verticalScrollBar().valueChanged.connect(self.synh_position)
        self.tableWidget_dub.verticalScrollBar().valueChanged.connect(self.synh_position)

    def _setup_layout(self):
        """Компоновка интерфейса."""
        self.layout_g = QGridLayout()
        self.layout_g.addWidget(self.buttons['b_addrow'], 0, 0)
        self.layout_g.addWidget(self.buttons['b_delrow'], 1, 0)
        self.layout_g.addWidget(self.buttons['b_cleartabl'], 0, 3)
        self.layout_g.addWidget(self.buttons['b_deltabl'], 1, 3)
        self.layout_g.addWidget(self.buttons['b_links'], 1, 4)
        self.layout_g.addWidget(self.l_enter_req, 0, 5, 1, 3)
        self.layout_g.addWidget(self.buttons['b_apply_query'], 1, 5)
        self.layout_g.addWidget(self.buttons['b_reset_query'], 1, 6)
        self.layout_g.addWidget(self.buttons['b_type_data'], 1, 7)

        self.splitter_h = QSplitter(Qt.Horizontal)
        self.splitter_h.addWidget(self.tableWidget_dub)
        self.splitter_h.addWidget(self.tableWidget)
        width = self.tableWidget_dub.width_column()
        self.splitter_h.setSizes([width, ConstSize.WIN_SIZE_MAIN_W.value - width])

        self.splitter_v = QSplitter(Qt.Vertical)
        self.splitter_v.addWidget(self.splitter_h)
        self.splitter_v.addWidget(self.logsTextEdit)
        self.splitter_v.setSizes(ConstSize.SIZE_SPLITTER.value)

        self.layout_v = QVBoxLayout(self.centralwidget)
        self.layout_v.addLayout(self.layout_g)
        self.layout_v.addWidget(self.splitter_v)

    def on_change(self, num_active: bool):
        '''Активность окна 1 и подкраска строки виджета с левой стороны'''
        count_column = self.tableWidget.column_count_tabl()
        column = self.editSQL.exist_check_int(
            self.editSQL.read_json(self.bd_manager.connect.path_rus_text),
            self.table_us)

        if num_active == 1:
            self.fl_actives_windows = 1
            # Подкраска с левой стороны
            self.tableWidget_dub.blockSignals(True)
            self.tableWidget.blockSignals(True)
            current_row = self.tableWidget.currentRow()

            self.tableWidget_dub.setColorOldRow(self.old_row_2, column)
            self.tableWidget.setColorOldRow(self.old_row_2, count_column)
            self.tableWidget_dub.setColorOldRow(self.old_row_1, column)
            self.tableWidget.setColorOldRow(self.old_row_1, count_column)

            self.tableWidget_dub.setColorNewRow(current_row, column)
            self.tableWidget.setColorNewRow(current_row, count_column)

            self.old_row_2 = self.tableWidget.currentRow()
        else:
            '''Активность окна 2 и подкраска строки виджета с правой стороны.'''
            self.fl_actives_windows = 2
            # Подкраска с правой стороны
            self.tableWidget.blockSignals(True)
            self.tableWidget_dub.blockSignals(True)
            current_row = self.tableWidget_dub.currentRow()

            self.tableWidget.setColorOldRow(self.old_row_1, count_column)
            self.tableWidget_dub.setColorOldRow(self.old_row_1, column)
            self.tableWidget.setColorOldRow(self.old_row_2, count_column)
            self.tableWidget_dub.setColorOldRow(self.old_row_2, column)

            self.tableWidget.setColorNewRow(current_row, count_column)
            self.tableWidget_dub.setColorNewRow(current_row, column)

            self.old_row_1 = self.tableWidget_dub.currentRow()

        self.tableWidget_dub.blockSignals(False)
        self.tableWidget.blockSignals(False)

    def type_table(self):
        '''Запуск нового окна для просмотра типа столбцов.'''
        inf_data = self.bd_manager.db_dev.execute_query(f"""
                                                    SELECT column_name, data_type
                                                    FROM information_schema.columns
                                                    WHERE table_schema = 'public' AND
                                                    table_name = '{self.table_us}'""")
        path_rus_text = self.bd_manager.connect.path_rus_text
        type_list = self.editSQL.type_column(inf_data, path_rus_text)

        self.type_tabl = WindowTypeTableSQL(type_list)
        self.type_tabl.show()

    def link_table(self):
        '''Создание и запуск нового окна - Ссылки.'''
        self.link_tabl = WindowContexMenuSQL()
        self.link_tabl.initObject(self)
        self.link_tabl.show()

    def synh_position(self, index):
        '''Синхронное перелистывание текста по вертикали.'''
        self.tableWidget.verticalScrollBar().setValue(index)
        self.tableWidget_dub.verticalScrollBar().setValue(index)

    def add_row(self):
        '''Добавляем новые строки в объекты.'''
        rowcount = self.tableWidget.row_count_tabl()

        value = 0
        if rowcount:
            value = self.tableWidget.text_cell(rowcount - 1, 0)
        sum_cell = int(value) + ConstSize.COUNT_ONE.value

        self.bd_manager.db_dev.query_no_return(f'''INSERT INTO "{self.table_us}" (id) VALUES ({sum_cell});''')
        self.tableWidget.insertRow(rowcount)
        self.tableWidget.setItem(rowcount, 0, QTableWidgetItem(f'{sum_cell}'))
        self.tableWidget_dub.insertRow(rowcount)
        self.tableWidget_dub.setItem(rowcount, 0, QTableWidgetItem(f'{sum_cell}'))

        self.logsTextEdit.logs_msg(f'Строка {sum_cell} добавлена в конец таблицы', 0)

    def delete_row(self):
        '''Удаляем выбранную строку.'''
        if self.fl_actives_windows == 1:
            row, column = self.tableWidget.data_cell()
        else:
            row, column = self.tableWidget_dub.data_cell()

        if (row == -1) and (column == -1):
            self.logsTextEdit.logs_msg('Выбери строку для удаления', 2)
            return
        if self.fl_actives_windows == 1:
            value_id = self.tableWidget.text_cell(row, 0)
        else:
            value_id = self.tableWidget_dub.text_cell(row, 0)

        self.bd_manager.db_dev.query_no_return(f"""DELETE FROM "{self.table_us}" WHERE id={value_id}""")
        self.tableWidget.removeRow(row)
        self.tableWidget.selectionModel().clearCurrentIndex()
        self.tableWidget_dub.removeRow(row)
        self.tableWidget_dub.selectionModel().clearCurrentIndex()

        self.logsTextEdit.logs_msg(f'Строка {value_id} удалена', 3)

    def clear_table(self):
        '''Удаления всех данных таблицы, без столбцов.'''
        rowcount = self.tableWidget.row_count_tabl()
        if rowcount == 0:
            self.logsTextEdit.logs_msg('Таблица пустая', 3)
            return
        while rowcount >= 0:
            self.tableWidget.removeRow(rowcount)
            self.tableWidget_dub.removeRow(rowcount)
            rowcount -= 1

        self.bd_manager.db_dev.query_no_return(f'DELETE FROM "{self.table_us}"')
        self.l_enter_req.clear()
        self.logsTextEdit.logs_msg('Таблица полностью очищена', 3)

    def drop_table(self):
        '''Удаление таблицы из базы данных.'''
        self.bd_manager.db_dev.query_no_return(f'DROP TABLE "{self.table_us}"')
        self.close()

    def size_widget(self):
        width = self.tableWidget_dub.width_column()
        self.splitter_h.setSizes([width, ConstSize.WIN_SIZE_MAIN_W.value - width])
        self.splitter_v.setSizes(ConstSize.SIZE_SPLITTER.value)

    def column_table(self, table: str, hat_name, query_column):
        if query_column[0] == '*':
            column_used = self.bd_manager.db_dev.execute_query_desc(f'SELECT * FROM "{table}" ORDER BY id')
        else:
            column_used = hat_name
        return column_used

    def apply_query(self):
        """Рукописный запрос к базе SQL."""

        rowcount = self.tableWidget.row_count_tabl()
        request = self.l_enter_req.text()

        if not len(self.l_enter_req.text()):
            self.logsTextEdit.logs_msg('Пустой запрос', 2)
            return

        try:
            value = self.bd_manager.db_dev.execute_query(f'''{request}''')
            hat_name = self.bd_manager.db_dev.execute_query_desc(f'''{request}''')

            query_table = Parser(f'''{request}''').tables
            query_column = Parser(f'''{request}''').columns
            name_column = [column[0] for column in hat_name]

            table_used = query_table[0]

            path_rus_text = self.bd_manager.connect.path_rus_text

            dict_rus = self.editSQL.exist_check_array(self.editSQL.read_json(path_rus_text), table_used)
            russ_name = self.editSQL.russian_name_column(dict_rus, self.column_table(table_used, hat_name, query_column))
            end = self.editSQL.exist_check_int(self.editSQL.read_json(path_rus_text), table_used)

            count_column = len(name_column)
            count_row = len(value)

            if count_column == 'error':
                return

            self.table_us = table_used

            self.tableWidget.table_us = table_used
            self.tableWidget.tw_clear_lines(rowcount)
            self.tableWidget.blockSignals(True)
            self.tableWidget.init_table(count_column, count_row, russ_name, value, end)

            self.tableWidget_dub.table_us = table_used
            self.tableWidget_dub.tw_clear_lines(rowcount)
            self.tableWidget_dub.blockSignals(True)

            end_dub = 0 if not end else end + 1
            self.tableWidget_dub.init_table(count_column, count_row, russ_name, value, end_dub)
            self.size_widget()

            self.logsTextEdit.logs_msg(f'Открыта таблица {table_used}', 1)
        except Exception:
            self.logsTextEdit.logs_msg(f'Ошибка запроса {traceback.format_exc()}', 1)

    def reset_query(self):
        '''Сброс запроса и возврат таблицы к состоянию до запроса.'''
        rowcount = self.tableWidget.row_count_tabl()

        self.table_us = self.table_old

        self.tableWidget.table_us = self.table_us
        self.tableWidget_dub.table_us = self.table_us

        self.tableWidget.tw_clear_lines(rowcount)
        self.tableWidget_dub.tw_clear_lines(rowcount)

        column, row, hat_name, value, end = self.tableWidget.object_data_table()
        self.tableWidget.blockSignals(True)
        self.tableWidget_dub.blockSignals(True)

        self.tableWidget.init_table(column, row, hat_name, value, end)
        self.tableWidget_dub.init_table(column, row, hat_name, value, end)
        self.size_widget()
        self.logsTextEdit.logs_msg(f'Открыта таблица: {self.table_us}', 2)

    def update_text(self, text=None):
        '''Обновление текста из окна ссылки.'''
        if self.fl_actives_windows == 1:
            self.tableWidget.value_change(text)
        else:
            self.tableWidget_dub.value_change(text)