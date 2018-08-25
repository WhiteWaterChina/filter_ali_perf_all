#!/usr/bin/env python
# -*- coding:cp936 -*-

import re
import xlsxwriter
import tkMessageBox
import Tkinter
import tkFileDialog

filename_seq_result = str()
filename_random_result = str()
filename_mix_result = str()


def get_filename_seq():
    global filename_seq_result
    filename_seq_result = tkFileDialog.askopenfilename()
    var_char_entry_seq_result.set(filename_seq_result)


def get_filename_random():
    global filename_random_result
    filename_random_result = tkFileDialog.askopenfilename()
    var_char_entry_random_result.set(filename_random_result)


def get_filename_mix():
    global filename_mix_result
    filename_mix_result = tkFileDialog.askopenfilename()
    var_char_entry_mix_result.set(filename_mix_result)


def filter_1job(result):
    pattern_bw = re.compile(r'bw=(\d*)(\w*)')
    pattern_latency = re.compile(r'     lat \((\w+)\).*avg=(\d+.\d+)')
    pattern_qos_data = re.compile('99.99th=\[.*?(\d+.\d*)\]')
    pattern_qos_unit = re.compile(r'clat percentiles \((\w+)\)')
    # group(1）是数值，group（2）是单位
    result_bw = re.search(pattern_bw, result)
    # group(1)是单位，group（2）是数值
    result_latency = re.search(pattern_latency, result)
    result_qos_data = re.search(pattern_qos_data, result)
    result_qos_unit = re.search(pattern_qos_unit, result)
    if result_bw.group(2) == 'KB':
        result_bw_display = float(result_bw.group(1)) / 1000
    elif result_bw.group(2) == "GB":
        result_bw_display = float(result_bw.group(1)) * 1000
    else:
        result_bw_display = float(result_bw.group(1))
    if result_latency.group(1) == 'msec':
        result_latency_display = float(result_latency.group(2)) * 1000
    else:
        result_latency_display = float(result_latency.group(2))
    if result_qos_unit == 'msec':
        result_qos_data_display = float(result_qos_data.group(1)) * 1000
    else:
        result_qos_data_display = float(result_qos_data.group(1))

    return result_bw_display, result_latency_display, result_qos_data_display


def filter_4job(result):
    pattern_bw = re.compile(r'bw=(\d*)(\w*)')
    pattern_latency = re.compile(r'     lat \((\w+)\).*avg=\s*(\d+.\d+)')
    pattern_qos_data = re.compile('99.99th=\[.*?(\d+.\d*)\]')
    pattern_qos_unit = re.compile(r'clat percentiles \((\w+)\)')

    result_bw_list = re.findall(pattern_bw, result)
    # group(1)是单位，group（2）是数值
    result_latency_list = re.findall(pattern_latency, result)
    result_qos_data_list = re.findall(pattern_qos_data, result)
    result_qos_unit_list = re.findall(pattern_qos_unit, result)
    result_bw_display = float()
    result_latency_display = float()
    result_qos_data_display = float()
    for index_bw_sub, item_bw_sub in enumerate(result_bw_list):
        if item_bw_sub[1] == 'KB':
            temp_bw = float(item_bw_sub[0]) / 1000
        elif item_bw_sub[1] == 'GB':
            temp_bw = float(item_bw_sub[0]) * 1000
        else:
            temp_bw = float(item_bw_sub[0])
        result_bw_display += temp_bw
    for index_latency_sub, item_latency_sub in enumerate(result_latency_list):
        if item_latency_sub[0] == 'msec':
            temp_latency = float(item_latency_sub[1]) * 1000
        else:
            temp_latency = float(item_latency_sub[1])
        result_latency_display += temp_latency
    result_latency_display /= 4
    for index_qos_sub, item_qos_sub in enumerate(result_qos_unit_list):
        if item_qos_sub == 'msec':
            temp_qos_data = float(result_qos_data_list[index_qos_sub]) * 1000
        else:
            temp_qos_data = float(result_qos_data_list[index_qos_sub])
        result_qos_data_display += temp_qos_data
    result_qos_data_display /= 4
    return result_bw_display, result_latency_display, result_qos_data_display


def filter_1job_random(result):
    pattern_iops = re.compile(r'iops=(\d*)')
    pattern_latency = re.compile(r'     lat \((\w+)\).*avg=\s*(\d+.\d+)')
    pattern_qos_data = re.compile('99.99th=\[.*?(\d+.\d*)\]')
    pattern_qos_unit = re.compile(r'clat percentiles \((\w+)\)')
    # group(1）是数值
    result_iops = re.search(pattern_iops, result)
    # group(1)是单位，group（2）是数值
    result_latency = re.search(pattern_latency, result)
    result_qos_data = re.search(pattern_qos_data, result)
    result_qos_unit = re.search(pattern_qos_unit, result)
    result_iops_display = float(result_iops.group(1))
    if result_latency.group(1) == 'msec':
        result_latency_display = float(result_latency.group(2)) * 1000
    else:
        result_latency_display = float(result_latency.group(2))
    if result_qos_unit == 'msec':
        result_qos_data_display = float(result_qos_data.group(1)) * 1000
    else:
        result_qos_data_display = float(result_qos_data.group(1))
    return result_iops_display, result_latency_display, result_qos_data_display


def filter_4job_random(result):
    pattern_iops = re.compile(r'iops=(\d*)')
    pattern_latency = re.compile(r'     lat \((\w+)\).*avg=(\d+.\d+)')
    pattern_qos_data = re.compile('99.99th=\[.*?(\d+.\d*)\]')
    pattern_qos_unit = re.compile(r'clat percentiles \((\w+)\)')

    result_iops_list = re.findall(pattern_iops, result)
    # group(1)是单位，group（2）是数值
    result_latency_list = re.findall(pattern_latency, result)
    result_qos_data_list = re.findall(pattern_qos_data, result)
    result_qos_unit_list = re.findall(pattern_qos_unit, result)
    result_iops_display = float()
    result_latency_display = float()
    result_qos_data_display = float()
    for index_iops_sub, item_iops_sub in enumerate(result_iops_list):
        result_iops_display += float(item_iops_sub)
    result_iops_display /= 4
    for index_latency_sub, item_latency_sub in enumerate(result_latency_list):
        if item_latency_sub[0] == 'msec':
            temp_latency = float(item_latency_sub[1]) * 1000
        else:
            temp_latency = float(item_latency_sub[1])
        result_latency_display += temp_latency
    result_latency_display /= 4
    for index_qos_sub, item_qos_sub in enumerate(result_qos_unit_list):
        if item_qos_sub == 'msec':
            temp_qos_data = float(result_qos_data_list[index_qos_sub]) * 1000
        else:
            temp_qos_data = float(result_qos_data_list[index_qos_sub])
        result_qos_data_display += temp_qos_data
    result_qos_data_display /= 4
    return result_iops_display, result_latency_display, result_qos_data_display


def filter_1job_mix(result):
    pattern_iops = re.compile(r'iops=(\d*)')
    pattern_latency = re.compile(r'     lat \((\w+)\).*avg=\s*(\d+.\d+)')
    pattern_qos_data = re.compile('99.99th=\[\s*(\d+.\d*)\]')
    pattern_qos_unit = re.compile(r'clat percentiles \((\w+)\)')
    result_iops = re.findall(pattern_iops, result)
    result_latency = re.findall(pattern_latency, result)
    result_qos_data = re.findall(pattern_qos_data, result)
    result_qos_unit = re.findall(pattern_qos_unit, result)
    result_iops_read = str(result_iops[0])
    result_iops_write = str(result_iops[1])
    result_latency_unit_read = result_latency[0][0]
    result_latency_data_read = result_latency[0][1]
    result_latency_unit_write = result_latency[1][0]
    result_latency_data_write = result_latency[1][1]
    result_qos_unit_read = result_qos_unit[0]
    result_qos_unit_write = result_qos_unit[1]
    result_qos_data_read = result_qos_data[0]
    result_qos_data_write = result_qos_data[1]
    result_iops_display = str(result_iops_read) + '/' + str(result_iops_write)
    if result_latency_unit_read == 'msec':
        result_latency_data_read = float(result_latency_data_read) * 1000
    if result_latency_unit_write == 'msec':
        result_latency_data_write = float(result_latency_data_write) * 1000
    result_latency_display = str(result_latency_data_read) + '/' + str(result_latency_data_write)
    if result_qos_unit_read == 'msec':
        result_qos_data_read = float(result_qos_data_read) * 1000
    if result_qos_unit_write == 'msec':
        result_qos_data_write = float(result_qos_data_write) * 1000
    result_qos_data_display = str(result_qos_data_read) + '/' + str(result_qos_data_write)
    return result_iops_display, result_latency_display, result_qos_data_display


def filter_4job_mix(result):
    pattern_iops = re.compile(r'iops=(\d*)')
    pattern_latency = re.compile(r'     lat \((\w+)\).*avg=(\d+.\d+)')
    pattern_qos_data = re.compile('99.99th=\[.*?(\d+.\d*)\]')
    pattern_qos_unit = re.compile(r'clat percentiles \((\w+)\)')

    result_iops_list = re.findall(pattern_iops, result)
    result_latency_list = re.findall(pattern_latency, result)
    result_qos_data_list = re.findall(pattern_qos_data, result)
    result_qos_unit_list = re.findall(pattern_qos_unit, result)
    result_iops_mix_read_temp = float()
    result_iops_mix_write_temp = float()
    result_latency_mix_read_temp = float()
    result_latency_mix_write_temp = float()
    result_qos_mix_read_temp = float()
    result_qos_mix_write_temp = float()
    for index_iops_sub, item_iops_sub in enumerate(result_iops_list):
        if index_iops_sub % 2 == 0:
            result_iops_mix_read_temp += float(item_iops_sub)
        else:
            result_iops_mix_write_temp += float(item_iops_sub)
    result_iops_mix_read_temp /= 4
    result_iops_mix_write_temp /= 4
    result_iops_display = str(result_iops_mix_read_temp) + '/' + str(result_iops_mix_write_temp)

    for index_latency_sub, item_latency_sub in enumerate(result_latency_list):
        if item_latency_sub[0] == 'msec':
            temp_latency = float(item_latency_sub[1]) * 1000
        else:
            temp_latency = float(item_latency_sub[1])
        if index_latency_sub % 2 == 0:
            result_latency_mix_read_temp += temp_latency
        else:
            result_latency_mix_write_temp += temp_latency
    result_latency_mix_read_temp /= 4
    result_latency_mix_write_temp /= 4
    result_latency_display = str(result_latency_mix_read_temp) + '/' + str(result_latency_mix_write_temp)

    for index_qos_sub, item_qos_sub in enumerate(result_qos_unit_list):
        if item_qos_sub == 'msec':
            temp_qos_data = float(result_qos_data_list[index_qos_sub]) * 1000
        else:
            temp_qos_data = float(result_qos_data_list[index_qos_sub])
        if index_qos_sub % 2 == 0:
            result_qos_mix_read_temp += temp_qos_data
        else:
            result_qos_mix_write_temp += temp_qos_data
    result_qos_mix_read_temp /= 4
    result_qos_mix_write_temp /= 4
    result_qos_data_display = str(result_qos_mix_read_temp) + '/' + str(result_qos_mix_write_temp)
    return result_iops_display, result_latency_display, result_qos_data_display


def get_data():
    work_book = xlsxwriter.Workbook("阿里单盘性能数据.xlsx".decode('gbk'))
    sheet_now = work_book.add_worksheet("单盘读写性能数据".decode('gbk'))
    format_one = work_book.add_format()
    format_one.set_border(1)
    pattern_find_4job = re.compile(r'.*(4job)')

    if len(var_char_entry_seq_result.get()) != 0:
        all_file_text_seq = open(filename_seq_result, mode='r').read()
        blockListSeq = ['128kB', '64kB', '32kB', '16kB', '8kB', '4kB']
        rwList = ['WR', 'RD']
        qdListSeq = ['1', '2', '4', '8', '16', '32']
        policyListJob = []

        policyListBW = ['512kB Seq WR 1job QD32:', '512kB Seq RD 1job QD32:']
        for block in blockListSeq:
            for rw in rwList:
                # policy4job = block + ' Seq' + ' ' + rw + ' 4job' + ' QD32:'
                for qd in qdListSeq:
                    policy1job = block + ' Seq' + ' ' + rw + ' 1job' + ' QD' + qd + ':'
                    policyListJob.append(policy1job)
                # policyListJob.append(policy4job)
        data_bw = []
        data_latency = []
        data_qos = []
        data_512k_bw_list = []
        for index_policy, item_policy in enumerate(policyListJob):
            if_4jobs = re.search(pattern_find_4job, item_policy)
            if item_policy != '4kB Seq RD 4job QD32:':
                if index_policy != len(policyListJob) - 1:
                    temp_text = re.findall(r'\b%s \(groupid=(.*?)%s' % (policyListJob[index_policy], policyListJob[index_policy + 1]), all_file_text_seq, re.S)[0]
                else:
                    temp_text = re.findall(r'\b%s \(groupid=(.*)' % (policyListJob[index_policy]), all_file_text_seq, re.S)[0]
            else:
                temp_text = re.findall(r'\b%s \(groupid=(.*)' % (policyListJob[index_policy]), all_file_text_seq, re.S)[0]
            if if_4jobs is None:
                bw, latency, qos_data = filter_1job(temp_text)
            else:
                bw, latency, qos_data = filter_4job(temp_text)
            data_bw.append(bw)
            data_latency.append(latency)
            data_qos.append(qos_data)
        for index_512k_bw, item_512k_bw in enumerate(policyListBW):
            if item_512k_bw == '512kB Seq WR 1job QD32:':
                temp_text = re.findall(r'\b%s \(groupid=(.*?)%s' % (policyListBW[index_512k_bw], policyListBW[index_512k_bw + 1]), all_file_text_seq, re.S)[0]
            else:
                temp_text = re.findall(r'\b%s \(groupid=(.*)' % (policyListBW[index_512k_bw]), all_file_text_seq, re.S)[0]
            bw, latency, qos_data = filter_1job(temp_text)
            data_512k_bw_list.append(bw)
        if len(blockListSeq) % 2 == 0:
            para_seq_line = len(blockListSeq)
        else:
            para_seq_line = len(blockListSeq) + 1
        for index_bw, item_bw in enumerate(data_bw):
            shang = index_bw / (len(qdListSeq) * len(rwList))
            yushu = index_bw % len(qdListSeq)
            column = 1 + yushu
            if (index_bw / para_seq_line) % 2 == 0:
                line = 10 + 8 * shang
            else:
                line = 6 + 8 * shang
            sheet_now.write(line, column, item_bw, format_one)
        for index_latency, item_latency in enumerate(data_latency):
            shang = index_latency / (len(qdListSeq) * len(rwList))
            yushu = index_latency % len(qdListSeq)
            column = 1 + yushu
            if (index_latency / para_seq_line) % 2 == 0:
                line = 11 + 8 * shang
            else:
                line = 7 + 8 * shang
            sheet_now.write(line, column, item_latency, format_one)
        for index_qos, item_qos in enumerate(data_qos):
            shang = index_qos / (len(qdListSeq) * len(rwList))
            yushu = index_qos % len(qdListSeq)
            column = 1 + yushu
            if (index_qos / para_seq_line) % 2 == 0:
                line = 12 + 8 * shang
            else:
                line = 8 + 8 * shang
            sheet_now.write(line, column, item_qos, format_one)
        sheet_now.write(2, 1, data_512k_bw_list[1], format_one)
        sheet_now.write(3, 1, data_512k_bw_list[0], format_one)

    if len(var_char_entry_random_result.get()) != 0:
        all_file_text_random = open(filename_random_result, mode='r').read()
        blockListRandom = ['4kB', '8kB', '16kB', '32kB', '1024kB']
        rwList = ['WR', 'RD']
        qdListRandom = ['1', '2', '4', '8', '16', '32']
        policyListJobRandom = []
        for block in blockListRandom:
            for rw in rwList:
                # policy4job = block + ' Ran' + ' ' + rw + ' 4job' + ' QD32:'
                for qd in qdListRandom:
                    policy1job = block + ' Ran' + ' ' + rw + ' 1job' + ' QD' + qd + ':'
                    policyListJobRandom.append(policy1job)
                # policyListJobRandom.append(policy4job)
        data_iops_random = []
        data_latency_random = []
        data_qos_random = []
        for index_policy_random, item_policy_random in enumerate(policyListJobRandom):
            if_4jobs = re.search(pattern_find_4job, item_policy_random)
            if item_policy_random != '32kB Ran RD 4job QD32:':
                if index_policy_random != len(policyListJobRandom) - 1:
                    temp_text = re.findall(r'\b%s \(groupid=(.*?)%s' % (policyListJobRandom[index_policy_random], policyListJobRandom[index_policy_random + 1]), all_file_text_random, re.S)[0]
                else:
                    temp_text = re.findall(r'\b%s \(groupid=(.*)' % (policyListJobRandom[index_policy_random]), all_file_text_random, re.S)[0]
            else:
                temp_text = re.findall(r'\b%s \(groupid=(.*)' % (policyListJobRandom[index_policy_random]), all_file_text_random, re.S)[0]
            if if_4jobs is None:
                iops, latency, qos_data = filter_1job_random(temp_text)
            else:
                iops, latency, qos_data = filter_4job_random(temp_text)
            data_iops_random.append(iops)
            data_latency_random.append(latency)
            data_qos_random.append(qos_data)
        if len(blockListRandom) % 2 == 0:
            para_random_line = len(blockListRandom)
        else:
            para_random_line = len(blockListRandom) + 1
        for index_iops_random, item_iops_random in enumerate(data_iops_random):
            shang_random = index_iops_random / (len(qdListRandom) * len(rwList))
            yushu_random = index_iops_random % len(qdListRandom)
            column_random = 1 + yushu_random
            if (index_iops_random / para_random_line ) % 2 == 0:
                line_random = 58 + 8 * shang_random
            else:
                line_random = 54 + 8 * shang_random
            sheet_now.write(line_random, column_random, item_iops_random, format_one)
        for index_latency_random, item_latency_random in enumerate(data_latency_random):
            shang = index_latency_random / (len(qdListRandom) * len(rwList))
            yushu = index_latency_random % len(qdListRandom)
            column = 1 + yushu
            if (index_latency_random / para_random_line) % 2 == 0:
                line = 59 + 8 * shang
            else:
                line = 55 + 8 * shang
            sheet_now.write(line, column, item_latency_random, format_one)
        for index_qos_random, item_qos_random in enumerate(data_qos_random):
            shang = index_qos_random / (len(qdListRandom) * len(rwList))
            yushu = index_qos_random % len(qdListRandom)
            column = 1 + yushu
            if (index_qos_random / para_random_line) % 2 == 0:
                line = 60 + 8 * shang
            else:
                line = 56 + 8 * shang
            sheet_now.write(line, column, item_qos_random, format_one)

    if len(var_char_entry_mix_result.get()) != 0:
        all_file_text_mix = open(filename_mix_result, mode='r').read()
        policyListJobmix = []
        blockListmix = ['4kB', '8kB', '16kB', '32kB']
        qdListmix = ['1', '2', '4', '8', '16', '32']
        for block in blockListmix:
            # policy4job = "%s mix 7/3 4job QD32:" % block
            for qd in qdListmix:
                policy1job = "%s mix 7/3 1job QD%s:" % (block, qd)
                policyListJobmix.append(policy1job)
            # policyListJobmix.append(policy4job)
        data_iops_mix = []
        data_latency_mix = []
        data_qos_mix = []
        for index_policy_mix, item_policy_mix_sub in enumerate(policyListJobmix):
            item_policy_mix = item_policy_mix_sub
            if_4jobs = re.search(pattern_find_4job, item_policy_mix)
            if item_policy_mix != '32kB mix 7/3 4job QD32:':
                if index_policy_mix != len(policyListJobmix) - 1:
                    temp_text = re.findall(r'\b%s\s\(groupid=(.*?)%s' % (item_policy_mix, policyListJobmix[index_policy_mix + 1]), all_file_text_mix, re.S)[0]
                else:
                    temp_text =re.findall(r'\b%s\s\(groupid=(.*)' % (policyListJobmix[index_policy_mix]), all_file_text_mix, re.S)[0]
            else:
                temp_text = re.findall(r'\b%s\s\(groupid=(.*)' % (policyListJobmix[index_policy_mix]), all_file_text_mix, re.S)[0]

            if if_4jobs is None:
                iops, latency, qos_data = filter_1job_mix(temp_text)
            else:
                iops, latency, qos_data = filter_4job_mix(temp_text)
            data_iops_mix.append(iops)
            data_latency_mix.append(latency)
            data_qos_mix.append(qos_data)
        for index_iops_mix, item_iops_mix in enumerate(data_iops_mix):
            shang = index_iops_mix / len(qdListmix)
            yushu = index_iops_mix % len(qdListmix)
            column = 1 + yushu
            line = 94 + 4 * shang
            sheet_now.write(line, column, item_iops_mix, format_one)
        for index_latency_mix, item_latency_mix in enumerate(data_latency_mix):
            shang = index_latency_mix / len(qdListmix)
            yushu = index_latency_mix % len(qdListmix)
            column = 1 + yushu
            line = 95 + 4 * shang
            sheet_now.write(line, column, item_latency_mix, format_one)
        for index_qos_mix, item_qos_mix in enumerate(data_qos_mix):
            shang = index_qos_mix / len(qdListmix)
            yushu = index_qos_mix % len(qdListmix)
            column = 1 + yushu
            line = 96 + 4 * shang
            sheet_now.write(line, column, item_qos_mix, format_one)

    tkMessageBox.showinfo("完成".decode('gbk'), "生成的结果在《阿里单盘性能数据.xlsx》中，请自行查看！".decode('gbk'))
    work_book.close()


root = Tkinter.Tk()
root.title("阿里性能测试单盘".decode('gbk'))
root.geometry('800x600')
root.resizable(width=True, height=True)
var_char_entry_seq_result = Tkinter.StringVar()
var_char_entry_random_result = Tkinter.StringVar()
var_char_entry_mix_result = Tkinter.StringVar()

frame_top = Tkinter.Frame(root, height=20)
frame_top.pack(side=Tkinter.TOP)
frame_top_top = Tkinter.Frame(frame_top, height=40)
frame_top_top.pack()
frame_top_bottom = Tkinter.Frame(frame_top, height=20)
frame_top_bottom.pack()
Tkinter.Label(frame_top_top, text='请在如下选择需要处理的阿里单盘性能测试顺序读写的结果文件(Seq)'.decode('gbk'), bg='Red').pack()
Tkinter.Entry(frame_top_bottom, textvariable=var_char_entry_seq_result, width=40).pack(side=Tkinter.LEFT)
Tkinter.Button(frame_top_bottom, text='选择文件'.decode('gbk'), command=get_filename_seq, width=20).pack(side=Tkinter.RIGHT)

frame_middle = Tkinter.Frame(root, height=20)
frame_middle.pack()
frame_middle_top = Tkinter.Frame(frame_middle, height=40)
frame_middle_top.pack()
frame_middle_bottom = Tkinter.Frame(frame_middle, height=20)
frame_middle_bottom.pack()
Tkinter.Label(frame_middle_top, text='请在如下选择需要处理的阿里单盘性能测试随机读写的结果文件(Random)'.decode('gbk'), bg='Red').pack()
Tkinter.Entry(frame_middle_bottom, textvariable=var_char_entry_random_result, width=40).pack(side=Tkinter.LEFT)
Tkinter.Button(frame_middle_bottom, text='选择文件'.decode('gbk'), command=get_filename_random, width=20).pack(side=Tkinter.RIGHT)

frame_bottom = Tkinter.Frame(root, height=20)
frame_bottom.pack()
frame_bottom_top = Tkinter.Frame(frame_bottom, height=40)
frame_bottom_top.pack()
frame_bottom_bottom = Tkinter.Frame(frame_bottom, height=20)
frame_bottom_bottom.pack()
Tkinter.Label(frame_bottom_top, text='请在如下选择需要处理的阿里单盘性能测试混合读写的结果文件(Mix)'.decode('gbk'), bg='Red').pack()
Tkinter.Entry(frame_bottom_bottom, textvariable=var_char_entry_mix_result, width=40).pack(side=Tkinter.LEFT)
Tkinter.Button(frame_bottom_bottom, text='选择文件'.decode('gbk'), command=get_filename_mix, width=20).pack(side=Tkinter.RIGHT)

frame_button = Tkinter.Frame(root, height=20)
frame_button.pack()

Tkinter.Button(frame_button, text='GO'.decode('gbk'), command=get_data, width=20,).pack(side=Tkinter.LEFT)
Tkinter.Button(frame_button, text='退出'.decode('gbk'), width=20, command=root.destroy).pack(side=Tkinter.LEFT)
Tkinter.mainloop()
