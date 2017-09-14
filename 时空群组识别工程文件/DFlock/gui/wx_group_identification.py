import wx,time
import display.Display as Display
import numpy as np
import matplotlib.pyplot as plt
import algorithms.flockdetection as FD
import algorithms.Color as color
import display.ServerPort as SP
import sys
"""创建Frame窗口"""
sys.path.append("..\\display")
app=wx.App()
frame=wx.Frame(None,title="Flock Recognition")
frame.SetSize(800,600)



"""创建Notebook -> 用来分页"""
notebook=wx.Notebook(frame)



"""创建 实时监控 Panel"""
panel_rtgd=wx.Panel(notebook)  # RTGD: Real-Time Graphical Display

# 创建所有静态文本
st_rtgd_eps=wx.StaticText(panel_rtgd,label="eps：")
st_rtgd_minpts=wx.StaticText(panel_rtgd,label="minPts：")
st_rtgd_gama=wx.StaticText(panel_rtgd,label="gama：")
st_rtgd_delta=wx.StaticText(panel_rtgd,label="delta：")
st_rtgd_frequency=wx.StaticText(panel_rtgd,label="frequency：2.48    ")
st_rtgd_clust_algori=wx.StaticText(panel_rtgd,label="Spatial Methods：")

# 创建下拉选项框
choice_rtgd=wx.Choice(panel_rtgd,choices=["DBSCAN","DJCluster"])
choice_rtgd.SetSelection(0)  # 设置默认值为DBSCAN

# 创建所有按钮
btn_rtgd_service_on=wx.Button(panel_rtgd,label="start monitor")
btn_rtgd_service_off=wx.Button(panel_rtgd,label="Shutdown")

def on_btn_rtgd_service_on_click(event):
    "参数设置"
    minPoints = int(tc_rtgd_minpts.GetValue())
    gama = int(tc_rtgd_gama.GetValue())
    delta = int(tc_rtgd_delta.GetValue())
    eps = float(tc_rtgd_eps.GetValue())
    spatialType = int(choice_rtgd.GetSelection())
    frequency = float(slider_rtgd_frequency.GetValue() / 100)
    print(eps, minPoints, gama, delta, frequency, spatialType)

    XAXISSIZE = 1000
    WIN = 100
    # fig, ax = plt.subplots()
    plt.axis([0, XAXISSIZE, 0, 10])
    ax = plt.axes()
    lst = SP.Listener(9011, eps, minPoints, gama, delta, spatialType, frequency, ax)
    lst.start()
    plt.show()
    # pass  # TODO 实时图形化 开启服务



btn_rtgd_service_on.Bind(wx.EVT_BUTTON, on_btn_rtgd_service_on_click)

def on_btn_rtgd_service_off_click(event):

    pass  # TODO 实时图形化 关闭服务

btn_rtgd_service_off.Bind(wx.EVT_BUTTON, on_btn_rtgd_service_off_click)

# 创建滑动条
slider_rtgd_frequency=wx.Slider(panel_rtgd,minValue=4,maxValue=500,size=(661,20),value=248)

def on_rtgd_slider_value_change(event):
    st_rtgd_frequency.SetLabelText("频率：" + str(slider_rtgd_frequency.GetValue()/100) + "    ")
slider_rtgd_frequency.Bind(wx.EVT_SLIDER, on_rtgd_slider_value_change)  # 移动滑块时同时显示数值大小

# 创建所有用来输入参数的文本输入框
tc_rtgd_eps=wx.TextCtrl(panel_rtgd,value="1.72")
tc_rtgd_minpts=wx.TextCtrl(panel_rtgd,value="2")
tc_rtgd_gama=wx.TextCtrl(panel_rtgd,value="4")
tc_rtgd_delta=wx.TextCtrl(panel_rtgd,value="2")

# 创建用来显示输出的文本框
tc_rtgd_output=wx.TextCtrl(panel_rtgd,style=wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)

# 使用BoxSizer管理所有控件的位置
hbox_rtgd_1=wx.BoxSizer()
hbox_rtgd_eps=wx.BoxSizer()
hbox_rtgd_minpts=wx.BoxSizer()
hbox_rtgd_delta=wx.BoxSizer()
hbox_rtgd_theta=wx.BoxSizer()
vbox_rtgd_eps=wx.BoxSizer(wx.VERTICAL)
vbox_rtgd_minpts=wx.BoxSizer(wx.VERTICAL)
vbox_rtgd_delta=wx.BoxSizer(wx.VERTICAL)
vbox_rtgd_theta=wx.BoxSizer(wx.VERTICAL)
hbox_rtgd_eps.Add(st_rtgd_eps,flag=wx.ALIGN_CENTER)
hbox_rtgd_eps.Add(tc_rtgd_eps,flag=wx.ALIGN_CENTER)
vbox_rtgd_eps.Add(hbox_rtgd_eps,flag=wx.ALIGN_CENTER)
hbox_rtgd_minpts.Add(st_rtgd_minpts,flag=wx.ALIGN_CENTER)
hbox_rtgd_minpts.Add(tc_rtgd_minpts,flag=wx.ALIGN_CENTER)
vbox_rtgd_minpts.Add(hbox_rtgd_minpts,flag=wx.ALIGN_CENTER)
hbox_rtgd_delta.Add(st_rtgd_gama,flag=wx.ALIGN_CENTER)
hbox_rtgd_delta.Add(tc_rtgd_gama,flag=wx.ALIGN_CENTER)
vbox_rtgd_delta.Add(hbox_rtgd_delta,flag=wx.ALIGN_CENTER)
hbox_rtgd_theta.Add(st_rtgd_delta,flag=wx.ALIGN_CENTER)
hbox_rtgd_theta.Add(tc_rtgd_delta,flag=wx.ALIGN_CENTER)
vbox_rtgd_theta.Add(hbox_rtgd_theta,flag=wx.ALIGN_CENTER)
hbox_rtgd_1.Add(vbox_rtgd_eps,proportion=1,flag=wx.ALL,border=20)
hbox_rtgd_1.Add(vbox_rtgd_minpts,proportion=1,flag=wx.ALL,border=20)
hbox_rtgd_1.Add(vbox_rtgd_delta,proportion=1,flag=wx.ALL,border=20)
hbox_rtgd_1.Add(vbox_rtgd_theta,proportion=1,flag=wx.ALL,border=20)

hbox_rtgd_2=wx.BoxSizer()
hbox_rtgd_slider_region=wx.BoxSizer()
vbox_rtgd_slider_region=wx.BoxSizer(wx.VERTICAL)
hbox_rtgd_slider_region.Add(st_rtgd_frequency,flag=wx.ALIGN_CENTER)
hbox_rtgd_slider_region.Add(slider_rtgd_frequency)
vbox_rtgd_slider_region.Add(hbox_rtgd_slider_region,flag=wx.ALIGN_CENTER)
hbox_rtgd_2.Add(vbox_rtgd_slider_region,proportion=1,flag=wx.ALL,border=20)

hbox_rtgd_3=wx.BoxSizer()
vbox_rtgd_clust_algori=wx.BoxSizer(wx.VERTICAL)
vbox_rtgd_service_on=wx.BoxSizer(wx.VERTICAL)
vbox_rtgd_plot=wx.BoxSizer(wx.VERTICAL)
vbox_rtgd_clust_algori.Add(st_rtgd_clust_algori,flag=wx.ALIGN_CENTER)
vbox_rtgd_clust_algori.Add(choice_rtgd,flag=wx.ALIGN_CENTER)
vbox_rtgd_service_on.Add(btn_rtgd_service_on,flag=wx.ALIGN_CENTER)
vbox_rtgd_plot.Add(btn_rtgd_service_off,flag=wx.ALIGN_CENTER)
hbox_rtgd_3.Add(vbox_rtgd_clust_algori,proportion=1,flag=wx.ALL,border=20)
hbox_rtgd_3.Add(vbox_rtgd_service_on,proportion=1,flag=wx.ALL,border=20)
hbox_rtgd_3.Add(vbox_rtgd_plot,proportion=1,flag=wx.ALL,border=20)

hbox_rtgd_4=wx.BoxSizer()
hbox_rtgd_4.Add(tc_rtgd_output,proportion=1,flag=wx.ALL|wx.EXPAND,border=20)

vbox_rtgd=wx.BoxSizer(wx.VERTICAL)
vbox_rtgd.Add(hbox_rtgd_1,flag=wx.EXPAND)
vbox_rtgd.Add(hbox_rtgd_2,flag=wx.EXPAND)
vbox_rtgd.Add(hbox_rtgd_3,flag=wx.EXPAND)
vbox_rtgd.Add(hbox_rtgd_4,proportion=1,flag=wx.EXPAND)

panel_rtgd.SetSizer(vbox_rtgd)



"""创建 Flock识别 Panel"""
panel_flock=wx.Panel(notebook)

# 创建所有静态文本
st_flock_eps=wx.StaticText(panel_flock,label="eps：")
st_flock_minpts=wx.StaticText(panel_flock,label="minPts：")
st_flock_gama=wx.StaticText(panel_flock,label="gama：")
st_flock_delta=wx.StaticText(panel_flock,label="delta：")
st_flock_frequency=wx.StaticText(panel_flock,label="频率：2.48    ")
st_flock_file=wx.StaticText(panel_flock,label="路径：")
st_flock_clust_algori=wx.StaticText(panel_flock,label="聚类方法：")
# st_flock_file=wx.StaticText(panel_flock,label="文件名：")
# 创建下拉选项框
choice_flock=wx.Choice(panel_flock,choices=["DBSCAN","DJCluster"])
choice_flock.SetSelection(0)  # 设置默认值为DBSCAN

# 创建所有按钮
btn_flock_choose_file=wx.Button(panel_flock,label="选择文件")
btn_flock_plot=wx.Button(panel_flock,label="绘制图形")

def on_btn_flock_choose_file_click(event):
    # TODO Flock识别 处理打开的文件
    openFileDialog = wx.FileDialog(panel_flock, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    if openFileDialog.ShowModal() == wx.ID_CANCEL:
        return
    file_path = openFileDialog.GetPath()
    st_flock_file.SetLabelText(file_path)

btn_flock_choose_file.Bind(wx.EVT_BUTTON,on_btn_flock_choose_file_click)

def on_btn_flock_plot_click(event):
    # TODO Fock 识别

    "参数设置"
    typeDistance = 0
    minPoints = int(tc_flock_minpts.GetValue())
    t0 = 0
    gama = int(tc_flock_gama.GetValue())
    delta = int(tc_flock_delta.GetValue())
    theta = 0.4
    eps = float(tc_flock_eps.GetValue())
    spatialType = int(choice_flock.GetSelection())
    frequency = float(slider_flock_frequency.GetValue() / 100)
    flock_file = st_flock_file.GetLabelText()
    print(flock_file, eps, minPoints, gama, delta, frequency, spatialType)

    "读取数据"
    pointmatrix, IDs = Display.readOriginFile(flock_file)
    print(IDs)

    "初始值设置"
    act_flocks = []
    pot_flocks = []
    curid = 0
    colorlist = np.zeros((2, 3))
    for j in range(3):
        colorlist[0][j] = 1
    for j in range(3):
        colorlist[1][j] = 0.9
    data = np.zeros((0, 0))
    lasttype = []
    assigned = [0, 0, 0, 0, 0, 0]
    flockmap = {}
    cmap = {}
    maxid = -2
    TSNUM = len(pointmatrix)
    WIN = 100
    tss = []
    for ts in pointmatrix:
        tss.append(ts)
    start = 0
    end = 0
    # fig, ax = plt.subplots()
    XAXISSIZE = 1000
    plt.axis([0, XAXISSIZE, 0, len(IDs)])
    ax = plt.axis()
    Display.drawFlock(colorlist, data, IDs, ax, start)
    while start < TSNUM:
        time.sleep(1)
        pointmap = {}
        end = start + WIN
        if end >= TSNUM:
            end = TSNUM
        for tsi in range(start, end):
            ts = tss[tsi]
            if ts not in pointmap:
                pointmap[ts] = pointmatrix[ts]
        start = end
        "下一次传送数据"
        draw_array, flockmap, act_flocks, pot_flocks, curid = FD.rtFlockDetect(IDs, gama, delta, pointmap, eps,
                                                                               minPoints,
                                                                               typeDistance, theta, act_flocks,
                                                                               pot_flocks,
                                                                               flockmap, curid, spatialType)
        draw_array1 = np.transpose(draw_array)
        data = Display.combinedata(data, draw_array1)
        "获得色彩数组"
        colorlist, lasttype, assigned, cmap, maxid = color.chooseColor(colorlist, draw_array, lasttype, assigned, cmap,
                                                                       maxid)
        print(list(colorlist))
        "画图"
        plt.clf()
        Display.drawFlock(colorlist, data, IDs, ax, start)
    plt.show()






btn_flock_plot.Bind(wx.EVT_BUTTON, on_btn_flock_plot_click)

# 创建滑动条
slider_flock_frequency=wx.Slider(panel_flock,minValue=4,maxValue=500,size=(661,20),value=248)

def on_flock_slider_value_change(event):
    st_flock_frequency.SetLabelText("频率：" + str(slider_flock_frequency.GetValue()/100) + "    ")
slider_flock_frequency.Bind(wx.EVT_SLIDER, on_flock_slider_value_change)  # 移动滑块时同时显示数值大小

# 创建所有用来输入参数的文本输入框
tc_flock_eps=wx.TextCtrl(panel_flock,value="1.72")
tc_flock_minpts=wx.TextCtrl(panel_flock,value="2")
tc_flock_gama=wx.TextCtrl(panel_flock,value="4")
tc_flock_delta=wx.TextCtrl(panel_flock,value="2")

# 创建用来显示输出的文本框
tmpvalue='Server Started,port 9011 \n 1 [0 1 0 (1,2,3,4,5)][1 1 0 (7,8,9,6)]\n\
2 [0 2 0 (1,2,3,4,5)][1 2 0 (6,7,8,9)]\n\
3 [0 3 0 (1,2,3,4,5)][1 3 0 (6,7,8,9)]\n\
4 [0 4 0 (1,2,3,4,5)][1 4 0 (6,7,8,9)]\n\
5 [0 5 0 (2,5,1,3,4)][1 5 0 (6,7,9,8)]\n\
6 [0 6 0 (2,5,1,4,3)][1 6 0 (6,8,9,7)]\n\
7 [0 7 0 (1,2,5,4,3)][1 7 0 (6,8,9,7)]\n\
8 [0 8 0 (6,7,8,9,5,2,1,3,4)][1 7 1 (6,8,9,7)]\n\
9 [0 9 0 (5,6,7,8,9,2,1,3,4)][1 7 2 (6,8,9,7)]\n\
10 [0 10 0 (1,2,3,5,6,7,8,9,4)]\n\
11 [0 11 0 (1,2,3,4,5,6,7,8,9)]\n\
12 [0 12 0 (1,3,4,5,6,8,9,2,7)]\n\
13 [0 13 0 (1,5,8,9,4,6,3,7,2)]\n\
14 [0 14 0 (1,5,6,7,8,9,4,3,2)]\n\
15 [0 15 0 (1,4,5,6,7,8,9,3,2)]\n\
16 [0 16 0 (1,4,6,7,8,9,5,2,3)]\n\
17 [0 17 0 (6,7,8,9,4,2,3,5,1)]\n\
18 [0 18 0 (1,2,3,5)][2 1 0 (4)][3 1 0 (6,7,8,9)]\n\
19 [0 19 0 (1,2,3,5)][2 2 0 (4)][3 2 0 (6,7,8,9)]\n\
20 [0 20 0 (2,3,5)][2 3 0 (1,4)][3 3 0 (7,9,6)][4 1 0 (8)]\n\
21 [0 21 0 (2,3,5)][2 4 0 (1,4)][3 4 0 (7,9,6)][4 2 0 (8)]'
tmpvalue=''
tc_flock_output=wx.TextCtrl(panel_flock,value=tmpvalue,style=wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)

# 使用BoxSizer管理所有控件的位置
hbox_flock_1=wx.BoxSizer()
hbox_flock_eps=wx.BoxSizer()
hbox_flock_minpts=wx.BoxSizer()
hbox_flock_delta=wx.BoxSizer()
hbox_flock_theta=wx.BoxSizer()
vbox_flock_eps=wx.BoxSizer(wx.VERTICAL)
vbox_flock_minpts=wx.BoxSizer(wx.VERTICAL)
vbox_flock_delta=wx.BoxSizer(wx.VERTICAL)
vbox_flock_theta=wx.BoxSizer(wx.VERTICAL)
hbox_flock_eps.Add(st_flock_eps,flag=wx.ALIGN_CENTER)
hbox_flock_eps.Add(tc_flock_eps,flag=wx.ALIGN_CENTER)
vbox_flock_eps.Add(hbox_flock_eps,flag=wx.ALIGN_CENTER)
hbox_flock_minpts.Add(st_flock_minpts,flag=wx.ALIGN_CENTER)
hbox_flock_minpts.Add(tc_flock_minpts,flag=wx.ALIGN_CENTER)
vbox_flock_minpts.Add(hbox_flock_minpts,flag=wx.ALIGN_CENTER)
hbox_flock_delta.Add(st_flock_gama,flag=wx.ALIGN_CENTER)
hbox_flock_delta.Add(tc_flock_gama,flag=wx.ALIGN_CENTER)
vbox_flock_delta.Add(hbox_flock_delta,flag=wx.ALIGN_CENTER)
hbox_flock_theta.Add(st_flock_delta,flag=wx.ALIGN_CENTER)
hbox_flock_theta.Add(tc_flock_delta,flag=wx.ALIGN_CENTER)
vbox_flock_theta.Add(hbox_flock_theta,flag=wx.ALIGN_CENTER)
hbox_flock_1.Add(vbox_flock_eps,proportion=1,flag=wx.ALL,border=20)
hbox_flock_1.Add(vbox_flock_minpts,proportion=1,flag=wx.ALL,border=20)
hbox_flock_1.Add(vbox_flock_delta,proportion=1,flag=wx.ALL,border=20)
hbox_flock_1.Add(vbox_flock_theta,proportion=1,flag=wx.ALL,border=20)

hbox_flock_2=wx.BoxSizer()
hbox_flock_slider_region=wx.BoxSizer()
vbox_flock_slider_region=wx.BoxSizer(wx.VERTICAL)
hbox_flock_slider_region.Add(st_flock_frequency,flag=wx.ALIGN_CENTER)
hbox_flock_slider_region.Add(slider_flock_frequency)
vbox_flock_slider_region.Add(hbox_flock_slider_region,flag=wx.ALIGN_CENTER)
hbox_flock_2.Add(vbox_flock_slider_region,proportion=1,flag=wx.ALL,border=20)

hbox_flock_3=wx.BoxSizer()
vbox_flock_choose_file=wx.BoxSizer(wx.VERTICAL)
vbox_flock_clust_algori=wx.BoxSizer(wx.VERTICAL)
vbox_flock_plot=wx.BoxSizer(wx.VERTICAL)
vbox_flock_choose_file.Add(btn_flock_choose_file,flag=wx.ALIGN_CENTER)
vbox_flock_choose_file.Add(st_flock_file,flag=wx.ALIGN_CENTER)
vbox_flock_clust_algori.Add(st_flock_clust_algori,flag=wx.ALIGN_CENTER)
vbox_flock_clust_algori.Add(choice_flock,flag=wx.ALIGN_CENTER)
vbox_flock_plot.Add(btn_flock_plot,flag=wx.ALIGN_CENTER)
hbox_flock_3.Add(vbox_flock_choose_file,proportion=1,flag=wx.ALL,border=20)
hbox_flock_3.Add(vbox_flock_clust_algori,proportion=1,flag=wx.ALL,border=20)
hbox_flock_3.Add(vbox_flock_plot,proportion=1,flag=wx.ALL,border=20)


hbox_flock_4=wx.BoxSizer()
hbox_flock_4.Add(tc_flock_output,proportion=1,flag=wx.ALL|wx.EXPAND,border=20)

vbox_flock=wx.BoxSizer(wx.VERTICAL)
vbox_flock.Add(hbox_flock_1,flag=wx.EXPAND)
vbox_flock.Add(hbox_flock_2,flag=wx.EXPAND)
vbox_flock.Add(hbox_flock_3,flag=wx.EXPAND)
vbox_flock.Add(hbox_flock_4,proportion=1,flag=wx.EXPAND)

panel_flock.SetSizer(vbox_flock)


# """创建 DBAD识别 Panel"""
# panel_dbad=wx.Panel(notebook)
#
# # 创建所有按钮
# btn_dbad_choose_file=wx.Button(panel_dbad,label="选择文件")
# btn_dbad_start_recog=wx.Button(panel_dbad,label="开始识别")
#
# def on_btn_dbad_choose_file_click(event):
#     openFileDialog = wx.FileDialog(panel_dbad, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
#     if openFileDialog.ShowModal() == wx.ID_CANCEL:
#         return
#     file_path = openFileDialog.GetPath()
#
#     # TODO DBAD识别 处理打开的文件
#
# btn_dbad_choose_file.Bind(wx.EVT_BUTTON,on_btn_dbad_choose_file_click)
#
# def on_btn_dbad_start_recog_click(event):
#     pass  # TODO DBAD识别 开始识别
# btn_dbad_start_recog.Bind(wx.EVT_BUTTON, on_btn_dbad_start_recog_click)
#
# # 创建所有静态文本标签
# st_dbad_sensor_type=wx.StaticText(panel_dbad,label="传感器类型：")
# st_dbad_filter_length=wx.StaticText(panel_dbad,label="Filter Length：2    ")
# st_dbad_winsize=wx.StaticText(panel_dbad,label="WinSize：3000    ")
#
# # 创建所有滑动条
# slider_dbad_filter_length=wx.Slider(panel_dbad,maxValue=5,style=wx.SL_MIN_MAX_LABELS,size=(500,0),value=2)
# slider_dbad_winsize=wx.Slider(panel_dbad,minValue=1000,maxValue=5000,style=wx.SL_MIN_MAX_LABELS,size=(500,0),value=3000)
#
# def on_dbad_slider_filter_length_value_change(event):
#     st_dbad_filter_length.SetLabelText("Filter Length：" + str(slider_dbad_filter_length.GetValue()) + "    ")
# slider_dbad_filter_length.Bind(wx.EVT_SLIDER, on_dbad_slider_filter_length_value_change)  # 移动滑块时同时显示数值大小
#
# def on_dbad_slider_winsize_value_change(event):
#     st_dbad_winsize.SetLabelText("WinSize：" + str(slider_dbad_winsize.GetValue()) + "    ")
# slider_dbad_winsize.Bind(wx.EVT_SLIDER, on_dbad_slider_winsize_value_change)  # 移动滑块时同时显示数值大小
#
# # 创建下拉选项框
# choice_dbad=wx.Choice(panel_dbad,choices=["加速度","方向"])
# choice_dbad.SetSelection(0)  # 设置默认值为加速度
#
# # 创建用来显示输出的文本框
# # tc_dbad_output=wx.TextCtrl(panel_dbad, value="分组结果：[[1, 2, 3, 4, 11], [5, 6], [7], [9]]", style=wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)
# tc_dbad_output=wx.TextCtrl(panel_dbad, style=wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)
#
# # 使用BoxSizer管理所有控件的位置
# hbox_dbad_1=wx.BoxSizer()
# vbox_dbad_choose_file=wx.BoxSizer(wx.VERTICAL)
# vbox_dbad_sensor_type=wx.BoxSizer(wx.VERTICAL)
# vbox_dbad_start_recog=wx.BoxSizer(wx.VERTICAL)
# vbox_dbad_choose_file.Add(btn_dbad_choose_file,flag=wx.ALIGN_CENTER)
# vbox_dbad_sensor_type.Add(st_dbad_sensor_type,flag=wx.ALIGN_CENTER)
# vbox_dbad_sensor_type.Add(choice_dbad,flag=wx.ALIGN_CENTER)
# vbox_dbad_start_recog.Add(btn_dbad_start_recog,flag=wx.ALIGN_CENTER)
# hbox_dbad_1.Add(vbox_dbad_choose_file,proportion=1,flag=wx.ALL,border=20)
# hbox_dbad_1.Add(vbox_dbad_sensor_type,proportion=1,flag=wx.ALL,border=20)
# hbox_dbad_1.Add(vbox_dbad_start_recog,proportion=1,flag=wx.ALL,border=20)
#
# hbox_dbad_2=wx.BoxSizer()
# hbox_dbad_slider_filter_length_region=wx.BoxSizer()
# vbox_dbad_slider_filter_length_region=wx.BoxSizer(wx.VERTICAL)
# hbox_dbad_slider_filter_length_region.Add(st_dbad_filter_length,flag=wx.ALIGN_BOTTOM)
# hbox_dbad_slider_filter_length_region.Add(slider_dbad_filter_length)
# vbox_dbad_slider_filter_length_region.Add(hbox_dbad_slider_filter_length_region,flag=wx.ALIGN_CENTER)
# hbox_dbad_2.Add(vbox_dbad_slider_filter_length_region,proportion=1,flag=wx.ALL,border=20)
#
# hbox_dbad_3=wx.BoxSizer()
# hbox_dbad_slider_winsize_region=wx.BoxSizer()
# vbox_dbad_slider_winsize_region=wx.BoxSizer(wx.VERTICAL)
# hbox_dbad_slider_winsize_region.Add(st_dbad_winsize,flag=wx.ALIGN_BOTTOM)
# hbox_dbad_slider_winsize_region.Add(slider_dbad_winsize)
# vbox_dbad_slider_winsize_region.Add(hbox_dbad_slider_winsize_region,flag=wx.ALIGN_CENTER)
# hbox_dbad_3.Add(vbox_dbad_slider_winsize_region,proportion=1,flag=wx.ALL,border=20)
#
# hbox_dbad_4=wx.BoxSizer()
# hbox_dbad_4.Add(tc_dbad_output,proportion=1,flag=wx.ALL|wx.EXPAND,border=20)
#
# vbox_dbad=wx.BoxSizer(wx.VERTICAL)
# vbox_dbad.Add(hbox_dbad_1,flag=wx.EXPAND)
# vbox_dbad.Add(hbox_dbad_2,flag=wx.EXPAND)
# vbox_dbad.Add(hbox_dbad_3,flag=wx.EXPAND)
# vbox_dbad.Add(hbox_dbad_4,proportion=1,flag=wx.EXPAND)
#
# panel_dbad.SetSizer(vbox_dbad)
#
#
#
# """创建 GBA识别 Panel"""
# panel_gba=wx.Panel(notebook)
#
# # 创建所有按钮
# btn_gba_choose_file=wx.Button(panel_gba,label="选择文件")
# btn_gba_start_recog=wx.Button(panel_gba,label="开始识别")
#
# def on_btn_gba_choose_file_click(event):
#     openFileDialog = wx.FileDialog(panel_gba, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
#     if openFileDialog.ShowModal() == wx.ID_CANCEL:
#         return
#     file_path = openFileDialog.GetPath()
#     # TODO GBA识别 处理打开的文件
# btn_gba_choose_file.Bind(wx.EVT_BUTTON,on_btn_gba_choose_file_click)
#
# def on_btn_gba_start_recog_click(event):
#     pass  # TODO GBA识别 开始识别
# btn_gba_start_recog.Bind(wx.EVT_BUTTON, on_btn_gba_start_recog_click)
#
# # 创建所有静态文本标签
# st_gba_behavior_winsize=wx.StaticText(panel_gba,label="Behavior WinSize：2000    ")
# st_gba_group_winsize=wx.StaticText(panel_gba,label="Group WinSize：10    ")
#
# # 创建所有滑动条
# slider_gba_behavior_winsize=wx.Slider(panel_gba,minValue=1000,maxValue=3000,style=wx.SL_MIN_MAX_LABELS,size=(500,0),value=2000)
# slider_gba_group_winsize=wx.Slider(panel_gba,maxValue=20,style=wx.SL_MIN_MAX_LABELS,size=(500,0),value=10)
#
# def on_gba_slider_behavior_winsize_value_change(event):
#     st_gba_behavior_winsize.SetLabelText("Filter Length：" + str(slider_gba_behavior_winsize.GetValue()) + "    ")
# slider_gba_behavior_winsize.Bind(wx.EVT_SLIDER, on_gba_slider_behavior_winsize_value_change)  # 移动滑块时同时显示数值大小
#
# def on_gba_slider_group_winsize_value_change(event):
#     st_gba_group_winsize.SetLabelText("Group WinSize：" + str(slider_gba_group_winsize.GetValue()) + "    ")
# slider_gba_group_winsize.Bind(wx.EVT_SLIDER, on_gba_slider_group_winsize_value_change)  # 移动滑块时同时显示数值大小
#
# # 创建用来显示输出的文本框
# # tc_gba_output=wx.TextCtrl(panel_gba,value="分组结果：[[1, 2, 3, 4, 11], [5, 6], [7], [9]]", style=wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)
# tc_gba_output=wx.TextCtrl(panel_gba, style=wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)
#
# # 使用BoxSizer管理所有控件的位置
# hbox_gba_1=wx.BoxSizer()
# vbox_gba_choose_file=wx.BoxSizer(wx.VERTICAL)
# vbox_gba_start_recog=wx.BoxSizer(wx.VERTICAL)
# vbox_gba_choose_file.Add(btn_gba_choose_file,flag=wx.ALIGN_CENTER)
# vbox_gba_start_recog.Add(btn_gba_start_recog,flag=wx.ALIGN_CENTER)
# hbox_gba_1.Add(vbox_gba_choose_file,proportion=1,flag=wx.ALL,border=20)
# hbox_gba_1.Add(vbox_gba_start_recog,proportion=1,flag=wx.ALL,border=20)
#
# hbox_gba_2=wx.BoxSizer()
# hbox_gba_slider_behavior_winsize_region=wx.BoxSizer()
# vbox_gba_slider_behavior_winsize_region=wx.BoxSizer(wx.VERTICAL)
# hbox_gba_slider_behavior_winsize_region.Add(st_gba_behavior_winsize,flag=wx.ALIGN_BOTTOM)
# hbox_gba_slider_behavior_winsize_region.Add(slider_gba_behavior_winsize)
# vbox_gba_slider_behavior_winsize_region.Add(hbox_gba_slider_behavior_winsize_region,flag=wx.ALIGN_CENTER)
# hbox_gba_2.Add(vbox_gba_slider_behavior_winsize_region,proportion=1,flag=wx.ALL,border=20)
#
# hbox_gba_3=wx.BoxSizer()
# hbox_gba_slider_group_winsize_region=wx.BoxSizer()
# vbox_gba_slider_group_winsize_region=wx.BoxSizer(wx.VERTICAL)
# hbox_gba_slider_group_winsize_region.Add(st_gba_group_winsize,flag=wx.ALIGN_BOTTOM)
# hbox_gba_slider_group_winsize_region.Add(slider_gba_group_winsize)
# vbox_gba_slider_group_winsize_region.Add(hbox_gba_slider_group_winsize_region,flag=wx.ALIGN_CENTER)
# hbox_gba_3.Add(vbox_gba_slider_group_winsize_region,proportion=1,flag=wx.ALL,border=20)
#
# hbox_gba_4=wx.BoxSizer()
# hbox_gba_4.Add(tc_gba_output,proportion=1,flag=wx.ALL|wx.EXPAND,border=20)
#
# vbox_gba=wx.BoxSizer(wx.VERTICAL)
# vbox_gba.Add(hbox_gba_1,flag=wx.EXPAND)
# vbox_gba.Add(hbox_gba_2,flag=wx.EXPAND)
# vbox_gba.Add(hbox_gba_3,flag=wx.EXPAND)
# vbox_gba.Add(hbox_gba_4,proportion=1,flag=wx.EXPAND)
#
# panel_gba.SetSizer(vbox_gba)
#
#
#
# """创建 CC识别 Panel"""
# panel_cc=wx.Panel(notebook)
#
# # 创建所有按钮
# btn_cc_choose_file=wx.Button(panel_cc,label="选择文件")
# btn_cc_start_recog=wx.Button(panel_cc,label="开始识别")
#
# def on_btn_cc_choose_file_click(event):
#     openFileDialog = wx.FileDialog(panel_cc, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
#     if openFileDialog.ShowModal() == wx.ID_CANCEL:
#         return
#     file_path = openFileDialog.GetPath()
#     # TODO CC识别 处理打开的文件
# btn_cc_choose_file.Bind(wx.EVT_BUTTON,on_btn_cc_choose_file_click)
#
# def on_btn_cc_start_recog_click(event):
#     pass  # TODO cc识别 开始识别
# btn_cc_start_recog.Bind(wx.EVT_BUTTON, on_btn_cc_start_recog_click)
#
# # 创建所有静态文本标签
# st_cc_sensor_type=wx.StaticText(panel_cc,label="传感器类型：")
# st_cc_filter_length=wx.StaticText(panel_cc,label="Filter Length：2    ")
# st_cc_winsize=wx.StaticText(panel_cc,label="WinSize：3000    ")
# st_cc_delay=wx.StaticText(panel_cc,label="Delay：5    ")
#
# # 创建所有滑动条
# slider_cc_filter_length=wx.Slider(panel_cc,maxValue=5,style=wx.SL_MIN_MAX_LABELS,size=(500,0),value=2)
# slider_cc_winsize=wx.Slider(panel_cc,minValue=1000,maxValue=5000,style=wx.SL_MIN_MAX_LABELS,size=(500,0),value=3000)
# slider_cc_delay=wx.Slider(panel_cc,maxValue=10,style=wx.SL_MIN_MAX_LABELS,size=(500,0),value=5)
#
# def on_cc_slider_filter_length_value_change(event):
#     st_cc_filter_length.SetLabelText("Filter Length：" + str(slider_cc_filter_length.GetValue()) + "    ")
# slider_cc_filter_length.Bind(wx.EVT_SLIDER, on_cc_slider_filter_length_value_change)  # 移动滑块时同时显示数值大小
#
# def on_cc_slider_winsize_value_change(event):
#     st_cc_winsize.SetLabelText("WinSize：" + str(slider_cc_winsize.GetValue()) + "    ")
# slider_cc_winsize.Bind(wx.EVT_SLIDER, on_cc_slider_winsize_value_change)  # 移动滑块时同时显示数值大小
#
# def on_cc_slider_delay_value_change(event):
#     st_cc_delay.SetLabelText("Delay：" + str(slider_cc_delay.GetValue()) + "    ")
# slider_cc_delay.Bind(wx.EVT_SLIDER, on_cc_slider_delay_value_change)  # 移动滑块时同时显示数值大小
#
# # 创建下拉选项框
# choice_cc=wx.Choice(panel_cc,choices=["加速度","方向"])
# choice_cc.SetSelection(0)  # 设置默认值为加速度
#
# # 创建用来显示输出的文本框
# # tc_cc_output=wx.TextCtrl(panel_cc,value="分组结果：[[1, 2, 3, 4, 11], [5, 6], [7], [9]]",style=wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)
# tc_cc_output=wx.TextCtrl(panel_cc,value="",style=wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)
#
# # 使用BoxSizer管理所有控件的位置
# hbox_cc_1=wx.BoxSizer()
# vbox_cc_choose_file=wx.BoxSizer(wx.VERTICAL)
# vbox_cc_sensor_type=wx.BoxSizer(wx.VERTICAL)
# vbox_cc_start_recog=wx.BoxSizer(wx.VERTICAL)
# vbox_cc_choose_file.Add(btn_cc_choose_file,flag=wx.ALIGN_CENTER)
# vbox_cc_sensor_type.Add(st_cc_sensor_type,flag=wx.ALIGN_CENTER)
# vbox_cc_sensor_type.Add(choice_cc,flag=wx.ALIGN_CENTER)
# vbox_cc_start_recog.Add(btn_cc_start_recog,flag=wx.ALIGN_CENTER)
# hbox_cc_1.Add(vbox_cc_choose_file,proportion=1,flag=wx.ALL,border=20)
# hbox_cc_1.Add(vbox_cc_sensor_type,proportion=1,flag=wx.ALL,border=20)
# hbox_cc_1.Add(vbox_cc_start_recog,proportion=1,flag=wx.ALL,border=20)
#
# hbox_cc_2=wx.BoxSizer()
# hbox_cc_slider_filter_length_region=wx.BoxSizer()
# vbox_cc_slider_filter_length_region=wx.BoxSizer(wx.VERTICAL)
# hbox_cc_slider_filter_length_region.Add(st_cc_filter_length,flag=wx.ALIGN_BOTTOM)
# hbox_cc_slider_filter_length_region.Add(slider_cc_filter_length)
# vbox_cc_slider_filter_length_region.Add(hbox_cc_slider_filter_length_region,flag=wx.ALIGN_CENTER)
# hbox_cc_2.Add(vbox_cc_slider_filter_length_region,proportion=1,flag=wx.ALL,border=20)
#
# hbox_cc_3=wx.BoxSizer()
# hbox_cc_slider_winsize_region=wx.BoxSizer()
# vbox_cc_slider_winsize_region=wx.BoxSizer(wx.VERTICAL)
# hbox_cc_slider_winsize_region.Add(st_cc_winsize,flag=wx.ALIGN_BOTTOM)
# hbox_cc_slider_winsize_region.Add(slider_cc_winsize)
# vbox_cc_slider_winsize_region.Add(hbox_cc_slider_winsize_region,flag=wx.ALIGN_CENTER)
# hbox_cc_3.Add(vbox_cc_slider_winsize_region,proportion=1,flag=wx.ALL,border=20)
#
# hbox_cc_4=wx.BoxSizer()
# hbox_cc_slider_delay_region=wx.BoxSizer()
# vbox_cc_slider_delay_region=wx.BoxSizer(wx.VERTICAL)
# hbox_cc_slider_delay_region.Add(st_cc_delay,flag=wx.ALIGN_BOTTOM)
# hbox_cc_slider_delay_region.Add(slider_cc_delay)
# vbox_cc_slider_delay_region.Add(hbox_cc_slider_delay_region,flag=wx.ALIGN_CENTER)
# hbox_cc_4.Add(vbox_cc_slider_delay_region,proportion=1,flag=wx.ALL,border=20)
#
# hbox_cc_5=wx.BoxSizer()
# hbox_cc_5.Add(tc_cc_output,proportion=1,flag=wx.ALL|wx.EXPAND,border=20)
#
# vbox_cc=wx.BoxSizer(wx.VERTICAL)
# vbox_cc.Add(hbox_cc_1,flag=wx.EXPAND)
# vbox_cc.Add(hbox_cc_2,flag=wx.EXPAND)
# vbox_cc.Add(hbox_cc_3,flag=wx.EXPAND)
# vbox_cc.Add(hbox_cc_4,flag=wx.EXPAND)
# vbox_cc.Add(hbox_cc_5,proportion=1,flag=wx.EXPAND)
#
# panel_cc.SetSizer(vbox_cc)



"""将所有Panel添加到Notebook"""
notebook.AddPage(panel_rtgd," Real-time Monitoring ")
notebook.AddPage(panel_flock," Flock Detection ")
# notebook.AddPage(panel_dbad," DBAD识别 ")
# notebook.AddPage(panel_gba," GBA识别 ")
# notebook.AddPage(panel_cc," CC识别 ")



"""显示Frame窗口"""
frame.Show()

# 刷新部分控件，以解决程序刚启动时部分控件的显示Bug
original_tc_size=tc_rtgd_eps.GetSize()
tc_rtgd_eps.SetSize((0,0))
tc_rtgd_minpts.SetSize((0,0))
tc_rtgd_gama.SetSize((0,0))
tc_rtgd_delta.SetSize((0,0))
tc_rtgd_eps.SetSize(original_tc_size)
tc_rtgd_minpts.SetSize(original_tc_size)
tc_rtgd_gama.SetSize(original_tc_size)
tc_rtgd_delta.SetSize(original_tc_size)

app.MainLoop()
