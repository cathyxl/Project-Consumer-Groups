from positioning_data_read.file_reader import FileReader
from typing import Dict
from random import random

class _ConfigReader:
    def __init__(self, config_path: str):
        self.__motion_probability_dict: Dict[int,Dict[int,float]]={}  # 用于存放每个区域中可能发生的各个动作的发生概率，形式为{region_id: {motion_state_id: probability, ... }, ... }
        with open(config_path, "r", True) as ms_setting_file:
            line=ms_setting_file.readline()
            while line!="":
                if line=="\n":
                    line=ms_setting_file.readline()
                    continue
                list1=line.split("->")
                list2 = list1[1].split(" ")
                ms_prob_dict={}
                total=0
                for ms_prob in list2:
                    if ms_prob == "":continue
                    else:
                        list3=ms_prob.split(":")
                        total+=int(list3[1])
                        ms_prob_dict[int(list3[0])]=int(list3[1])
                for key, value in ms_prob_dict.items():
                    ms_prob_dict[key] = value / total
                self.__motion_probability_dict[int(list1[0])]=ms_prob_dict
                line = ms_setting_file.readline()

    @property
    def ms_probability_dict(self):
        return self.__motion_probability_dict

class _MSDataGenerator:
    def __init__(self,config_reader: _ConfigReader,hist_pos_data_path: str,ms_data_path:str,freq_ratio: int):
        self.__filter_num: int=None

        with open(ms_data_path, "w", True):
            pass

        with open(hist_pos_data_path, "r", True) as pos_file, \
                open(ms_data_path, "a+", True) as motion_file:
            pos_file_reader = FileReader(pos_file)
            for i in range(2):
                pos_file_reader.next_word()
            self.__filter_num = int(pos_file_reader.next_word())
            flag_in = False
            current_region = None
            count = 0
            word = pos_file_reader.next_word()
            while word is not None:
                if word == "<":
                    motion_file.write("\n<\n")
                    flag_in = True
                elif word == ">":
                    if count <= self.__filter_num:
                        pass
                    else:
                        num = (count // freq_ratio) + 1
                        for _ in range(num):
                            motion_file.write(str(current_region) + ":" + str(self.__get_random_ms(current_region)) + " ")
                        count = 0
                        current_region = None
                    motion_file.write("\n>\n")
                    flag_in = False
                else:
                    if flag_in is True:
                        if int(word) == current_region:
                            count += 1
                        else:
                            if count>self.__filter_num:
                                num = (count // freq_ratio) + 1
                                for _ in range(num):
                                    motion_file.write(
                                        str(current_region) + ":" + str(self.__get_random_ms(current_region)) + " ")
                            count=1
                            current_region = int(word)
                word = pos_file_reader.next_word()

    def __get_random_ms(self,region_id: int) -> int:
        value=config_reader.ms_probability_dict[region_id]
        total=0
        rdm = random()
        for k,v in value.items():
            total+=v
            if total>rdm:
                return k

if __name__=="__main__":
    config_reader = _ConfigReader("simulation_data\\motion_state_setting.config")
    ms_data_generator=_MSDataGenerator(config_reader,
                                       "simulation_data\\historical_positioning_data.hpd",
                                       "simulation_data\\motion_state_data.msd",
                                       3)
