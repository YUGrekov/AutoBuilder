import configparser
import os

VERSION = 'ProjectCreate.exe'


class Connect():
    '''Отдельный вызов конфигурационного файла'''

    def __init__(self) -> None:
        '''Проверяем существование файла'''
        path_prj = f'{os.path.dirname(os.path.abspath(VERSION))}\\_settings\\init_conf.cfg'

        if os.path.exists(path_prj):
            self.config = configparser.ConfigParser()
            self.config.read(path_prj, encoding="utf-8")

        self.prefix_system = self.exist_check('Common', 'prefix_system')
        self.type_system = self.exist_check('Common', 'type_system')
        self.name_project = self.exist_check('Common', 'name_project')
        self.path_to_exel = self.exist_check('Common', 'path_to_kzfkp')
        self.path_rus_text = self.exist_check('Common', 'path_rus_text_column')
        self.path_sample = self.exist_check('MSG', 'path_sample')
        self.path_location_file = self.exist_check('MSG', 'path_location_file')
        self.path_su = self.exist_check('SU', 'path_su')
        self.path_to_devstudio_omx = self.exist_check('Scada', 'path_to_devstudio_omx')
        self.path_to_devstudio = self.exist_check('Scada', 'path_to_devstudio_folder')
        self.path_hmi = self.exist_check('Scada', 'path_hmi')
        self.path_hmi_sample = self.exist_check('Scada', 'path_hmi_sample')
        self.path_file_txt = self.exist_check('Scada', 'path_txt')
        self.database = self.exist_check('SQL', 'database')
        self.user = self.exist_check('SQL', 'user')
        self.password = self.exist_check('SQL', 'password')
        self.host = self.exist_check('SQL', 'host')
        self.port = self.exist_check('SQL', 'port')
        self.database_msg = self.exist_check('SQL', 'database_msg')
        self.user_msg = self.exist_check('SQL', 'user_msg')
        self.password_msg = self.exist_check('SQL', 'password_msg')
        self.host_msg = self.exist_check('SQL', 'host_msg')
        self.port_msg = self.exist_check('SQL', 'port_msg')

    def exist_check(self, hat: str, name_param: str) -> str:
        '''Проверяем на существование заданное значение'''
        try:
            return self.config[hat][name_param]
        except Exception:
            return ''