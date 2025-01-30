import sys
import traceback
from psycopg2 import Error
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QCheckBox
from connect_log.logging_text import LogsTextEdit
from window_editing import MainWindow as WinEditing
from general_functions import General_functions as DopFunction
from create_database.new_db import NewDB
from model import connect
from model import db
from model import db_prj
from model import Signals
from excel.workingKD import Import_in_SQL
from request_sql import RequestSQL
# from hmi_defence import DefenceMap
# from hmi_uso import DaignoPicture
# from hmi_siren import Alarm_map
# from txt_trends import TreeTrends
# from map_address import AnalogsMap
# from map_address import DiskretsMap
# from map_address import VSMap
# from map_address import ZDMap
# from map_address import PumpsMap
# from map_address import UtsUptsMap
# from map_address import PicturesMap
# from map_address import KTPRMap
# from map_address import KTPRAMap
# from map_address import GMPNAMap
# from map_address import PIMap
# from map_address import PZMap
# from map_address import RelaytedSystemMap
# from map_address_diag import DiagMap
# from map_address_diag import RackStateMap
# from omx_object import AnalogsOmx
# from omx_object import DiskretsOmx
# from omx_object import VSOmx
# from omx_object import ZDOmx
# from omx_object import NAOmx
# from omx_object import UtsUptsOmx
# from omx_object import PIOmx
# from omx_object import PZOmx
# from omx_object import PICOmx
# from omx_object import SSOmx
# from omx_object import KTPROmx
# from omx_object import KtpraGmpnaOmx
# from omx_object import DIAGOmx
# from omx_object import AttrDIAGOmx


SIZE_WORK_BACK = (1002, 500)
SIZE_SPLIT_V = [500, 150]
SIZE_SPLIT_H = [602, 40]


class EditTabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super(EditTabWidget, self).__init__(*args, **kwargs)
        self.setStyleSheet("""QTabWidget::pane {
                           border: 1px solid #a19f9f;
                           border-bottom-left-radius: 5;
                           border-bottom-right-radius: 5;
                           padding: 10px;}
                           QTabBar::tab{
                           min-width: 227px;
                           min-height: 20;
                           font: 13px times;}
                           QTabBar::tab:selected{
                           color: rgb(0, 0, 0);
                           background: #dbcaba}
                           """)


class TabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super(QTabWidget, self).__init__(*args, **kwargs)
        self.setStyleSheet("""QTabWidget::pane {
                           border: 1px solid #a19f9f;
                           border-bottom-left-radius: 5;
                           border-bottom-right-radius: 5;
                           padding: 10px;
                           margin-top: 1px;}
                           QTabBar::tab{
                           min-width:124px;
                           min-height:20;
                           font:13px times;}
                           QTabBar::tab:selected{
                           color:rgb(0, 0, 0);
                           background: #dbcaba}
                           """)


class CheckBox(QCheckBox):
    '''Конструктор класса чекбокса.'''
    def __init__(self, *args, **kwargs):
        super(CheckBox, self).__init__(*args, **kwargs)
        self.setStyleSheet("""*{
                           font:14px times;
                           padding: 3px;
                           border-radius: 4
                           }""")


class PushButton(QPushButton):
    '''Конструктор класса кнопки.'''
    def __init__(self, *args, **kwargs):
        super(PushButton, self).__init__(*args, **kwargs)


class GenFormButton(QPushButton):
    '''Общий конструктор класса кнопки.'''
    def __init__(self, *args, **kwargs):
        super(GenFormButton, self).__init__(*args, **kwargs)
        self.setStyleSheet("""*{font:12px times;
                                border: 1px solid #a19f9f;
                                min-height: 18;
                                padding: 4px; border-radius: 4}
                                *:hover{background:#e0e0e0;
                                        color:'black'}
                                *:pressed{background: '#e0e0e0'}""")


class LineEdit(QLineEdit):
    '''Общий конструктор строки заполнения.'''
    def __init__(self, *args, **kwargs):
        super(LineEdit, self).__init__(*args, **kwargs)
        self.setStyleSheet("""*{
                                background-color: #f0f0f0;
                                font:13px times;
                                border: 1px solid #a19f9f;
                                padding: 4px; border-radius: 4}""")


class Label(QLabel):
    '''Конструктор класса кнопки.'''
    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.fl_connect_bd = False

        self.setStyleSheet('''
                           background-color: #eb6574;
                           border: 1px solid #a19f9f;
                           border-radius:4; padding: 4px;
                           font:13px times;''')

    def connect_true(self):
        self.setStyleSheet('''
                           background-color: #7ce063;
                           border: 1px solid #a19f9f;
                           border-radius: 4; padding: 4px;
                           font:13px times;''')

    def connect_false(self):
        self.setStyleSheet('''
                           background-color: #eb6574;
                           border: 1px solid #a19f9f;
                           border-radius: 4; padding: 4px;
                           font:13px times;''')


class LabelSimple(QLabel):
    '''Конструктор класса кнопки.'''
    def __init__(self, *args, **kwargs):
        super(LabelSimple, self).__init__(*args, **kwargs)
        self.setStyleSheet('''font:12px times; background: #a3d6d0;
                           padding: 2px; border-radius: 3''')
        self.setAlignment(Qt.AlignCenter)


class ElementSignature(QLabel):
    '''Конструктор класса текста.
    Подаись элемента виджета'''
    def __init__(self, *args, **kwargs):
        super(ElementSignature, self).__init__(*args, **kwargs)
        self.setStyleSheet("""*{font:13px times;
                        padding: 2px; border-radius: 3}""")

    def label(self):
        self.setStyleSheet("""*{font:13px times;
                        background: #dbcaba;
                        padding: 2px; border-radius: 3}""")


class LabelHMI(QLabel):
    '''Конструктор класса текста.
    Подпись элемента виджета'''
    def __init__(self, *args, **kwargs):
        super(LabelHMI, self).__init__(*args, **kwargs)
        self.setStyleSheet('''border-radius: 4;
                              padding: 0px;
                              font: 16px times;''')
        self.setAlignment(Qt.AlignCenter)


class GenProject(QWidget):
    def __init__(self, parent=None):
        super(GenProject, self).__init__(parent)


class ComboBox(QComboBox):
    def __init__(self, text):
        super(ComboBox, self).__init__()
        self.setEditable(True)
        self.setCurrentIndex(-1)
        self.setCurrentText(text)
        self.setMinimumContentsLength(22)
        self.setStyleSheet('''
                           padding: 4px;
                           border: 1px solid #a19f9f;
                           font: 13px times;''')

    def color_red(self):
        self.setStyleSheet('''
                            color: red;
                            padding: 4px;
                            border: 1px solid #a19f9f;
                            font: 13px times;''')

    def color_green(self):
        self.setStyleSheet('''
                            color: green;
                            padding: 4px;
                            border: 1px solid #a19f9f;
                            font: 13px times;''')


# Построение редактора SQL
class EditWindows(QWidget):
    '''Конструктор класса редактирования окна разработки.'''
    def __init__(self, logtext, parent=None):
        super(EditWindows, self).__init__(parent)

        self.parent = parent
        self.logsTextEdit = logtext
        layout_v = QVBoxLayout(self)

        self.combo_choise_tabl = ComboBox('Обнови список таблиц')
        self.button_connect_1 = GenFormButton('Окно редактора №1')
        self.button_connect_2 = GenFormButton('Окно редактора №2')
        self.button_update = GenFormButton('Обновить список')

        self.button_update.setToolTip('Обновление списка таблиц после изменения БД')

        self.button_connect_1.clicked.connect(self.open_window1)
        self.button_connect_2.clicked.connect(self.open_window2)
        self.button_update.clicked.connect(self.update_list)

        layout_v.addWidget(self.combo_choise_tabl)
        layout_v.addWidget(self.button_connect_1)
        layout_v.addWidget(self.button_connect_2)
        layout_v.addStretch()
        layout_v.addWidget(self.button_update)

    def open_window1(self):
        '''Выполнение по клику кнопки.
        Открытие окна редактирования БД 1.'''
        name_table = self.combo_choise_tabl.currentText()

        if name_table == 'Выбери таблицу':
            self.logsTextEdit.logs_msg('Не выбрана таблица для открытия окна для редактирования базы данных!', 2)
            return
        try:
            self.open_w1 = WinEditing(name_table)
            self.open_w1.show()
            self.logsTextEdit.logs_msg(f'''Открыто окно для редактирования базы данных №1.\n
                                        Таблица: {name_table}''', 1)
        except Exception:
            self.logsTextEdit.logs_msg('''Невозможно подключиться к таблице.
                                       Нет подключения к БД разработки''', 2)

    def open_window2(self):
        '''Выполнение по клику кнопки.
        Открытие окна редактирования БД 2.'''
        name_table = self.combo_choise_tabl.currentText()

        if name_table == 'Выбери таблицу':
            self.logsTextEdit.logs_msg('Не выбрана таблица для открытия окна для редактирования базы данных!', 2)
            return
        try:
            self.open_w2 = WinEditing(name_table)
            self.open_w2.show()
            self.logsTextEdit.logs_msg(f'''Открыто окно для редактирования базы данных №2.\n
                                        Таблица: {name_table}''', 1)
        except Exception:
            self.logsTextEdit.logs_msg('''Невозможно подключиться к таблице.
                                       Нет подключения к БД разработки''', 2)

    def update_list(self):
        '''Функция обновляет список таблиц по команде.'''
        try:
            self.parent.tab_1.connect_devSQL()
        except Exception:
            self.logsTextEdit.logs_msg('''Невозможно обновить список.
                                       Нет подключения к БД разработки''', 2)
            self.combo_choise_tabl.clear()
            self.combo_choise_tabl.addItem('Выбери таблицу')
            return

        list_table = db.get_tables()
        self.combo_choise_tabl.clear()
        for table in list_table:
            self.combo_choise_tabl.addItem(str(table))
        self.logsTextEdit.logs_msg('Список таблиц обновлен', 1)


# Главная страница. Подключение к БД
class TabConnect(QWidget):
    '''Конструктор класса. Проверка и подключение к БД.'''
    def __init__(self, logtext, parent=None):
        super(TabConnect, self).__init__(parent)

        self.logsTextEdit = logtext
        self.parent = parent
        self.dop_function = DopFunction()

        layout_v1 = QVBoxLayout()
        layout_v2 = QVBoxLayout()
        layout_v3 = QVBoxLayout()
        layout_h1 = QHBoxLayout()
        layout_h2 = QHBoxLayout(self)
        # Подписи
        label_dev_sign = ElementSignature('\tБаза данных разработки\t')
        label_dev_sign.label()
        label_dev_database = ElementSignature(f'Название:         {connect.database}')
        label_dev_user = ElementSignature(f'Пользователь:  {connect.user}')
        label_dev_pwd = ElementSignature(f'Пароль:            {connect.password}')
        label_dev_host = ElementSignature(f'Адрес:              {connect.host}')
        label_dev_port = ElementSignature(f'Порт:                {connect.port}')

        label_prj_sign = ElementSignature('\tБаза данных проекта\t\t')
        label_prj_sign.label()
        label_prj_database = ElementSignature(f'Название:         {connect.database_msg}')
        label_prj_user = ElementSignature(f'Пользователь:  {connect.user_msg}')
        label_prj_pwd = ElementSignature(f'Пароль:            {connect.password_msg}')
        label_prj_host = ElementSignature(f'Адрес:              {connect.host_msg}')
        label_prj_port = ElementSignature(f'Порт:                {connect.port_msg}')
        # Кнопки
        self.button_connect_devSQL = GenFormButton('Подключиться к БД')
        self.button_connect_devSQL.setToolTip('Подключение к БД разработки')
        self.button_connect_prjSQL = GenFormButton('Подключиться к БД')
        self.button_connect_prjSQL.setToolTip('Подключение к БД проекта')
        self.button_disconnect_devSQL = GenFormButton('Отключиться от БД')
        self.button_disconnect_prjSQL = GenFormButton('Отключиться от БД')
        self.button_connect_devSQL.clicked.connect(self.connect_devSQL)
        self.button_connect_prjSQL.clicked.connect(self.connect_prjSQL)
        self.button_disconnect_devSQL.clicked.connect(self.disconnect_devSQL)
        self.button_disconnect_prjSQL.clicked.connect(self.disconnect_prjSQL)
        # Новая БД
        label_newBD_1 = ElementSignature('Новый шаблон SQL БД разработки\t')
        label_newBD_1.label()
        self.button_newDB = GenFormButton('Создать базу данных')
        self.button_newDB.setToolTip('''Создается новая БД вместе с пустыми таблицами под определенную систему(МНС, ПТ и тд.).\nНазвание БД берется из файла init_conf.cfg в разделе [SQL] - database''')
        self.button_newDB.clicked.connect(self.clicked_newDB)
        self.checkbox_sys_mns = CheckBox('МНС')
        self.checkbox_sys_pt = CheckBox('ПТ')

        layout_v1.addWidget(label_dev_sign)
        layout_v1.addWidget(label_dev_database)
        layout_v1.addWidget(label_dev_user)
        layout_v1.addWidget(label_dev_pwd)
        layout_v1.addWidget(label_dev_host)
        layout_v1.addWidget(label_dev_port)
        layout_v1.addWidget(self.button_connect_devSQL)
        layout_v1.addWidget(self.button_disconnect_devSQL)
        layout_v1.addStretch()

        layout_v2.addWidget(label_prj_sign)
        layout_v2.addWidget(label_prj_database)
        layout_v2.addWidget(label_prj_user)
        layout_v2.addWidget(label_prj_pwd)
        layout_v2.addWidget(label_prj_host)
        layout_v2.addWidget(label_prj_port)
        layout_v2.addWidget(self.button_connect_prjSQL)
        layout_v2.addWidget(self.button_disconnect_prjSQL)
        layout_v2.addStretch()

        layout_h1.addStretch()
        layout_h1.addWidget(self.checkbox_sys_mns)
        layout_h1.addWidget(self.checkbox_sys_pt)
        layout_h1.addStretch()

        layout_v3.addWidget(label_newBD_1)
        layout_v3.addLayout(layout_h1)
        layout_v3.addWidget(self.button_newDB)
        layout_v3.addStretch()

        layout_h2.addLayout(layout_v1)
        layout_h2.addLayout(layout_v2)
        layout_h2.addLayout(layout_v3)
        layout_h2.addStretch()

    def connect_devSQL(self):
        '''Обработка клика по подключению к БД разработки.'''
        # Флаг подклюбчения к базе разработки
        if self.parent.connect_SQL_edit.fl_connect_bd:
            return

        try:
            db.init(str(connect.database).lower(),
                    user=connect.user,
                    password=connect.password,
                    host=connect.host,
                    port=connect.port)
            if not self.dop_function.exist_check_db(str(connect.database).lower(),
                                                    connect.user,
                                                    connect.password,
                                                    connect.host,
                                                    connect.port):
                raise Exception('Проверь даннные для подключения к БД')

            self.logsTextEdit.logs_msg('БД разработки: подключение установлено', 0)
            self.parent.connect_SQL_edit.setText('Соединение с БД разработки установлено')
            self.parent.connect_SQL_edit.connect_true()
            self.parent.connect_SQL_edit.fl_connect_bd = True
        except (Exception, Error) as error:
            self.logsTextEdit.logs_msg(f'Ошибка поключения к БД разработки: {error}', 2)

    def disconnect_devSQL(self):
        '''Обработка клика по отключению БД разработки.'''
        try:
            db.init(None)
            self.logsTextEdit.logs_msg('БД разработки: подключение разорвано', 2)
            self.parent.connect_SQL_edit.setText('Соединение с БД разработки разорвано')
            self.parent.connect_SQL_edit.connect_false()
            self.parent.connect_SQL_edit.fl_connect_bd = False
        except (Exception, Error) as error:
            self.logsTextEdit.logs_msg(f'Ошибка: {error}', 2)

    def connect_prjSQL(self):
        '''Обработка клика по подключению к БД проекта.'''
        try:
            db_prj.init(connect.database_msg,
                        user=connect.user_msg,
                        password=connect.password_msg,
                        host=connect.host_msg,
                        port=connect.port_msg)

            if not self.dop_function.exist_check_db(connect.database_msg,
                                                    connect.user_msg,
                                                    connect.password_msg,
                                                    connect.host_msg,
                                                    connect.port_msg):
                raise Exception('Проверь даннные для подключения к БД')

            self.logsTextEdit.logs_msg('БД проекта: подключение установлено', 0)
            self.parent.connect_SQL_prj.setText('Соединение с БД проекта установлено')
            self.parent.connect_SQL_prj.connect_true()
        except (Exception, Error) as error:
            self.logsTextEdit.logs_msg(f'Ошибка поключения к БД проекта: {error}', 2)

    def disconnect_prjSQL(self):
        '''Обработка клика по отключению БД проекта.'''
        try:
            db_prj.init(None)
            self.logsTextEdit.logs_msg('БД проекта: подключение разорвано', 2)
            self.parent.connect_SQL_prj.setText('Соединение с БД проекта разорвано')
            self.parent.connect_SQL_prj.connect_false()
        except (Exception, Error) as error:
            self.logsTextEdit.logs_msg(f'Ошибка: {error}', 2)

    def clicked_newDB(self):
        '''Выбор системы и создание БД.'''
        obj_new_db = NewDB()
        if not self.checkbox_sys_mns.isChecked() and not self.checkbox_sys_pt.isChecked():
            self.logsTextEdit.logs_msg('Выбери систему для новой БД!', 3)
        if self.checkbox_sys_mns.isChecked():
            obj_new_db.create_new_base('MNS', self.logsTextEdit)
            self.connect_devSQL()
        if self.checkbox_sys_pt.isChecked():
            obj_new_db.create_new_base('PT', self.logsTextEdit)
            self.connect_devSQL()


# Импорт Excel
class ImportKD(QWidget):
    '''Проверка и подключение к БД.'''
    def __init__(self, logtext, parent=None):
        super(ImportKD, self).__init__(parent)

        self.logsTextEdit = logtext
        self.parent = parent
        self.dop_function = DopFunction()
        self.fl_connect = False
        self.fl_load_hat = False

        button_connectKD = GenFormButton('Подключить Excel')
        button_disconnectKD = GenFormButton('Отключить Excel')
        button_read_table = GenFormButton('Подключиться к таблице')
        button_read_table.setStyleSheet("""*{font:12px times; border: 2px solid #d68336;
                                            min-height: 18; padding: 4px; border-radius: 4}
                                            *:hover{background:#e0e0e0; color:'black'}
                                            *:pressed{background: '#e0e0e0'}""")
        button_clear_table = GenFormButton('Очистить таблицу')
        button_add_signals = GenFormButton('Добавить новые сигналы')
        button_update_signals = GenFormButton('Обновить сигналы')
        # Events buttons
        button_connectKD.clicked.connect(self.connectKD)
        button_disconnectKD.clicked.connect(self.disconnectKD)
        button_read_table.clicked.connect(self.read_table)
        button_clear_table.clicked.connect(self.clear_table)
        button_add_signals.clicked.connect(self.add_new_signals)
        button_update_signals.clicked.connect(self.update_signals)

        self.combo_choise_tabl = ComboBox('Шкаф')
        self.combo_choise_tabl.setStyleSheet('''padding: 4px;
                                                border: 2px solid #d68336;
                                                font: 13px times;''')
        self.combo_type = ComboBox('Выбери в списке')
        self.combo_shema = ComboBox('Выбери в списке')
        self.combo_basket = ComboBox('Выбери в списке')

        self.select_row = LineEdit(placeholderText='Номер строки заголовка',
                                   clearButtonEnabled=True)
        self.select_row.setStyleSheet("""*{background-color: #f0f0f0; font:13px times;
                                           border: 2px solid #d68336;
                                           padding: 4px; border-radius: 4}""")

        self.combo_tag = ComboBox('Выбери в списке')
        self.combo_klk = ComboBox('Выбери в списке')
        self.combo_module = ComboBox('Выбери в списке')

        self.combo_name = ComboBox('Выбери в списке')
        self.combo_kont = ComboBox('Выбери в списке')
        self.combo_channel = ComboBox('Выбери в списке')

        label_type = LabelSimple('Тип')
        label_schema = LabelSimple('Схема')
        label_basket = LabelSimple('Корзина')
        label_tag = LabelSimple('Тэг')
        label_klk = LabelSimple('Клеммник')
        label_modul = LabelSimple('Модуль')
        label_name = LabelSimple('Наименование')
        label_kont = LabelSimple('Контакт')
        label_channel = LabelSimple('Канал')

        layout_v0 = QVBoxLayout()
        layout_v1 = QVBoxLayout()
        layout_v2 = QVBoxLayout()
        layout_v3 = QVBoxLayout()
        layout_v4 = QVBoxLayout(self)
        layout_h1 = QHBoxLayout()
        layout_h2 = QHBoxLayout()

        layout_v0.addWidget(button_connectKD)
        layout_v0.addWidget(button_disconnectKD)
        layout_v0.addSpacing(107)
        layout_v0.addWidget(button_clear_table)
        layout_v0.addStretch()

        layout_v1.addWidget(self.combo_choise_tabl)
        layout_v1.addWidget(label_type)
        layout_v1.addWidget(self.combo_type)
        layout_v1.addWidget(label_schema)
        layout_v1.addWidget(self.combo_shema)
        layout_v1.addWidget(label_basket)
        layout_v1.addWidget(self.combo_basket)
        layout_v1.addStretch()

        layout_v2.addWidget(self.select_row)
        layout_v2.addWidget(label_tag)
        layout_v2.addWidget(self.combo_tag)
        layout_v2.addWidget(label_klk)
        layout_v2.addWidget(self.combo_klk)
        layout_v2.addWidget(label_modul)
        layout_v2.addWidget(self.combo_module)
        layout_v2.addStretch()

        layout_v3.addWidget(button_read_table)
        layout_v3.addWidget(label_name)
        layout_v3.addWidget(self.combo_name)
        layout_v3.addWidget(label_kont)
        layout_v3.addWidget(self.combo_kont)
        layout_v3.addWidget(label_channel)
        layout_v3.addWidget(self.combo_channel)
        layout_v3.addStretch()
        layout_v3.addSpacing(10)

        layout_h1.addLayout(layout_v0)
        layout_h1.addSpacing(15)
        layout_h1.addLayout(layout_v1)
        layout_h1.addLayout(layout_v2)
        layout_h1.addLayout(layout_v3)
        layout_h1.addStretch()

        layout_h2.addSpacing(380)
        layout_h2.addWidget(button_update_signals)
        layout_h2.addSpacing(60)
        layout_h2.addWidget(button_add_signals)
        layout_h2.addStretch()

        layout_v4.addLayout(layout_h1)
        layout_v4.addLayout(layout_h2)
        layout_v4.addStretch()

    def disconnectKD(self):
        try:
            if not self.fl_connect:
                raise
            self.connectKD.disconnect_exel()
        except Exception:
            self.logsTextEdit.logs_msg('''Импорт КД: соединение уже было разорвано''', 3)
            return

        self.fl_connect = False
        self.parent.connect_exel.connect_false()
        self.parent.connect_exel.setText('''Соединение с Exel разорвано''')
        self.logsTextEdit.logs_msg('Импорт КД: соединение c Exel разорвано', 2)

    def connectKD(self):
        '''Подключение к файлу КД(КЗФКП) формата Exel.'''
        try:
            self.connectKD = Import_in_SQL(connect.path_to_exel,
                                           self.logsTextEdit)
            hat_table = self.connectKD.read_table()
            self.combo_choise_tabl.clear()
            self.combo_choise_tabl.addItems(hat_table)
            self.logsTextEdit.logs_msg('''Импорт КД:
                                       соединение c Exel установлено''', 0)
            self.logsTextEdit.logs_msg('Импорт КД: названия шкафов обновлены', 0)
            self.parent.connect_exel.connect_true()
            self.parent.connect_exel.setText('''Соединение с Exel установлено''')
            self.fl_connect = True
        except Exception:
            self.logsTextEdit.logs_msg(f'''Импорт КД:
                                       ошибка поключения к файлу КД
                                       {traceback.format_exc()}''', 2)

    def read_table(self):
        '''Чтение шапки таблицы для определения позиции столбцов.'''
        name_uso = self.combo_choise_tabl.currentText()
        if not self.fl_connect:
            self.logsTextEdit.logs_msg('''Импорт КД: нет подключения к файлу Exel''', 2)
            return
        try:
            row = "".join(self.select_row.text().split())
            self.logsTextEdit.logs_msg(f'''Импорт КД: выбрано УСО: {name_uso}, номер строки: {int(row)}''', 1)
            self.fl_load_hat = True
        except Exception:
            self.logsTextEdit.logs_msg('''Импорт КД: некорректный номер строки''', 2)
            return

        self.fill_combobox(self.connectKD.read_hat_table(name_uso, row, False))

    def fill_combobox(self, hat_table: dict):
        '''Заполняем названиями столбцы для верного импорта сигналов.'''
        list_combobox = [(self.combo_type, 'тип'), (self.combo_shema, 'схема'), (self.combo_basket, 'корз'),
                         (self.combo_tag, 'tэг'), (self.combo_klk, 'клк'), (self.combo_kont, 'конт'),
                         (self.combo_module, 'мод'), (self.combo_name, 'наименование'), (self.combo_channel, 'кан')]

        name_uso = self.combo_choise_tabl.currentText()
        count_all = 0
        for struct in list_combobox:
            struct[0].addItems(hat_table)

            count_index = 0
            struct[0].setCurrentText('Найди в списке')
            struct[0].color_red()
            for title in hat_table:
                if struct[1] in str(title).lower():
                    struct[0].setCurrentIndex(count_index)
                    struct[0].color_green()
                    count_all += 1
                    break
                count_index += 1

        if count_all == len(list_combobox):
            self.logsTextEdit.logs_msg(f'''Импорт КД: заголовок нужного столбца найден в УСО: {name_uso}''', 0)
        else:
            self.logsTextEdit.logs_msg(f'''Импорт КД: заголовок нужного столбца
                                       не найден в УСО: {name_uso}. Укажите вручную!''', 2)

    def clear_table(self):
        '''Полная очистка(не удаление) таблицы Signals.'''
        try:
            reqsql = RequestSQL()
        except Exception:
            self.logsTextEdit.logs_msg('''Импорт КД:
                                       невозможно обновить список.
                                       Нет подключения к БД разработки''', 2)
            return

        list_tabl = reqsql.get_tabl()
        check_table = self.dop_function.check_in_table('signals', list_tabl)
        if check_table:
            reqsql.clear_table('signals')
            self.logsTextEdit.logs_msg('Импорт КД: таблица signals очищена', 1)
        else:
            reqsql.new_table(Signals)
            self.logsTextEdit.logs_msg('''Импорт КД:
                                       таблица signals создана в БД''', 1)

    def hat_list(self):
        dict_column = {'type_signal': self.combo_type.currentText(),
                       'uso': '',
                       'tag': self.combo_tag.currentText(),
                       'description': self.combo_name.currentText(),
                       'schema': self.combo_shema.currentText(),
                       'klk': self.combo_klk.currentText(),
                       'contact': self.combo_kont.currentText(),
                       'basket': self.combo_basket.currentText(),
                       'module': self.combo_module.currentText(),
                       'channel': self.combo_channel.currentText()}
        return dict_column

    def add_new_signals(self):
        '''Добавление нового шкафа с сигналами.'''
        if not self.fl_load_hat:
            self.logsTextEdit.logs_msg('''Импорт КД: необходимо подключиться к таблице''', 2)
            return
        name_uso = self.combo_choise_tabl.currentText()
        try:
            data_uso = self.connectKD.preparation_import(name_uso,
                                                         self.select_row.text(),
                                                         self.hat_list())
            self.connectKD.database_entry_SQL(data_uso, name_uso)

        except Exception:
            self.logsTextEdit.logs_msg(f'''Импорт КД: ошибка {traceback.format_exc()}''', 2)
            return

    def update_signals(self):
        '''Обновление сигналов у выбранного шкафа.'''
        if not self.fl_load_hat:
            self.logsTextEdit.logs_msg('''Импорт КД:
                                       необходимо подключиться к таблице''', 2)
            return
        name_uso = self.combo_choise_tabl.currentText()
        try:
            data_uso = self.connectKD.preparation_import(name_uso,
                                                         self.select_row.text(),
                                                         self.hat_list())
            self.connectKD.row_update_SQL(data_uso, name_uso)

        except Exception:
            self.logsTextEdit.logs_msg(f'''Импорт КД:
                                       ошибка {traceback.format_exc()}''', 2)
            return


# Заполнение SQL разработки
class DevSQL(QWidget):
    '''Заполнение и редактирование БД разработки.'''
    def __init__(self, logtext, parent=None):
        super(DevSQL, self).__init__(parent)


# Заполнение DevStudio
class GenHMIandDev(QWidget):
    '''Генерация ВУ HMI и DevStudio.'''
    def __init__(self, logtext, parent=None):
        super(GenHMIandDev, self).__init__(parent)
        self.logsTextEdit = logtext
        self.parent = parent
        self.dop_function = DopFunction()

        layout_v1 = QVBoxLayout(self)
        self.layout_v2 = QVBoxLayout()
        self.layout_v3 = QVBoxLayout()
        self.layout_v4 = QVBoxLayout()
        self.layout_v5 = QVBoxLayout()
        self.layout_v6 = QVBoxLayout()
        self.layout_v7 = QVBoxLayout()
        self.layout_h1 = QHBoxLayout()
        self.layout_h2 = QHBoxLayout()
        self.layout_h3 = QHBoxLayout()

        label_hmi_sign = LabelHMI('HMI')
        label_devstudio_sign = LabelHMI('DevStudio')
        label_textfile = LabelHMI('TextFile')

        self.object_hmi()
        self.object_devstudio()
        self.object_textfile()

        layout_v1.addWidget(label_hmi_sign)
        layout_v1.addLayout(self.layout_h1)
        layout_v1.addWidget(label_devstudio_sign)
        layout_v1.addLayout(self.layout_h2)
        layout_v1.addWidget(label_textfile)
        layout_v1.addLayout(self.layout_h3)
        layout_v1.addStretch()

    def object_hmi(self):
        '''Добавляем объекты для генерация HMI.'''
        self.select_row = LineEdit(placeholderText='Номер МА',
                                   clearButtonEnabled=True)
        self.select_row.setMaximumSize(135, 100)
        self.select_row.setValidator(QIntValidator())
        self.select_row.setToolTip('''Если необходимо собрать\nзашиты или готовности по конкретному МА,\nто укажи номер''')

        self.button_gen_hmi = GenFormButton('\t\t\t\tСобрать Pictures\t\t\t\t')
        self.button_gen_hmi.clicked.connect(self.click_hmi)

        self.checkbox_hmi_ktpr = CheckBox('KTPR')
        self.checkbox_hmi_ktpra = CheckBox('KTPRA')
        self.checkbox_hmi_gmpna = CheckBox('GMPNA')
        self.checkbox_hmi_ktprp = CheckBox('KTPRP')
        self.checkbox_hmi_uso = CheckBox('USO')
        self.checkbox_hmi_uts = CheckBox('UTS')
        self.checkbox_hmi_upts = CheckBox('UPTS')

        self.layout_hmi()

    def layout_hmi(self):
        '''Собираем в один слой атрибуты HMI.'''
        self.layout_h1.addWidget(self.select_row)
        self.layout_h1.addWidget(self.checkbox_hmi_ktpra)
        self.layout_h1.addWidget(self.checkbox_hmi_gmpna)
        self.layout_h1.addWidget(self.checkbox_hmi_ktpr)
        self.layout_h1.addWidget(self.checkbox_hmi_ktprp)
        self.layout_h1.addWidget(self.checkbox_hmi_uso)
        self.layout_h1.addWidget(self.checkbox_hmi_uts)
        self.layout_h1.addWidget(self.checkbox_hmi_upts)
        self.layout_h1.addWidget(self.button_gen_hmi)

    def object_devstudio(self):
        '''Добавляем объекты для генерация DevStudio.'''
        self.checkbox_dev_analogs = CheckBox('Analogs')
        self.checkbox_dev_diskrets = CheckBox('Diskrets')
        self.checkbox_dev_vs = CheckBox('VS')
        self.checkbox_dev_zd = CheckBox('ZD')
        self.checkbox_dev_na = CheckBox('NA')
        self.checkbox_dev_uts = CheckBox('UTS')
        self.checkbox_dev_pic = CheckBox('Pic')
        self.checkbox_dev_ktpr = CheckBox('KTPR')
        self.checkbox_dev_ktpra = CheckBox('KTPRA')
        self.checkbox_dev_gmpna = CheckBox('GMPNA')
        self.checkbox_dev_upts = CheckBox('UPTS')
        self.checkbox_dev_pi = CheckBox('PI')
        self.checkbox_dev_pz = CheckBox('PZ')
        self.checkbox_dev_ktprp = CheckBox('KTPRP')
        self.checkbox_dev_sss = CheckBox('SSs')
        self.checkbox_dev_ais = CheckBox('AIs')
        self.checkbox_dev_aos = CheckBox('AOs')
        self.checkbox_dev_dis = CheckBox('DIs')
        self.checkbox_dev_dos = CheckBox('DOs')
        self.checkbox_dev_rss = CheckBox('RSs')
        self.checkbox_dev_psus = CheckBox('PSUs')
        self.checkbox_dev_cpus = CheckBox('CPUs')
        self.checkbox_dev_mns = CheckBox('MNs')
        self.checkbox_dev_cns = CheckBox('CNs')
        self.checkbox_dev_rackstate = CheckBox('Rackstates')
        self.checkbox_dev_colorDI = CheckBox('ColorScheme')
        self.checkbox_dev_anForm = CheckBox('AnalogsFormats')
        self.checkbox_dev_mapEGU = CheckBox('MapEGU')

        self.layout_devstudio()

    def layout_devstudio(self):
        '''Собираем в один слой атрибуты DevStudio.'''
        self.layout_v2.addWidget(self.checkbox_dev_analogs)
        self.layout_v2.addWidget(self.checkbox_dev_diskrets)
        self.layout_v2.addWidget(self.checkbox_dev_vs)
        self.layout_v2.addWidget(self.checkbox_dev_zd)
        self.layout_v2.addWidget(self.checkbox_dev_na)
        self.layout_v2.addWidget(self.checkbox_dev_uts)
        self.layout_v3.addWidget(self.checkbox_dev_pic)
        self.layout_v3.addWidget(self.checkbox_dev_ktpr)
        self.layout_v3.addWidget(self.checkbox_dev_ktpra)
        self.layout_v3.addWidget(self.checkbox_dev_gmpna)
        self.layout_v3.addWidget(self.checkbox_dev_upts)
        self.layout_v3.addWidget(self.checkbox_dev_pi)
        self.layout_v4.addWidget(self.checkbox_dev_pz)
        self.layout_v4.addWidget(self.checkbox_dev_ktprp)
        self.layout_v4.addWidget(self.checkbox_dev_sss)
        self.layout_v4.addWidget(self.checkbox_dev_ais)
        self.layout_v4.addWidget(self.checkbox_dev_aos)
        self.layout_v4.addWidget(self.checkbox_dev_dis)
        self.layout_v5.addWidget(self.checkbox_dev_dos)
        self.layout_v5.addWidget(self.checkbox_dev_rss)
        self.layout_v5.addWidget(self.checkbox_dev_psus)
        self.layout_v5.addWidget(self.checkbox_dev_cpus)
        self.layout_v5.addWidget(self.checkbox_dev_mns)
        self.layout_v5.addWidget(self.checkbox_dev_cns)
        self.layout_v6.addWidget(self.checkbox_dev_rackstate)
        self.layout_v6.addWidget(self.checkbox_dev_colorDI)
        self.layout_v6.addWidget(self.checkbox_dev_anForm)
        self.layout_v6.addWidget(self.checkbox_dev_mapEGU)
        self.layout_v6.addSpacing(60)

        button_gen_omx = GenFormButton('\t\t\t\tЗаполнить структуру\t\t\t\t')
        button_gen_omx.clicked.connect(self.click_fill_omx)
        button_clear_omx = GenFormButton('\t\t\t\tОчистить структуру\t\t\t\t')
        button_clear_omx.clicked.connect(self.click_clear_omx)
        button_gen_map = GenFormButton('\t\t\t\tЗаполнить карту\t\t\t\t')
        button_gen_map.clicked.connect(self.click_fill_map)
        button_clear_map = GenFormButton('\t\t\t\tОчистить карту\t\t\t\t')
        button_clear_map.clicked.connect(self.click_clear_map)

        self.layout_v7.addWidget(button_gen_omx)
        self.layout_v7.addWidget(button_clear_omx)
        self.layout_v7.addSpacing(25)
        self.layout_v7.addWidget(button_gen_map)
        self.layout_v7.addWidget(button_clear_map)

        self.layout_h2.addLayout(self.layout_v2)
        self.layout_h2.addLayout(self.layout_v3)
        self.layout_h2.addLayout(self.layout_v4)
        self.layout_h2.addLayout(self.layout_v5)
        self.layout_h2.addLayout(self.layout_v6)
        self.layout_h2.addSpacing(50)
        self.layout_h2.addLayout(self.layout_v7)

    def object_textfile(self):
        '''Добавляем объекты для генерация текстовых файлов.'''
        self.button_trends = GenFormButton('\t\t\t\tДерево трендов\t\t\t\t')
        self.button_trends.clicked.connect(self.click_tree_trends)

        self.layout_textfile()

    def layout_textfile(self):
        '''Собираем в один слой генерацию текстовых файлов.'''
        self.layout_h3.addWidget(self.button_trends)
        self.layout_h3.addSpacing(600)

    def object_uso(self):
        '''Объект класса генерация усо.'''
        self.uso = DaignoPicture(self.logsTextEdit)
        self.uso.filling_pic_uso()

    def object_defence(self, table: dict, number_pump: int = None):
        '''Объект класса генерация защит.'''
        self.defence = DefenceMap(self.logsTextEdit)
        self.defence.fill_pic_new(table, number_pump)

    def object_siren(self, table: dict):
        '''Объект класса генерация сирен.'''
        self.siren = Alarm_map(table, self.logsTextEdit)
        self.siren.filling_template()

    def click_hmi(self):
        '''Клик по кнопке собрать Pictures.'''
        try:
            reqsql = RequestSQL()
        except Exception:
            self.logsTextEdit.logs_msg('''Невозможно создать форму.
                                       Нет подключения к БД разработки''', 2)
            return

        if self.checkbox_hmi_ktpr.isChecked():
            self.object_defence('KTPR')
        if self.checkbox_hmi_ktprp.isChecked():
            self.object_defence('KTPRP')
        if self.checkbox_hmi_ktpra.isChecked():
            num_pump = self.select_row.text()
            if num_pump == '':
                self.object_defence('KTPRA')
            else:
                self.object_defence('KTPRA', int(num_pump))
        if self.checkbox_hmi_gmpna.isChecked():
            num_pump = self.select_row.text()
            if num_pump == '':
                self.object_defence('GMPNA')
            else:
                self.object_defence('GMPNA', int(num_pump))
        if self.checkbox_hmi_uso.isChecked():
            self.object_uso()
        if self.checkbox_hmi_uts.isChecked():
            self.object_siren('UTS')
        if self.checkbox_hmi_upts.isChecked():
            self.object_siren('UPTS')

    def check_devstudio_attr(self):
        list_param = []
        list_help = {self.checkbox_dev_analogs: ['Analogs', AnalogsMap, AnalogsOmx],
                     self.checkbox_dev_diskrets: ['Diskrets', DiskretsMap, DiskretsOmx],
                     self.checkbox_dev_vs: ['AuxSystems', VSMap, VSOmx],
                     self.checkbox_dev_zd: ['Valves', ZDMap, ZDOmx],
                     self.checkbox_dev_na: ['NAs', PumpsMap, NAOmx],
                     self.checkbox_dev_uts: ['UTSs', UtsUptsMap, UtsUptsOmx],
                     self.checkbox_dev_pic: ['Pictures', PicturesMap, PICOmx],
                     self.checkbox_dev_ktpr: ['KTPRs', KTPRMap, KTPROmx],
                     self.checkbox_dev_ktpra: ['KTPRAs', KTPRAMap, KtpraGmpnaOmx],
                     self.checkbox_dev_gmpna: ['GMPNAs', GMPNAMap, KtpraGmpnaOmx],
                     self.checkbox_dev_upts: ['UPTSs', UtsUptsMap, UtsUptsOmx],
                     self.checkbox_dev_pi: ['PIs', PIMap, PIOmx],
                     self.checkbox_dev_pz: ['PZs', PZMap, PZOmx],
                     self.checkbox_dev_ktprp: ['KTPRPs', KTPRMap, KTPROmx],
                     self.checkbox_dev_sss: ['SSs', RelaytedSystemMap, SSOmx],
                     self.checkbox_dev_ais: ['Diag.AIs', DiagMap, DIAGOmx],
                     self.checkbox_dev_aos: ['Diag.AOs', DiagMap, DIAGOmx],
                     self.checkbox_dev_dis: ['Diag.DIs', DiagMap, DIAGOmx],
                     self.checkbox_dev_dos: ['Diag.DOs', DiagMap, DIAGOmx],
                     self.checkbox_dev_rss: ['Diag.RSs', DiagMap, DIAGOmx],
                     self.checkbox_dev_psus: ['Diag.PSUs', DiagMap, DIAGOmx],
                     self.checkbox_dev_cpus: ['Diag.CPUs', DiagMap, DIAGOmx],
                     self.checkbox_dev_mns: ['Diag.MNs', DiagMap, DIAGOmx],
                     self.checkbox_dev_cns: ['Diag.CNs', DiagMap, DIAGOmx],
                     self.checkbox_dev_rackstate: ['Diag.RackStates', RackStateMap]
                     }
        for param, value in list_help.items():
            if param.isChecked():
                list_param.append(value)
        return list_param

    def click_fill_omx(self):
        for param in self.check_devstudio_attr():
            try:
                if param[0] in ('KTPRAs', 'GMPNAs'):
                    table = True if 'KTPRAs' in param else False
                    obj = param[2](self.logsTextEdit, table)
                elif 'Diag' in param[0]:
                    type_module = param[0].split('.')

                    if type_module[1] in ('AIs', 'AOs', 'DIs', 'DOs'):
                        attr = AttrDIAGOmx(self.logsTextEdit, type_module[1])
                        attr.write_in_omx()

                    obj = param[2](self.logsTextEdit, type_module[1])
                else:
                    obj = param[2](self.logsTextEdit)
            except Exception:
                self.logsTextEdit.logs_msg('''Невозможно заполнить карту адресов DevStudio.
                                           Нет подключения к БД разработки''', 2)
                return
            obj.write_in_omx()

    def click_clear_omx(self):
        '''Очистка объектов DevStudio.'''
        for param in self.check_devstudio_attr():
            if 'Diag.' in param[0]:
                text = param[0].replace('Diag.', '')
                fl_diag = True
            elif 'KTPRPs' in param[0]:
                fl_diag = False
                text = 'KTPRs'
            else:
                fl_diag = False
                text = param[0]

            path_file = connect.path_to_devstudio_omx
            path_attr = f'Root{connect.prefix_system}'

            root, tree = self.dop_function.xmlParser(path_file)
            self.dop_function.clear_omx(path_attr, text, root, fl_diag)

            tree.write(path_file, pretty_print=True)

            self.logsTextEdit.logs_msg(f'''DevStudio. Object. {text}. Объекты очищены''', 3)

    def click_fill_map(self):
        '''Заполнение карты адресов DevStudio.'''
        for param in self.check_devstudio_attr():
            try:
                obj = param[1](self.logsTextEdit)
            except Exception:
                self.logsTextEdit.logs_msg('''Невозможно заполнить карту адресов DevStudio.
                                           Нет подключения к БД разработки''', 2)
                return
            if 'Diag' in param[0]:
                if 'RackStates' in param[0]:
                    obj.work_file()
                else:
                    module = param[0].replace('Diag.', '')
                    obj.work_file(module)
            else:
                obj.work_file(True) if param[0] in ('UPTSs', 'KTPRPs') else obj.work_file()

    def click_clear_map(self):
        '''Очистка карты адресов DevStudio.'''
        for param in self.check_devstudio_attr():
            driver_file = 'Modbus503' if 'Analogs' in param[0] else 'Modbus'
            text = 'KTPRs' if param[0] in 'KTPRPs' else param[0]

            path_file = f'{connect.path_to_devstudio}\\{driver_file}.xml'
            path_attr = f'Root{connect.prefix_system}.{text}.'

            root, tree = self.dop_function.xmlParser(path_file)
            self.dop_function.clear_map(path_file, path_attr, root, tree)
            self.logsTextEdit.logs_msg(f'''DevStudio. Map. {text}. Карта адресов очищена''', 3)

    def click_tree_trends(self):
        '''Формирование дерева трендов.'''
        trends = TreeTrends(self.logsTextEdit)
        trends.fill_tree_trends()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('ProjectInit')
        self.setWindowIcon(QIcon('logo.png'))
        self.setFixedSize(SIZE_WORK_BACK[0], SIZE_WORK_BACK[1])
        # Журнал сообщений
        self.logsTextEdit = LogsTextEdit(self)
        self.logsTextEdit.setStyleSheet('''
                                        font:12px times;
                                        background-color: #f0f0f0;
                                        border-top-left-radius: 5;
                                        border-top-right-radius: 5;
                                        border-bottom-left-radius: 5;
                                        border-bottom-right-radius: 5;
                                        border: 1px solid #a19f9f;''')
        # Основное окно с вкладками
        self.tabwidget = TabWidget()
        self.set_tabs()
        # Окно редактирования
        self.edit_window = EditTabWidget()
        self.edit_tab()
        # Нижние ряд с индикаций
        self.bottom_row()
        # Макет
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        splitter_h = QSplitter(Qt.Horizontal)
        splitter_h.addWidget(self.tabwidget)
        splitter_h.addWidget(self.edit_window)
        splitter_h.setSizes([100, 236])

        splitter_v = QSplitter(Qt.Vertical)
        splitter_v.addWidget(splitter_h)
        splitter_v.addWidget(self.logsTextEdit)
        splitter_v.setSizes(SIZE_SPLIT_V)

        layout_h = QHBoxLayout()
        layout_h.addWidget(self.clear_log)
        layout_h.addWidget(self.connect_SQL_edit)
        layout_h.addWidget(self.connect_SQL_prj)
        layout_h.addWidget(self.connect_exel)

        layout_v = QVBoxLayout(self.centralwidget)
        layout_v.addWidget(splitter_v)
        layout_v.addLayout(layout_h)

        self.logsTextEdit.logs_msg('Генератор разработки проекта запущен', 1)

    def edit_tab(self):
        '''Добавление на экран виджетов для запуска окна редактирования.'''
        tab_1 = EditWindows(self.logsTextEdit, self)
        self.edit_window.addTab(tab_1, 'Окно редактирования БД SQL')

    def set_tabs(self):
        self.tab_1 = TabConnect(self.logsTextEdit, self)
        tab_2 = ImportKD(self.logsTextEdit, self)
        tab_3 = DevSQL(self.logsTextEdit)
        tab_4 = TabConnect(self.logsTextEdit)
        tab_5 = GenHMIandDev(self.logsTextEdit)
        tab_6 = TabConnect(self.logsTextEdit)

        self.tabwidget.addTab(self.tab_1, 'Соединение')
        self.tabwidget.addTab(tab_2, 'Импорт КЗФКП')
        self.tabwidget.addTab(tab_3, 'БД разработки')
        self.tabwidget.addTab(tab_4, 'БД проекта')
        self.tabwidget.addTab(tab_5, 'ВУ')
        self.tabwidget.addTab(tab_6, 'СУ')

    def bottom_row(self):
        '''Нижний ряд с кнопкой и ииндикацией.'''
        self.connect_exel = Label()
        self.connect_exel.setText('Соединение с Exel не установлено')
        self.connect_SQL_edit = Label()
        self.connect_SQL_edit.setText('Соединение с БД разработки не установлено')
        self.connect_SQL_prj = Label()
        self.connect_SQL_prj.setText('Соединение с БД проекта не установлено')
        self.clear_log = PushButton('Очистить журнал')
        self.clear_log.clicked.connect(self.clear_jornal)
        self.clear_log.setStyleSheet("""*{
                                     font:13px times;
                                     background-color: #f0f0f0;
                                     border: 1px solid #a19f9f;
                                     padding: 4px; border-radius: 4}
                                     *:hover{background:#e0e0e0;
                                             color:'black'}
                                     *:pressed{background: '#e0e0e0'}""")

    def clear_jornal(self):
        '''Чистка журнала при нажатии кнопки.'''
        self.logsTextEdit.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec())