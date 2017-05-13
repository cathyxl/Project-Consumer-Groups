from typing import List
from file_reader import FileReader

class PositioningDataReader:
    def __init__(self,new_file_reader: FileReader):
        self.__file_reader: FileReader=new_file_reader
        for i in range(2):
            self.__next_word()
        self.__filter_num: int=int(self.__next_word())
        self.__is_finished: bool=False

    def __get_region_seq(self) -> List[int]:
        current_region: int = None
        region_seq: List[int]=[]
        consecutive_same_region_num: int=1
        start_word=self.__next_word()
        if start_word=="<":
            while True:
                next_word=self.__next_word()
                if next_word==">" or next_word is None:
                    if consecutive_same_region_num >= self.__filter_num:
                        if region_seq == [] or current_region != region_seq[-1]:
                            region_seq.append(current_region)
                    if next_word is None:
                        self.__is_finished = True
                    break
                else:
                    if current_region is None:
                        current_region = int(next_word)
                    else:
                        if int(next_word)==current_region:
                            consecutive_same_region_num += 1
                        else:
                            if consecutive_same_region_num>=self.__filter_num:
                                if region_seq==[] or current_region!=region_seq[-1]:
                                    region_seq.append(current_region)
                            current_region = int(next_word)
                            consecutive_same_region_num = 1
        else:
            if start_word is None:
                self.__is_finished = True
            return []
        return region_seq


    def __next_word(self) -> str:
        return self.__file_reader.next_word()

    def get_data_set(self) -> List[List[int]]:
        data_set: List[List[int]]=[]
        while True:
            region_seq=self.__get_region_seq()
            if region_seq != []:
                data_set.append(region_seq)
            if self.__is_finished==True:
                break
        return data_set
