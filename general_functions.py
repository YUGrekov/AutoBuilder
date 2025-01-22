import psycopg2
import os
import codecs
from lxml import etree


class General_functions():
    '''Общие функции использованные при разработке.'''
    def str_find(self, line, array):
        '''Поиск в строке.'''
        for word in array:
            if str(line).find(word) > -1:
                return True

    def translate(self, str):
        if str is None:
            return None

        dict = {".": "_",
                "/": "_",
                "\\": "_",
                ",": "_",
                ":": "_",
                ";": "_",
                "А": "A",
                "В": "B",
                "Е": "E",
                "К": "K",
                "М": "M",
                "Н": "H",
                "О": "O",
                "Р": "P",
                "С": "C",
                "Т": "T",
                "Ц": "TC",
                "Х": "X",
                "а": "a",
                "в": "b",
                "е": "e",
                "к": "k",
                "м": "m",
                "н": "h",
                "о": "o",
                "р": "p",
                "с": "c",
                "т": "t",
                "ц": "tc",
                "х": "x"
                }

        trantab = str.maketrans(dict)
        return str.translate(trantab)

    def exist_check_db(self, dbname, user, password, host, port):
        '''Проверка на существование БД'''
        try:
            db_connect = psycopg2.connect(f"""dbname={dbname}
                                              user={user}
                                              host={host}
                                              password={password}
                                              port={port}
                                              connect_timeout=1""")
            db_connect.close()
            return True
        except Exception:
            return False

    def check_in_table(self, table: str, array_table: dict):
        '''Проверка на существование таблицы в БД.'''
        return True if table in array_table else False

    def xmlParser(self, path):
        '''Парсинг файла.'''
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(path, parser)
        root = tree.getroot()
        return root, tree

    def clear_map(self, path_file, directory, root, tree):
        """Очистка нужной директории файла карты адресов DevStudio.
        Args:
            directory (str): Очищаемый атрибут
            root (_type_): Рабочий каталог
        """
        for item in root.iter('node-path'):
            if directory in item.text:
                parent = item.getparent()
                root.remove(parent)
        tree.write(path_file, pretty_print=True)

    def clear_xml(self, path_file, directory, root, tree):
        """Очистка нужной директории файла атрибутов."""
        for item in root.iter('item'):
            if directory in item.attrib['id']:
                root.remove(item)
        tree.write(path_file, pretty_print=True)

    def clear_omx(self, path_attr, directory,
                  root, fl_diag: bool = False):
        '''Очистка нужного объекта DevStudio.'''
        path = 'Diag' if fl_diag else path_attr

        for el in root.iter('{automation.deployment}application-object'):
            if el.attrib['name'] == "Application_PLC":
                for item in el.iter('{automation.control}object'):
                    if item.attrib['name'] == path:
                        for el1 in item.iter('{automation.control}object'):
                            if el1.attrib['name'] == directory:
                                item.remove(el1)
                        object = etree.Element("{automation.control}object")
                        object.attrib['name'] = directory
                        item.append(object)

                        for el1 in item.iter('{automation.control}object'):
                            if el1.attrib['name'] == directory:
                                return el1

    def check_file_txt(self, path):
        """Проверка файла txt на существование."""
        if not os.path.exists(path):
            text_file = codecs.open(path, 'w', 'utf-8')
            text_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<Source Type="NaftaPostgres">\n</Source>')
        else:
            os.remove(path)
            text_file = codecs.open(path, 'w', 'utf-8')
            text_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<Source Type="NaftaPostgres">\n</Source>')
        text_file.close()