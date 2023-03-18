import socket
import time
from enums import QueryMethod, Table
from database import db_manager
from constants import DB_NAME
# try:
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect(("192.168.1.27", 5001))
#     s.send(b'aaa')
#     time.sleep(0.5)
#     data = s.recv(1024).decode('utf-8')
#     s.close()
#     print(data)
# except Exception as inst:
#     print(inst)

res = db_manager.DbManager("../" + DB_NAME).execute_query(table_name=Table.HALO_RING_CONFIG.value,
                                    query_method=QueryMethod.SELECT,
                                    values={"led_color_idfk": ""},condition={"adress":"192.168.1.33"})
print(res)