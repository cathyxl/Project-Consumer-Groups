from typing import Dict

def predict_motion_state(motion_state_db: Dict[int, Dict[int, int]],region_id: int) -> str:
    dict_=motion_state_db[region_id]
    current_ms: str="静止"
    temp=dict_[1]
    if temp<dict_[2]:
        temp=dict_[2]
        current_ms="行走"
    if temp<dict_[3]:
        current_ms="奔跑"
    return current_ms
