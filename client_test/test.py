from plotter import distance_plotter
from database import db_manager
from constants import DB_NAME
from enums import QueryMethod, Table
db_manager.DbManager(DB_NAME)

a = distance_plotter.DistancePlotter()