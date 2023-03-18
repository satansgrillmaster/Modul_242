import halo
import event
import socket
import json
import _thread


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
        s.connect(("192.168.1.27", 5001))
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

            if first_request != 0:
                self.init_request('DATA_UPDATE_REQUEST', '')

            time.sleep(0.5)

    def init_request(self, request_info_lvl, message):
        self.request_info_lvl = request_info_lvl
        self.message = message

    def close_thread(self):
        self.is_alive = 0


@event.start
def on_start():
    halo.led.show_all(255, 255, 255, 10)
    halo.wifi.start(ssid='Salt_2GHz_8A9EB3', password='r7okjbSXZnuVr32v2h', mode=halo.wifi.WLAN_MODE_STA)

    while halo.wifi.is_connected() != 1:
        time.sleep(0.1)

    halo.led.off_all()

    ts = SocketHandler()
    ts.init_request('NEW_CONNECTION', '')
    _thread.start_new_thread(ts._send_request, ())

    time.sleep(10)
    # ts.close_thread()


@event.button_pressed
def on_button_pressed():
    halo.stop_all_scripts()
