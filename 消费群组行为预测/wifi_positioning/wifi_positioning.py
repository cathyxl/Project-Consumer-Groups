from typing import List, Tuple, Set, Generator
from numpy import sqrt

class _AccessPoint:
    def __init__(self,id: int,position: Tuple[float,float],signal_strength: float,attenuation_ability: float):
        self.id: int=id
        self.position: Tuple[float,float]=position
        self.signal_strength: float=signal_strength
        self.attenuation_ability: float=attenuation_ability

    def get_signal_strength(self,distance_away_from_ap: float) -> float:
        temp: float=self.signal_strength-self.attenuation_ability*distance_away_from_ap
        return temp if temp>0 else 0

class _ShoppingMall:
    def __init__(self,wifi_config_path: str):
        self.ap_list: List[_AccessPoint]=[]
        with open(wifi_config_path,"r",True) as config_file:
            line: str=config_file.readline()
            while line!= "":
                if line=="\n":
                    line = config_file.readline()
                    continue
                list1: List[str]=line.split(",")
                list2: List[str]=list1[1].lstrip("(").rstrip(")").split("/")
                position: Tuple[float,float]=(float(list2[0]),float(list2[1]))
                self.ap_list.append(_AccessPoint(int(list1[0]),position,float(list1[2]),float(list1[3])))
                line=config_file.readline()

class _Fingerprint:
    def __init__(self,position: Tuple[float,float],shopping_mall: _ShoppingMall):
        # self.position: Tuple[float, float] = position
        self.fingerprint: List[float] = []
        for ap in shopping_mall.ap_list:
            self.fingerprint.append(ap.get_signal_strength(self.__euclidean_distance(position, ap.position)))

    def __euclidean_distance(self,x: Tuple[float, float],y: Tuple[float, float]) -> float:
        return sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

    @classmethod
    def fingerprint_distance(cls,f1: "_Fingerprint",f2: "_Fingerprint") -> float:
        temp: float=0
        for index in range(len(f1.fingerprint)):
            temp+=(f1.fingerprint[index]-f2.fingerprint[index])**2
        return sqrt(temp)

class _ReferencePointFingerprint(_Fingerprint):
    def __init__(self,position: Tuple[float,float],shopping_mall: _ShoppingMall,region_id: int):
        super().__init__(position,shopping_mall)
        self.region_id=region_id

class _PositioningFingerprint(_Fingerprint):
    def __init__(self,position: Tuple[float,float],shopping_mall: _ShoppingMall):
        super().__init__(position,shopping_mall)

class _ReferencePointDatabase:
    def __init__(self,shopping_mall: _ShoppingMall):
        self.__reference_points: List[_ReferencePointFingerprint]=[]
        ignore_counts: Set[int]={17,18,19,24,25,26}
        for count in range(1,43):
            if count in ignore_counts:continue
            x: int=(count%7)*5
            y: int=(count//7+1)*5
            for m in range(x-4,x):
                for n in range(y-4,y):
                    self.__reference_points.append(_ReferencePointFingerprint((m, n), shopping_mall, count))

    def reference_points(self) -> Generator[_ReferencePointFingerprint,None,None]:
        for reference_point in self.__reference_points:
            yield reference_point

def _determine_locating_region(pos_fin: _PositioningFingerprint,ref_point_db: _ReferencePointDatabase) -> int:
    ref_points_cmp: List[Tuple[int,float]]=[]
    for ref_point in ref_point_db.reference_points():
        fin_distance: float= _Fingerprint.fingerprint_distance(pos_fin,ref_point)
        ref_points_cmp.append((ref_point.region_id,fin_distance))
    ref_points_cmp.sort(key=lambda x:x[1])
    sub_cmp_list=ref_points_cmp[:16]
    sub_cmp_list=list(map(lambda x:x[0],sub_cmp_list))
    #"""
    set_={x for x in sub_cmp_list}
    list_=[]
    for ele in set_:
        list_.append((ele,sub_cmp_list.count(ele)))
    list_.sort(key=lambda x:-x[1])
    result=list_[0][0]
    return result
    #"""
    #return sub_cmp_list[0]

def get_mall_wifi_db(wifi_ap_config_path: str):
    shopping_mall = _ShoppingMall(wifi_ap_config_path)
    return (shopping_mall,_ReferencePointDatabase(shopping_mall))

def position_it(point: Tuple[int, int],shopping_mall,ref_point_db):
    positioning_fingerprint = _PositioningFingerprint(point, shopping_mall)
    return _determine_locating_region(positioning_fingerprint, ref_point_db)

if __name__=="__main__":
    shopping_mall = _ShoppingMall("..\\simulation_data\\wifi_setting.config")
    ref_point_db = _ReferencePointDatabase(shopping_mall)
    positioning_fingerprint = _PositioningFingerprint((30,22),shopping_mall)
    print(_determine_locating_region(positioning_fingerprint,ref_point_db))
