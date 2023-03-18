import socket
import json
from database import db_manager
from constants import DB_NAME
from enums import QueryMethod, Table
import random


class Server:

    NEW_CONNECTION_INFO_LVL = "NEW_CONNECTION"
    WARRNING_INFO_LVL = "WARRNING"
    ERROR_INFO_LVL = "ERROR"

    NO_MESSAGE = "NO MESSAGE"

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = self._init_socket()
        self.db_manager = db_manager.DbManager(DB_NAME)

        while True:
            self.socket.listen()
            conn, addr = self.socket.accept()
            with conn:
                self.handle_halo_request(conn.recv(1024), addr)

                halo_ring_config = self.db_manager.execute_query(Table.HALO_RING_CONFIG.value,
                                                          QueryMethod.SELECT,
                                                          {"led_color_idfk":""},
                    {"adress": addr[0]})

                led_color_config = self.db_manager.execute_query(Table.LED_COLOR.value,
                                                          QueryMethod.SELECT,
                                                          {"description":""},
                                                          {"id": str(halo_ring_config[0][0])})
                conn.sendto(led_color_config[0][0].encode('utf-8'), addr)

    def _init_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        return s

    def handle_halo_request(self, request, adress):
        clean_data = json.loads(request)
        info_lvl = clean_data["request_info_lvl"]

        if info_lvl == Server.NEW_CONNECTION_INFO_LVL:
            self.db_manager.execute_query(table_name=Table.HALO_RING_CONFIG.value,
                                          query_method=QueryMethod.INSERT,
                                          values={
                                              "adress": adress[0],
                                              "led_color_idfk": "2",
                                          }, )
        elif info_lvl == Server.WARRNING_INFO_LVL or info_lvl == Server.ERROR_INFO_LVL:
            self.db_manager.execute_query(table_name=Table.TASK_LOG.value,
                                          query_method=QueryMethod.INSERT,
                                          values={
                                              "request_info_lvl": info_lvl,
                                              "log_message": clean_data["message"],
                                              "request_ip": adress[0]
                                          }, )
        else:
            print(clean_data)
