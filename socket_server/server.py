import socket
import json
from database import db_manager
from constants import DB_NAME
from enums import QueryMethod, Table
from plotter import distance_plotter


class Server:

    NEW_CONNECTION_INFO_LVL = "NEW_CONNECTION"
    WARRNING_INFO_LVL = "WARRNING"
    MAP_DATA_1_INFO_LVL = "MAP_DATA_1"
    MAP_DATA_2_INFO_LVL = "MAP_DATA_2"
    UPDATE_MAP_DATA_1_INFO_LVL = "UPDATE_MAP_DATA_1"
    UPDATE_MAP_DATA_2_INFO_LVL = "UPDATE_MAP_DATA_2"

    PLOTTER_INFO_LVL = "DATA_PLOTTER"
    UPDATE_PLOTTER_INFO_LVL = "UPDATE_DATA_PLOTTER"

    ERROR_INFO_LVL = "ERROR"

    REQUEST_SUCCESS = '200'
    REQUEST_ERROR = '400'

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.db_manager = db_manager.DbManager(DB_NAME)

        # start socket and listen for connections
        self.socket = self._init_socket()
        self._listen_to_connections()
        self.num_distance = 0
        self.distances = []
        self.plotter = None

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
                for client_adress in response['header']['clients']:
                    conn.sendto(json.dumps(response).encode('utf-8'), (client_adress[0], int(client_adress[1])))

    def handle_halo_request(self, request, address):
        clean_data = json.loads(request)
        info_lvl = clean_data["request_info_lvl"]
        response_code = Server.REQUEST_SUCCESS
        response_message = 'ok'
        clients = []

        if info_lvl == Server.NEW_CONNECTION_INFO_LVL:
            try:
                self.db_manager.execute_query(table_name=Table.HALO_RING_CONFIG.value,
                                              query_method=QueryMethod.INSERT,
                                              values={"address": address[0],
                                                      "led_color_idfk": "1",
                                                      "client_id": str(address[1])},
                                                        )
            except Exception as e:
                response_code = Server.REQUEST_ERROR
                response_message = 'Server error: ' + str(e)
            clients.append((address[0], address[1]))

        elif info_lvl == Server.WARRNING_INFO_LVL or info_lvl == Server.ERROR_INFO_LVL:
            self.db_manager.execute_query(table_name=Table.TASK_LOG.value,
                                          query_method=QueryMethod.INSERT,
                                          values={"request_info_lvl": info_lvl,
                                                  "log_message": clean_data["message"],
                                                  "request_ip": address[0]})

            reciving_clients = self.db_manager.execute_query(table_name=Table.HALO_RING_CONFIG.value,
                                                             query_method=QueryMethod.SELECT,
                                                             values={"address": "",
                                                                     "client_id": ""},
                                                             condition={"address": address[0]},
                                                             negativ_condition=True)
            for client in reciving_clients:
                clients.append((client[0], client[1]))

        elif info_lvl == Server.MAP_DATA_1_INFO_LVL:
            self.db_manager.execute_query(table_name=Table.SENSOR_DATA.value,
                                          query_method=QueryMethod.INSERT,
                                          values={
                                                  "sensor_1_data": clean_data["message"],
                                                  })
            clients.append((address[0], address[1]))

        elif info_lvl == Server.MAP_DATA_2_INFO_LVL:
            self.db_manager.execute_query(table_name=Table.SENSOR_DATA.value,
                                          query_method=QueryMethod.INSERT,
                                          values={
                                                  "sensor_2_data": clean_data["message"],
                                                  })
            clients.append((address[0], address[1]))

        elif info_lvl == Server.UPDATE_MAP_DATA_1_INFO_LVL:
            self.db_manager.execute_query(table_name=Table.UPDATE_SENSOR_DATA.value,
                                          query_method=QueryMethod.INSERT,
                                          values={
                                                  "sensor_1_data": clean_data["message"],
                                                  })
            clients.append((address[0], address[1]))

        elif info_lvl == Server.UPDATE_MAP_DATA_2_INFO_LVL:
            self.db_manager.execute_query(table_name=Table.UPDATE_SENSOR_DATA.value,
                                          query_method=QueryMethod.INSERT,
                                          values={
                                                  "sensor_2_data": clean_data["message"],
                                                  })
            clients.append((address[0], address[1]))

        elif info_lvl == Server.PLOTTER_INFO_LVL:
            self.distances = self.db_manager.execute_query(table_name=Table.SENSOR_DATA.value,
                                                            query_method=QueryMethod.SELECT,
                                                            values={"sensor_1_data": "",
                                                                    "sensor_2_data": ""},
                                                            condition={"sensor_1_data": "null"},
                                                            negativ_condition=True,
                                                            )
            self.distances += self.db_manager.execute_query(table_name=Table.SENSOR_DATA.value,
                                                            query_method=QueryMethod.SELECT,
                                                            values={"sensor_1_data": "",
                                                                    "sensor_2_data": ""},
                                                            condition={"sensor_2_data": "null"},
                                                            negativ_condition=True,
                                                            )

            self.num_distance = len(self.distances)
            self.plotter = self.plotter = distance_plotter.DistancePlotter(self.num_distance, self.distances, self.db_manager)
            self.plotter.calculate_and_draw_init(self.distances)
            clients.append((address[0], address[1]))

        elif info_lvl == Server.UPDATE_PLOTTER_INFO_LVL:


            new_distances = self.db_manager.execute_query(table_name=Table.UPDATE_SENSOR_DATA.value,
                                                            query_method=QueryMethod.SELECT,
                                                            values={"sensor_1_data": "",
                                                                    "sensor_2_data": ""},
                                                            condition={"sensor_1_data": "null"},
                                                            negativ_condition=True,
                                                            )
            new_distances += self.db_manager.execute_query(table_name=Table.UPDATE_SENSOR_DATA.value,
                                                            query_method=QueryMethod.SELECT,
                                                            values={"sensor_1_data": "",
                                                                    "sensor_2_data": ""},
                                                            condition={"sensor_2_data": "null"},
                                                            negativ_condition=True,
                                                            )


            self.plotter.redraw(len(new_distances), new_distances, self.distances)
            clients.append((address[0], address[1]))


        else:
            clients.append((address[0], address[1]))


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

        response = {'header': {'code': response_code,
                               'message': response_message,
                               'clients': clients},
                    'color': {"r": led_color_config[0][0],
                              "g": led_color_config[0][1],
                              "b": led_color_config[0][2]}
                    }

        return response
