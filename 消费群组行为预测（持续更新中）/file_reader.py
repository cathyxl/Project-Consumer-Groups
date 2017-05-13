class FileReader:
    def __init__(self,new_file_object):
        self.__file_object=new_file_object
        self.__current_line=""
        self.__current_cursor=0
        self.__temp_word=[]

    def next_word(self):
        while True:
            if self.__current_line == "":
                self.__current_line=self.__file_object.readline()
                if self.__current_line=="":
                    return None
            for i in range(self.__current_cursor,len(self.__current_line)):
                self.__current_cursor = i
                char: str = self.__current_line[i]
                if char=="<" or char==">" or char=="=":
                    if self.__temp_word==[]:
                        self.__current_cursor+=1
                        return char
                    else:
                        result="".join(self.__temp_word)
                        self.__temp_word = []
                        return result
                elif char.isalnum() or char=="_":
                    self.__temp_word.append(char)
                    continue
                else:
                    if self.__temp_word==[]:
                        continue
                    else:
                        result = "".join(self.__temp_word)
                        self.__temp_word = []
                        return result
            else:
                self.__current_line = ""
                self.__current_cursor = 0
