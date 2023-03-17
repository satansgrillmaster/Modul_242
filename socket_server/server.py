import socket
import json
from database import db_manager
from constants import DB_NAME
from enums import QueryMethod, Table


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = self._init_socket()
        self.db_manager = db_manager.DbManager(DB_NAME)

        while True:
            self.socket.listen()
            conn, addr = self.socket.accept()
            with conn:
                print(f"Connected by {addr[0]}")

                self.handle_halo_request(conn.recv(1024))

    def _init_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        return s

    def handle_halo_request(self, request):
        clean_data = json.loads(request)
        request_type = clean_data["type"]
        message = clean_data["message"]
        self.db_manager.execute_query(table_name=Table.LOG.value,
                                      query_method=QueryMethod.INSERT,
                                      values={
            "log_type": request_type,
            "log_message": message
        }, )

        print(request_type, message)

