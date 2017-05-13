from file_reader import FileReader
from positioning_data_reader import PositioningDataReader
from region_prediction import mine_and_predict_region

with open("simulation_data\\historical_positioning_data.hpd","r",True) as file:
    data_set=PositioningDataReader(FileReader(file)).get_data_set()

print(mine_and_predict_region(data_set,20,0.1,[1],2))