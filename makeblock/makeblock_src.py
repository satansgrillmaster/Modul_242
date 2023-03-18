import halo
import event
import socket
import json
import _thread


class sockethandler:

    def __init__(self):
        self.is_alive = 1
        self.request_info_lvl = ''
        self.message = ''

    def _send_request(self):
        while self.is_alive:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("192.168.1.27", 5001))
            s.send(json.dumps({
                "request_info_lvl": self.request_info_lvl,
                "message": self.message
            }))
            time.sleep(1)
            try:
                response = s.recv(1024)
            except Exception as e:
                print(e)
            if response != 0:
                data = response.decode('utf-8')
                print(data)
                if data == 'green':
                    halo.led.show_all(0, 255, 0, 50)
                elif data == 'red':
                    halo.led.show_all(255, 0, 0, 50)
                elif data == 'blue':
                    halo.led.show_all(0, 0, 255, 50)
                elif data == 'yellow':
                    halo.led.show_all(255, 255, 0, 50)
            s.close()
            time.sleep(0.5)

    def init_request(self, request_info_lvl, message):
        self.request_info_lvl = request_info_lvl
        self.message = message

    def close_thread(self):
        self.is_alive = 0


@event.start
def on_start():
    halo.led.show_all(255, 255, 255, 10)
    time.sleep(1)

    halo.wifi.start(ssid='Salt_2GHz_8A9EB3', password='r7okjbSXZnuVr32v2h', mode=halo.wifi.WLAN_MODE_STA)
    while halo.wifi.is_connected() != 1:
        time.sleep(0.1)

    halo.led.off_all()

    ts = sockethandler()
    ts.init_request('NEW_CONNECTION', '')
    _thread.start_new_thread(ts._send_request, ())
    time.sleep(2)
    ts.init_request('LOG', 'test')

    time.sleep(10)
    # ts.close_thread()


@event.button_pressed
def on_button_pressed():
    halo.stop_all_scripts()
