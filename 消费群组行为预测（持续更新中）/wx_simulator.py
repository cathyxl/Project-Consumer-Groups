from typing import Tuple

import wx

from apriori_prediction.region_prediction import apriori, mine_and_predict_region
from positioning_data_creation.file_reader import FileReader
from positioning_data_creation.positioning_data_reader import PositioningDataReader

association_rule_tree=None  # 存储关联规则的树形结构

app=wx.App()
win=wx.Frame(None,title="单人消费者预测模拟")
win.SetSize(575,500)
bkg=wx.Panel(win)

st_support=wx.StaticText(bkg,label="Apriori支持度（整数）：")
st_confidence=wx.StaticText(bkg,label="Apriori置信度：50%")
btn_load_positioning_data=wx.Button(bkg,label="打开并挖掘定位记录")
btn_load_motion_data=wx.Button(bkg,label="打开行为动作记录文件")
tc_support_input=wx.TextCtrl(bkg,value="1")
slider_confidence=wx.Slider(bkg,style=wx.SL_MIN_MAX_LABELS,size=(420,0),value=50)

st_input_region_seq=wx.StaticText(bkg,label="输入模拟区域序列，区域用“-”隔开：")
tc_input_region_seq=wx.TextCtrl(bkg,value="")
btn_predict=wx.Button(bkg,label="执行预测")

st_forward_predict_num=wx.StaticText(bkg,label="指定向前预测区域的个数：")
tc_forward_predict_num=wx.TextCtrl(bkg,value="1")

result_area=wx.TextCtrl(bkg,style=wx.HSCROLL|wx.TE_MULTILINE)

#slider=wx.Slider(bkg,value=50,minValue=0,maxValue=100,style=wx.SL_AUTOTICKS|wx.SL_MIN_MAX_LABELS)
hbox1=wx.BoxSizer()
hbox1.Add(st_support,proportion=0,flag=wx.ALL,border=5)
hbox1.Add(tc_support_input,proportion=1,flag=wx.ALL,border=5)
hbox1.Add(btn_load_positioning_data,proportion=0,flag=wx.ALL,border=5)
hbox1.Add(btn_load_motion_data,proportion=0,flag=wx.ALL,border=5)
#hbox.Add(btn1,proportion=0,flag=wx.LEFT,border=0)
#hbox.Add(btn2,proportion=0,flag=wx.LEFT,border=0)
hbox2=wx.BoxSizer()
hbox2.Add(st_confidence,proportion=0,flag=wx.ALL,border=5)
hbox2.Add(slider_confidence,proportion=1,flag=wx.ALL,border=5)

hbox3=wx.BoxSizer()
hbox3.Add(wx.StaticText(bkg,label=""),proportion=0,flag=wx.ALL,border=5)

hbox4=wx.BoxSizer()
hbox4.Add(st_input_region_seq,proportion=0,flag=wx.ALL,border=5)
hbox4.Add(tc_input_region_seq,proportion=1,flag=wx.ALL,border=5)
hbox4.Add(btn_predict,proportion=0,flag=wx.ALL,border=5)

hbox5=wx.BoxSizer()
hbox5.Add(st_forward_predict_num,proportion=0,flag=wx.ALL,border=5)
hbox5.Add(tc_forward_predict_num,proportion=0,flag=wx.ALL,border=5)

hbox6=wx.BoxSizer()
hbox6.Add(result_area,proportion=1,flag=wx.ALL|wx.EXPAND,border=5)

vbox=wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox1,proportion=0,flag=wx.ALL,border=5)
vbox.Add(hbox2,proportion=0,flag=wx.ALL,border=5)
vbox.Add(hbox3,proportion=0,flag=wx.ALL,border=5)
vbox.Add(hbox4,proportion=0,flag=wx.ALL,border=5)
vbox.Add(hbox5,proportion=0,flag=wx.ALL,border=5)
vbox.Add(hbox6,proportion=1,flag=wx.ALL|wx.EXPAND,border=20)

bkg.SetSizer(vbox)

def func_on_change_slider(event):
    st_confidence.SetLabelText("Apriori置信度："+str(slider_confidence.GetValue())+"%")

def func_on_load_positioning_data(event):
    openFileDialog = wx.FileDialog(bkg,style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    if openFileDialog.ShowModal() == wx.ID_CANCEL:
        return
    file_path=openFileDialog.GetPath()
    with open(file_path,"r",True) as positioning_file:
        data_set = PositioningDataReader(FileReader(positioning_file)).get_data_set()
    result_area.WriteText("成功打开定位记录文件，正在进行关联规则挖掘...\n")
    global association_rule_tree
    association_rule_tree=apriori(data_set,int(tc_support_input.GetValue()),slider_confidence.GetValue()/100)
    result_area.WriteText("关联规则挖掘成功，已生成树形存储结构，可以开始进行预测。\n")

def func_on_predict(event):
    result: Tuple[Tuple[int], float] = mine_and_predict_region(association_rule_tree,
                                                               [int(i) for i in
                                                                tc_input_region_seq.GetValue().split("-")],
                                                               int(tc_forward_predict_num.GetValue()))
    result_area.WriteText("已经过区域序列："+str(tc_input_region_seq.GetValue())+"。预测结果："+str(result[0])+"。置信度："+str(result[1])+"。\n")

slider_confidence.Bind(wx.EVT_SLIDER,func_on_change_slider)
btn_load_positioning_data.Bind(wx.EVT_BUTTON,func_on_load_positioning_data)
btn_predict.Bind(wx.EVT_BUTTON,func_on_predict)

win.Show()
app.MainLoop()
