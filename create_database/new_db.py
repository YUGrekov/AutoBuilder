import model as new
import psycopg2 as postgres
from psycopg2 import Error
from peewee import PostgresqlDatabase


MNS_LIST = [new.AI, new.AIFuse, new.AIgrp, new.AO, new.Buf, new.BufR, new.DI, new.DO, new.DPS,
            new.GMPNA, new.HardWare, new.HMINA, new.HMIREAL, new.HMIUDINT, new.HMIVS,
            new.HMIWORD, new.HMIZD, new.KTPR, new.KTPRA, new.KTPRS, new.Msg, new.MsgCat,
            new.MsgOthers, new.Net, new.NPS, new.PIC, new.PrjTM, new.RS, new.RSData, new.RSReq,
            new.Signals, new.SPGrp, new.SPRules, new.SS, new.SSData, new.TM_DP, new.TM_TI2,
            new.TM_TI4, new.TM_TII, new.TM_TR2, new.TM_TR4, new.TM_TS, new.TM_TU,
            new.TrendsGrp, new.UMPNA, new.tmNA_UMPNA_narab, new.tmNA_UMPNA, new.USO,
            new.UTS, new.UTS_tm, new.VS, new.VS_tm, new.VSGRP, new.VSGRP_tm, new.VV,
            new.ZD, new.ZD_tm, new.ZDType]

PT_LIST = [new.AI, new.AIFuse, new.AIgrp, new.BD, new.BDGRP, new.Buf, new.BufR, new.DI, new.DO,
           new.HardWare, new.HMIREAL, new.HMIUDINT, new.HMIVS, new.HMIWORD, new.HMIZD,
           new.KTPRP, new.KTPRS, new.Msg, new.MsgCat, new.MsgOthers, new.Net, new.PI, new.PIC,
           new.PrjTM, new.PT, new.PZ, new.PZ_tm, new.RS, new.RSData, new.RSReq, new.Signals,
           new.SPGrp, new.SPRules, new.SS, new.SSData, new.TrendsGrp, new.USO, new.UPTS,
           new.UPTS_tm, new.VS, new.VS_tm, new.VSGRP, new.VSGRP_tm, new.ZD, new.ZD_tm,
           new.ZDType]


class NewDB():
    '''Создание новой БД SQL с таблицами под определённую систему.'''
    def __init__(self):
        self.link = postgres.connect(dbname="postgres",
                                     user=new.connect.user,
                                     password=new.connect.password,
                                     host=new.connect.host)

    def create_new_base(self, type_system: str, logsTextEdit):
        """Создание подключения с PostgresSQL.
        Создание новой БД. Название БД из файла init_conf.cfg

        Args:
            type_system (str): Тип системы(МНС, ПТ, САР, РП)
        """
        cursor = self.link.cursor()
        self.link.autocommit = True
        logsTextEdit.logs_msg('Создано подключение к PostgreSQL', 0)

        try:
            cursor.execute(f'CREATE DATABASE {str(new.connect.database).lower()}')
            logsTextEdit.logs_msg(f'Добавлена новая БД: {new.connect.database}', 0)
        except (Exception, Error) as error:
            logsTextEdit.logs_msg(error, 3)
            return

        cursor.close()
        self.link.close()
        self.create_new_tabl(type_system)

    def create_new_tabl(self, type_system: str):
        '''Создание таблиц в новой БД.'''
        new.db = PostgresqlDatabase(str(new.connect.database).lower(),
                                    user=new.connect.user,
                                    password=new.connect.password,
                                    host=new.connect.host,
                                    port=new.connect.port)
        with new.db:
            type_list = MNS_LIST if type_system == 'MNS' else PT_LIST
            new.db.create_tables(type_list)