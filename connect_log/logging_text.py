from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTextEdit
from datetime import datetime as dt


COLORS = {
    0: '<span style="color:green;">{}</span>',
    1: '<span style="color:black;">{}</span>',
    2: '<span style="color:red;">{}</span>',
    3: '<span style="color:#9ea108;">{}</span>'
}


class LogsTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('''border-radius: 4px; border: 1px solid''')
        self.setFont(QFont('Arial', 10))
        self.setReadOnly(True)

    def data_time(self) -> str:
        '''Текущее дата и время'''
        return dt.now().strftime("%d/%m/%y  %H:%M:%S")

    def logs_msg(self, msg: str = None, color: int = 1):
        """Выдача события.
        Args:
            msg (str, optional): Текст сообщения. Defaults to None.
            color (int, optional): Номер цвета. Defaults to 1.
        """
        event = self.data_time()
        self.append(COLORS.get(color, COLORS[1]).format(f'{event}: {msg}'))