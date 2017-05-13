from random import random, randint
from typing import List

class _ConfigReader:
    def __init__(self,config_path: str):
        self.__entrance_regions={}
        self.__transfer_info_dict={}  # 用于存放一个区域向其他区域转换的概率信息，形式为{region_id: {region_id: probability, ... }, ... }
        with open(config_path,"r",True) as config_file:
            line=config_file.readline()
            while line=="\n":
                line=config_file.readline()
            entrance_list=line.split(" ")
            total=0
            for item in entrance_list:
                item_list=item.split(":")
                total+=int(item_list[1])
                self.__entrance_regions[int(item_list[0])]=int(item_list[1])
            for key,value in self.__entrance_regions.items():
                self.__entrance_regions[key]=value/total
            line=config_file.readline()
            while line!="":
                if line=="\n":
                    line=config_file.readline()
                    continue
                list1=line.split("->")
                list2=list1[1].split(" ")
                tran_prob_dict = {}
                total=0
                for tran_prob in list2:
                    if tran_prob == "":continue
                    else:
                        list3=tran_prob.split(":")
                        total+=int(list3[1])
                        tran_prob_dict[int(list3[0])]=int(list3[1])
                for key, value in tran_prob_dict.items():
                    tran_prob_dict[key] = value / total
                self.__transfer_info_dict[int(list1[0])]=tran_prob_dict
                line=config_file.readline()

    @property
    def entrance_regions(self):
        return self.__entrance_regions

    @property
    def transfer_info_dict(self):
        return self.__transfer_info_dict

class _PositioningDataGenerator:
    def __init__(self,config_reader: _ConfigReader):
        self.__entrance_regions = config_reader.entrance_regions
        self.__transfer_info_dict = config_reader.transfer_info_dict

    def generate_data(self,output_path: str,filter_num: int,region_seq_num: int) -> None:
        with open(output_path,"w",True):
            pass

        with open(output_path,"a+",True) as output_file:
            output_file.write("filter_num = "+str(filter_num)+"\n")
            for i in range(region_seq_num):
                output_file.write("\n<\n")
                region_seq=self.__generate_region_seq_data()
                for region_id in region_seq:
                    string=""
                    rdint = randint(20, 40)
                    string+=(str(region_id)+" ")*rdint
                    rdm=random()
                    if rdm>0.8:
                        string+=(str(randint(1,20))+" ")*randint(1,filter_num)
                    output_file.write(string)
                output_file.write("\n>\n")


    def __generate_region_seq_data(self) -> List[int]:
        rdm=random()
        total=0
        region_seq=[]
        for key,value in self.__entrance_regions.items():
            total+=value
            if total>rdm:
                region_seq.append(key)
                break
        while region_seq[-1] in self.__transfer_info_dict:
            rdm = random()
            total = 0
            for key, value in self.__transfer_info_dict[region_seq[-1]].items():
                total += value
                if total > rdm:
                    region_seq.append(key)
                    break
        return region_seq

def generate_positioning_data(config_path: str,output_path: str,filter_num: int,region_seq_num: int):
    _PositioningDataGenerator(_ConfigReader(config_path)).generate_data(output_path,filter_num,region_seq_num)

if __name__=="__main__":
    generate_positioning_data("simulation_data\\path_setting.config","simulation_data\\historical_positioning_data.hpd",5,100)
