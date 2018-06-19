#!/usr/bin/env python
# -*- coding:cp936 -*-
import os

import time
import re
import tkFileDialog
import numpy
import Tkinter
import matplotlib.pyplot as plyt


def get_data_dir():
    global data_dir
    data_dir = tkFileDialog.askdirectory().replace('/', '\\')
    var_char_entry_data_dir.set(data_dir)


def get_result_dir():
    global result_dir
    result_dir = tkFileDialog.askdirectory().replace('/', '\\')
    var_char_entry_result_dir.set(result_dir)


def plyt_1jobs(item_filename):
    data_1 = []
    data_2 = []
    #filename_list_handled.append(item_filename)
    datapathname = os.path.join(data_dir, item_filename)
    figure_name = item_filename.split('.')[0]
    file1 = open(datapathname, mode='r')
    for item_data in file1:
        temp = item_data.split(',')[1].strip()
        #temp_time = item_data.split(',')[0].strip()
        data_1.append(temp)
        #data_2.append(temp_time)
    length = len(data_1)
    #j = 0
    for i in range(1, length +1):
        data_2.append(i)
        # j = j + 1
    print len(data_2)
    # find max & min for y stick,set jiange 1/10
    max_y = float(max(data_1))
    min_y = float(min(data_1))
    print "max:%s;min:%s" % (max_y, min_y)
    jiange = (max_y - min_y) / 10
    y_ticks = numpy.arange(min_y, max_y, step=jiange)
    print y_ticks
    data_second = numpy.array(data_2)
    data_data = numpy.array(data_1)
    file1.close()
    figure_1 = plyt.figure(figure_name)
    plyt.title(figure_name)
    plyt.ylim((min_y, max_y))

    plyt.plot(data_second, data_data)
    time.sleep(1)
    figure_1.savefig(os.path.join(result_dir, figure_name))
    plyt.close()
    print "%s done" % figure_name


def plyt_4jobs(item_filename, sub_filename_list_all):
    data_1 = []
    data_2 = []
    datatemp = {}
    filename_list_handle_thistime = []
    figure_name = item_filename.split('.')[0]
    for item in sub_filename_list_all:
        if re.match(figure_name, item):
            filename_list_handle_thistime.append(item)
            filename_list_handled.append(item)
    for index_4jobs, item_4jobs_thistime in enumerate(filename_list_handle_thistime):
        datapathname = os.path.join(data_dir, item_4jobs_thistime)
        file_temp = open(datapathname, mode='r')
        datatemp['%s' % str(index_4jobs)] = []
        for item_data in file_temp:
            datatemp['%s' % str(index_4jobs)].append(item_data.split(',')[1].strip())
        file_temp.close()
    print len(datatemp)
    try:
        for index_subdata, item_subdata in enumerate(datatemp['0']):
            data_1.append(float(datatemp['0'][index_subdata]) + float(datatemp['1'][index_subdata]) + float(datatemp['2'][index_subdata]) + float(datatemp['3'][index_subdata]))
    except IndexError:
        pass
    length = len(data_1)
    for i in range(1, length + 1):
        data_2.append(i)
    data_second = numpy.array(data_2)
    data_data = numpy.array(data_1)
    figure_1 = plyt.figure(figure_name)
    plyt.title(figure_name)
    plyt.plot(data_second, data_data)
    time.sleep(1)
    figure_1.savefig(os.path.join(result_dir, figure_name))
    plyt.close()
    print "%s done" % figure_name


def plyt_32jobs(item_filename, sub_filename_list_all):
    data_1 = []
    data_2 = []
    datatemp = {}
    filename_list_handle_thistime = []
    figure_name = item_filename.split('.')[0]
    for item in sub_filename_list_all:
        if re.match(figure_name, item):
            filename_list_handle_thistime.append(item)
            filename_list_handled.append(item)
    for index_32jobs, item_32jobs_thistime in enumerate(filename_list_handle_thistime):
        datapathname = os.path.join(data_dir, item_32jobs_thistime)
        file_temp = open(datapathname, mode='r')
        datatemp['%s' % str(index_32jobs)] = []
        for item_data in file_temp:
            datatemp['%s' % str(index_32jobs)].append(item_data.split(',')[1].strip())
        file_temp.close()
    print len(datatemp)
    try:
        for index_subdata, item_subdata in enumerate(datatemp['0']):
            data_1.append(float(datatemp['0'][index_subdata]) + float(datatemp['1'][index_subdata]) + float(datatemp['2'][index_subdata])
                + float(datatemp['3'][index_subdata]) + float(datatemp['4'][index_subdata]) + float(datatemp['5'][index_subdata])
                + float(datatemp['6'][index_subdata]) + float(datatemp['7'][index_subdata]) + float(datatemp['8'][index_subdata])
                + float(datatemp['9'][index_subdata]) + float(datatemp['10'][index_subdata]) + float(datatemp['11'][index_subdata])
                + float(datatemp['12'][index_subdata]) + float(datatemp['13'][index_subdata]) + float(datatemp['14'][index_subdata])
                + float(datatemp['15'][index_subdata]) + float(datatemp['16'][index_subdata]) + float(datatemp['17'][index_subdata])
                + float(datatemp['18'][index_subdata]) + float(datatemp['19'][index_subdata]) + float(datatemp['20'][index_subdata])
                + float(datatemp['21'][index_subdata]) + float(datatemp['22'][index_subdata]) + float(datatemp['23'][index_subdata])
                + float(datatemp['24'][index_subdata]) + float(datatemp['25'][index_subdata]) + float(datatemp['26'][index_subdata])
                + float(datatemp['27'][index_subdata]) + float(datatemp['28'][index_subdata]) + float(datatemp['29'][index_subdata])
                + float(datatemp['30'][index_subdata]) + float(datatemp['31'][index_subdata]))
    except IndexError:
        pass
    length = len(data_1)
    for i in range(1, length + 1):
        data_2.append(i)
    data_second = numpy.array(data_2)
    data_data = numpy.array(data_1)
    figure_1 = plyt.figure(figure_name)
    plyt.title(figure_name)
    plyt.plot(data_second, data_data)
    time.sleep(1)
    figure_1.savefig(os.path.join(result_dir, figure_name))
    plyt.close()
    print "%s done" % figure_name

def plot_image():
    filename_done = []
    filename_list=os.listdir(data_dir)
    pattern_find_4job = re.compile(r'_4_')
    pattern_find_32job = re.compile(r'_32_')
    for item_filename in filename_list:
        print item_filename
        if item_filename.split(".")[0] not in filename_done:
            if_4jobs = re.search(pattern_find_4job, item_filename)
            if if_4jobs is not None:
                if item_filename not in filename_list_handled:
                    plyt_4jobs(item_filename, filename_list)
                    filename_done.append(item_filename.split(".")[0])
            else:
                if_32jobs = re.search(pattern_find_32job, item_filename)
                if if_32jobs is not None:
                    #print "fail.not find%s" % item_filename
                    #plot 1job
                    plyt_32jobs(item_filename, filename_list)
                    filename_done.append(item_filename.split(".")[0])
                else:
                    print "Begin %s" % item_filename
                    plyt_1jobs(item_filename)
                    filename_done.append(item_filename)

root = Tkinter.Tk()
root.title("阿里性能测试单盘结果画图工具".decode('gbk'))
root.geometry('800x600')
root.resizable(width=True, height=True)
data_dir = str()
result_dir = str()
var_char_entry_data_dir = Tkinter.StringVar()
var_char_entry_result_dir = Tkinter.StringVar()
filename_list_handled = []

frame_top = Tkinter.Frame(root, height=20)
frame_top.pack(side=Tkinter.TOP)
frame_top_top = Tkinter.Frame(frame_top, height=40)
frame_top_top.pack()
frame_top_bottom = Tkinter.Frame(frame_top, height=20)
frame_top_bottom.pack()
Tkinter.Label(frame_top_top, text='请在如下选择需要处理的包含阿里性能测试结果的目录'.decode('gbk'), bg='Red').pack()
Tkinter.Entry(frame_top_bottom, textvariable=var_char_entry_data_dir, width=40).pack(side=Tkinter.LEFT)
Tkinter.Button(frame_top_bottom, text='选择文件夹'.decode('gbk'), command=get_data_dir, width=20).pack(side=Tkinter.RIGHT)

frame_middle = Tkinter.Frame(root, height=20)
frame_middle.pack()
frame_middle_top = Tkinter.Frame(frame_middle, height=40)
frame_middle_top.pack()
frame_middle_bottom = Tkinter.Frame(frame_middle, height=20)
frame_middle_bottom.pack()
Tkinter.Label(frame_middle_top, text='请在如下选择放置最后生成图片的目录'.decode('gbk'), bg='Red').pack()
Tkinter.Entry(frame_middle_bottom, textvariable=var_char_entry_result_dir, width=40).pack(side=Tkinter.LEFT)
Tkinter.Button(frame_middle_bottom, text='选择文件夹'.decode('gbk'), command=get_result_dir, width=20).pack(side=Tkinter.RIGHT)

frame_button = Tkinter.Frame(root, height=20)
frame_button.pack()

Tkinter.Button(frame_button, text='GO'.decode('gbk'), command=plot_image, width=20,).pack(side=Tkinter.LEFT)
Tkinter.Button(frame_button, text='退出'.decode('gbk'), width=20, command=root.destroy).pack(side=Tkinter.LEFT)

root.mainloop()
