from peewee import PostgresqlDatabase
from peewee import Database
from peewee import OperationalError
from typing import Optional
from psycopg2 import Error


class DatabaseManager:
    """
    Универсальный класс для управления подключением к базе данных с использованием peewee.
    """
    def __init__(self, parent,
                 db_type: str,
                 database: str,
                 user: Optional[str] = None,
                 password: Optional[str] = None,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 ):
        """
        Инициализация менеджера базы данных.

        :param logstext: экземпляр логов'.
        :param db_type: Тип базы данных ('postgresql').
        :param database: Имя базы данных.
        :param user: Имя пользователя.
        :param password: Пароль.
        :param host: Хост.
        :param port: Порт.
        """
        self.logs_msg = parent.logsTextEdit.logs_msg
        self.db_type = db_type
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        # Инициализация объекта базы данных
        if db_type == 'postgresql':
            self.db: Database = PostgresqlDatabase(
                database, user=user, password=password, host=host, port=port
            )
        else:
            raise ValueError(f"Неподдерживаемый тип базы данных: {db_type}")

    def __enter__(self):
        """Поддержка контекстного менеджера для автоматического подключения."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Поддержка контекстного менеджера для автоматического отключения."""
        pass

    def get_database(self) -> Database:
        """
        Возвращает объект базы данных для использования в моделях peewee.
        :return: Объект базы данных (PostgresqlDatabase).
        """
        return self.db

    def get_tables(self):
        '''Сбор таблиц базы'''
        return self.db.get_tables()

    def is_connected(self) -> bool:
        """
        Проверяет, установлено ли соединение с базой данных.
        :return: True, если соединение установлено, иначе False.
        """
        return not self.db.is_closed()

    def connect(self) -> None:
        """
        Устанавливает соединение с базой данных.
        """
        try:
            if not self.is_connected():
                self.db.connect()
                self.logs_msg(f"БД: cоединение с базой данных '{self.database}' установлено", 0)
                print(f"Соединение с базой данных '{self.database}' установлено.")
            else:
                self.logs_msg(f"БД: cоединение с базой данных '{self.database}' уже установлено", 0)
                print(f"Соединение с базой данных '{self.database}' уже установлено")
        except OperationalError as e:
            self.logs_msg(f"БД: ошибка подключения к базе данных '{self.database}': {e}", 2)
            print(f"Ошибка подключения к базе данных '{self.database}': {e}")

    def disconnect(self) -> None:
        """
        Разрывает соединение с базой данных.
        """
        try:
            if self.is_connected():
                self.db.close()
                self.logs_msg(f"БД: cоединение с базой данных '{self.database}' разорвано", 2)
                print(f"Соединение с базой данных '{self.database}' разорвано")
            else:
                self.logs_msg(f"БД: cоединение с базой данных '{self.database}' уже разорвано", 2)
                print(f"Соединение с базой данных '{self.database}' уже разорвано")
        except OperationalError as e:
            self.logs_msg(f"БД: ошибка при разрыве соединения с базой данных '{self.database}': {e}", 2)
            print(f"Ошибка при разрыве соединения с базой данных '{self.database}': {e}")

    def connect_default_db(self) -> None:
        try:
            # Подключаемся к системной базе данных 'postgres'
            default_db = PostgresqlDatabase(
                'postgres',  # Системная база данных
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return default_db
        except Exception:
            return ('Ошибка')

    def check_database_exists(self) -> bool:
        """
        Проверяет, существует ли база данных.
        :return: True, если база данных существует, иначе False.
        """
        try:
            default_db = self.connect_default_db()
            default_db.connect()

            # Выполняем запрос к системному каталогу pg_database
            query = "SELECT 1 FROM pg_database WHERE datname = %s;"
            cursor = default_db.execute_sql(query, (self.database,))
            result = cursor.fetchone()
            cursor.close()
            # Закрываем временное соединение
            default_db.close()

            # Если результат не пустой, база данных существует
            return result is not None
        except Exception:
            return False

    def create_database(self, dbname):
        """
        Создает новую базу данных в PostgreSQL.
        :param dbname: Имя новой базы данных.
        """
        try:
            # Подключаемся к серверу PostgreSQL (к базе данных по умолчанию "postgres")
            default_db = self.connect_default_db()
            default_db.connect()
            default_db.autocommit = True  # Включаем autocommit для выполнения DDL-запросов

            # Проверяем, существует ли база данных
            if not self.check_database_exists():
                # Создаем новую базу данных
                default_db.execute_sql(f'CREATE DATABASE {dbname};')
                self.logs_msg(f"БД: '{dbname}' успешно создана", 0)
                print(f"База данных '{dbname}' успешно создана")
            else:
                self.logs_msg(f"БД: '{dbname}' уже существует", 0)
                print(f"База данных '{dbname}' уже существует")

            # Закрываем соединение
            default_db.close()

        except Error as e:
            self.logs_msg(f"БД: Ошибка при создании базы данных: {e}", 0)
            print(f"Ошибка при создании базы данных: {e}")

    def execute_query_one(self, query: str) -> Optional[list]:
        """
        Выполняет SQL-запрос к базе данных.

        :param query: SQL-запрос.
        :return: Результат выполнения запроса или None в случае ошибки.
        """
        try:
            if not self.is_connected():
                self.connect()
            cursor = self.db.execute_sql(query)
            return cursor.fetchone()
        except OperationalError as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None

    def execute_query(self, query: str) -> Optional[list]:
        """
        Выполняет SQL-запрос к базе данных.

        :param query: SQL-запрос.
        :return: Результат выполнения запроса или None в случае ошибки.
        """
        try:
            if not self.is_connected():
                self.connect()
            cursor = self.db.execute_sql(query)
            return cursor.fetchall()
        except OperationalError as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None

    def execute_query_desc(self, query: str) -> Optional[list]:
        """
        Выполняет SQL-запрос к базе данных.

        :param query: SQL-запрос.
        :return: Результат выполнения запроса или None в случае ошибки.
        """
        try:
            if not self.is_connected():
                self.connect()
            cursor = self.db.execute_sql(query)
            return cursor.description
        except OperationalError as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None

    def query_no_return(self, query: str) -> Optional[list]:
        """
        Выполняет SQL-запрос к базе данных.

        :param query: SQL-запрос.
        :return: Результат выполнения запроса или None в случае ошибки.
        """
        try:
            if not self.is_connected():
                self.connect()
            self.db.execute_sql(query)
        except OperationalError as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None