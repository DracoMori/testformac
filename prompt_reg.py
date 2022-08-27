import pandas as pd
import re

data = pd.read_excel('./回单模板_1.xlsx')
data = data.fillna('') # 把缺失数据替换成 ‘’ ，反正读取出 nan，使得无法进行正则匹配

def regnize(vocab, text):
    '''
    vocab: 模版词组
    text: 待匹配文本
    '''
    vocab = [x for x in vocab.split('\\t') if x != ''] # 将词组拆分成一个一个
    count = 0  # 计数，当识别出在 text中时，+1
    for w in vocab:
        w = w.replace('**', '\d+')  # 把 '**年**月**日' 转换成 正则表达式
        w = w.replace('*', '')
        if re.findall(w, text):
            count += 1
        # 如果是日期类型 且 年月日未匹配成功，则匹配 月日
        if w == '\d+年\d+月\d+日' and not re.findall(w, text):
            w = '\d+月\d+日'
            if re.findall(w, text):
                count += 1
    # 返回出现占比，作为相似度
    return count / len(vocab)

for i in range(data.shape[0]):
    vocab = data.loc[i, '词组']
    text = data.loc[i, '实际回单内容']
    sim = regnize(vocab, text) # 计算相似度
    data.loc[i, '相似度'] = round(sim, 2)

data.to_excel('./回单模板相似度.xlsx')

# text1 = '2022年2月14日经榜头供电所工作人员董益和、余俭核实，户号7568989541仙游县榜头镇华明佛珠厂，现场检查该户表计010123035303接线正确无异常，实际表计反向有功电量为0，无反向走字。经查询采集系统和表计档案信息分析，该户表计为杭州西力电能表制造有限公司2014年批次09版电能表，该批次电能表运行时间较久后，部分表计会出现数据突变异常，如出现反向电量，导致传送采集系统也出现反向电量，实际现场表计并无反向走字。经用户同意后现场予以更换表计（工单编号:220214210901），现已无异常。'
# text2 = '2月14日经榜头供电所工作人员董益和、余俭核实，户号7568989541仙游县榜头镇华明佛珠厂，现场检查该户表计010123035303接线正确无异常，实际表计反向有功电量为0，无反向走字。经查询采集系统和表计档案信息分析，该户表计为杭州西力电能表制造有限公司2014年批次09版电能表，该批次电能表运行时间较久后，部分表计会出现数据突变异常，如出现反向电量，导致传送采集系统也出现反向电量，实际现场表计并无反向走字。经用户同意后现场予以更换表计（工单编号:220214210901），现已无异常。'
# regnize(vocab, text1)
# regnize(vocab, text2)

