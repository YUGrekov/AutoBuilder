from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTextEdit
from datetime import datetime as dt

COLOR_RED = '<span style="color:red;">{}</span>'
COLOR_YELLOW = '<span style="color:#9ea108;">{}</span>'
COLOR_BLACK = '<span style="color:black;">{}</span>'
COLOR_GREEN = '<span style="color:green;">{}</span>'


class LogsTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(LogsTextEdit, self).__init__(parent)

        self.setStyleSheet('''border-radius: 4px;
                              border: 1px solid''')
        self.setFont(QFont('Arial', 10))
        self.setReadOnly(True)

    def data_time(self) -> str:
        '''Текущее дата и время'''
        now = dt.now()
        data = now.strftime("%d/%m/%y")
        time = now.strftime("%H:%M:%S")
        return f'{data}  {time}'

    def logs_msg(self, msg: str = None, color: int = 1):
        """Выдача события.
        Args:
            msg (str, optional): Текст сообщения. Defaults to None.
            color (int, optional): Номер цвета. Defaults to 1.
        """
        event = self.data_time()

        if color == 0:
            self.append(COLOR_GREEN.format(f'{event}: {msg}'))
        elif color == 1:
            self.append(COLOR_BLACK.format(f'{event}: {msg}'))
        elif color == 2:
            self.append(COLOR_RED.format(f'{event}: {msg}'))
        elif color == 3:
            self.append(COLOR_YELLOW.format(f'{event}: {msg}'))