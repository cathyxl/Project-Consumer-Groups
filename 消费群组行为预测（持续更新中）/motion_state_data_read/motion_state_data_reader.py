from typing import Dict


class _Reader:
    def __init__(self, new_file_object):
        self.__file_object = new_file_object
        self.__current_line = ""
        self.__current_cursor = 0
        self.__temp_word = []
        self.__current_word: str= None

    def next_word(self):
        while True:
            if self.__current_line == "":
                self.__current_line = self.__file_object.readline()
                if self.__current_line == "":
                    self.__current_word = None
                    return
            for i in range(self.__current_cursor, len(self.__current_line)):
                self.__current_cursor = i
                char: str = self.__current_line[i]
                if char == "<" or char == ">" or char == "=":
                    if self.__temp_word == []:
                        self.__current_cursor += 1
                        self.__current_word = char
                        return
                    else:
                        result = "".join(self.__temp_word)
                        self.__temp_word = []
                        self.__current_word = result
                        return
                elif char.isalnum() or char in {"_", ":"}:
                    self.__temp_word.append(char)
                    continue
                else:
                    if self.__temp_word == []:
                        continue
                    else:
                        result = "".join(self.__temp_word)
                        self.__temp_word = []
                        self.__current_word = result
                        return
            else:
                self.__current_line = ""
                self.__current_cursor = 0

    @property
    def current_word(self) -> str:
        return self.__current_word


class MotionStateDataReader:
    def __init__(self, file_path: str):
        self.__database: Dict[int, Dict[int, int]] = {}  # {region_id: {motion_state_id: total_time}}
        self.__read_file(file_path)


    def __read_file(self, file_path: str):
        with open(file_path, "r", True) as file:
            file_reader=_Reader(file)
            file_reader.next_word()
            while file_reader.current_word is not None:
                if file_reader.current_word in {"<",">"}:
                    file_reader.next_word()
                    continue
                list_=file_reader.current_word.split(":")
                region_id=int(list_[0])
                motion_state_id=int(list_[1])
                if region_id not in self.__database:
                    dict_={1:0,2:0,3:0}
                    self.__database[region_id]=dict_
                self.__database[region_id][motion_state_id] = self.__database[region_id][motion_state_id] + 1
                file_reader.next_word()

    @property
    def database(self) -> Dict[int, Dict[int, int]]:
        return self.__database

if __name__=="__main__":
    motion_state_reader=MotionStateDataReader("..\\simulation_data\\motion_state_data.msd")
    print(motion_state_reader.database)
