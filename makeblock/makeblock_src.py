import halo
import event
import socket
import json
import _thread
import mbuild

ts = None


class Configuration:

    def __init__(self, data):
        self.data = data
        self.set_led_config()

    def set_led_config(self):
        color = self.data['color']
        halo.led.show_all(color['r'], color['g'], color['b'], 10)


class SocketHandler:

    def __init__(self):
        self.is_alive = 1
        self.request_info_lvl = ''
        self.message = ''

    def _connect_to_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.65.4.32", 5001))
        return s

    def _send_request(self):
        first_request = 1

        while self.is_alive:
            s = self._connect_to_server()
            s.send(json.dumps({
                "request_info_lvl": self.request_info_lvl,
                "message": self.message
            }))
            time.sleep(0.5)

            try:
                response = s.recv(1024)
            except Exception as e:
                print(e)

            if response != 0:
                config = Configuration(json.loads(response))

            s.close()

            if first_request == 1:
                self.send_map_data(0)
                first_request = 0

            time.sleep(10)
            self.send_map_data(1)

            self.init_request('DATA_UPDATE_REQUEST', '')

            time.sleep(0.5)

    def init_request(self, request_info_lvl, message):
        self.request_info_lvl = request_info_lvl
        self.message = message

    def close_thread(self):
        self.is_alive = 0

    def send_map_data(self, update):

        info_lvl_first = ""
        info_lvl_second = ""

        if update:
            info_lvl_first = "UPDATE_MAP_DATA_1"
            info_lvl_second = "UPDATE_MAP_DATA_2"
        else:
            info_lvl_first = "MAP_DATA_1"
            info_lvl_second = "MAP_DATA_2"

        i = 0
        mbuild.servo_driver.set_angle(0, 1)
        time.sleep(3)
        while i < 180:
            s = self._connect_to_server()
            self.request_info_lvl = info_lvl_first
            self.message = str(mbuild.ultrasonic_sensor.get_distance(1))

            s.send(json.dumps({
                "request_info_lvl": self.request_info_lvl,
                "message": self.message
            }))
            s.close()

            s = self._connect_to_server()
            self.request_info_lvl = info_lvl_second
            self.message = str(mbuild.ultrasonic_sensor.get_distance(2))

            s.send(json.dumps({
                "request_info_lvl": self.request_info_lvl,
                "message": self.message
            }))
            s.close()

            mbuild.servo_driver.set_angle(i, 1)
            time.sleep(0.3)
            i += 10

        s = self._connect_to_server()
        if update:
            self.request_info_lvl = "UPDATE_DATA_PLOTTER"
            self.message = ''
        else:
            self.request_info_lvl = "DATA_PLOTTER"
            self.message = ''

        s.send(json.dumps({
            "request_info_lvl": self.request_info_lvl,
            "message": self.message
        }))

        s.close()


@event.start
def on_start():
    global ts


    #while 1 == 1:
    #    if mbuild.ultrasonic_sensor.get_distance(1) > 10:
    #        print(mbuild.ultrasonic_sensor.get_distance(1))


    halo.led.show_all(255, 255, 255, 10)
    halo.wifi.start(ssid='KR-yellow', password='2601-9345-2477', mode=halo.wifi.WLAN_MODE_STA)

    while halo.wifi.is_connected() != 1:
        time.sleep(0.1)

    halo.led.off_all()
    ts = SocketHandler()
    ts.init_request('NEW_CONNECTION', '')
    _thread.start_new_thread(ts._send_request, ())

    # ts.close_thread()


@event.button_pressed
def on_button_pressed():
    global ts

    ts.init_request('WARRNING', 'test')
