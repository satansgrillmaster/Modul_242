import socket
import json
from database import db_manager
from constants import DB_NAME
from enums import QueryMethod, Table


class Server:

    NEW_CONNECTION_INFO_LVL = "NEW_CONNECTION"
    WARRNING_INFO_LVL = "WARRNING"
    ERROR_INFO_LVL = "ERROR"

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.db_manager = db_manager.DbManager(DB_NAME)

        # start socket and listen for connections
        self.socket = self._init_socket()
        self._listen_to_connections()

    def _init_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        return s

    def _listen_to_connections(self):

        while True:
            self.socket.listen()
            conn, addr = self.socket.accept()

            with conn:
                response = self.handle_halo_request(conn.recv(1024), addr)
                conn.sendto(json.dumps(response).encode('utf-8'), addr)

    def handle_halo_request(self, request, address):
        clean_data = json.loads(request)
        info_lvl = clean_data["request_info_lvl"]

        if info_lvl == Server.NEW_CONNECTION_INFO_LVL:
            try:
                self.db_manager.execute_query(table_name=Table.HALO_RING_CONFIG.value,
                                              query_method=QueryMethod.INSERT,
                                              values={"address": address[0],
                                                      "led_color_idfk": "1"})
            except Exception as e:
                print(e)

        elif info_lvl == Server.WARRNING_INFO_LVL or info_lvl == Server.ERROR_INFO_LVL:
            self.db_manager.execute_query(table_name=Table.TASK_LOG.value,
                                          query_method=QueryMethod.INSERT,
                                          values={"request_info_lvl": info_lvl,
                                                  "log_message": clean_data["message"],
                                                  "request_ip": address[0]})
        else:
            print(clean_data)

        halo_ring_config = self.db_manager.execute_query(Table.HALO_RING_CONFIG.value,
                                                         QueryMethod.SELECT,
                                                         {"led_color_idfk": ""},
                                                         {"address": address[0]})

        led_color_config = self.db_manager.execute_query(Table.LED_COLOR.value,
                                                         QueryMethod.SELECT,
                                                         {"r": "",
                                                          "g": "",
                                                          "b": ""},
                                                         {"id": str(halo_ring_config[0][0])})

        response = {'color': {
            "r": led_color_config[0][0],
            "g": led_color_config[0][1],
            "b": led_color_config[0][2]
        }}

        return response
