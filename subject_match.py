import pandas as pd
import re

# 数据读取，sheet_name是表的名字
data = pd.read_excel('./监控分析清单.xlsx', sheet_name='8月分析抽检清单')
subject_list = pd.read_excel('./监控分析清单.xlsx', sheet_name='模板')

# 为data构建一个索引列(1-n, n为样本量)，用于后续恢复顺序
data['id'] = list(range(data.shape[0]))

# 缺失值填充为空字符
subject_list = subject_list.fillna('')

# 把主题对应的主题词转化为字典的形式，方面后面查找
subject2words = dict()
for i in range(subject_list.shape[0]):
    sub = subject_list['稽查主题'].iloc[i]
    words = subject_list['词组'].iloc[i]
    subject2words[sub] = words



# 统计每个主题的样本量
subject2cnt = data['主题'].value_counts()

def regnize(vocab, text):
    '''
    vocab: 模版词组
    text: 分析描述
    '''
    vocab = [x for x in vocab.split('\\t') if x != ''] # 将词组拆分成一个一个
    flag = False # 纪录是否匹配成功
    for w in vocab:
        w = w.replace('**', '\d+')  # 把 '**年**月**日' 转换成 正则表达式
        w = w.replace('*', '')
        if re.findall(w, text):
            flag = True
            break
        # 如果是日期类型 且 年月日未匹配成功，则匹配 月日
        if w == '\d+年\d+月\d+日' and not re.findall(w, text):
            w = '\d+月\d+日'
            if re.findall(w, text):
                flag = True
                break
    # 匹配到则返回通过，否则置空
    if flag:
        return '通过'
    else:
        return None



# 构建一个 结构和 data 一样的 dataframe，用来存放结果
data_match = pd.DataFrame(columns=data.columns.to_list())

# 按 主题 分组 进行匹配
for i, df in data.groupby('主题'):
    # 查看该主题的样本量，若 > 50，则进行50%抽样. 
    if subject2cnt[i] > 50:
        df = df.sample(int(subject2cnt[i]*0.5)) # 抽样，条数=该主题样本量 * 0.5 取整数
    #提取主题词
    vocab = subject2words[i]
    # 对 取到 的 该主题的 '分析描述' 进行组图匹配
    for j in range(df.shape[0]):
        text = df['分析描述'].iloc[j]
        df['核查结果'].iloc[j] = regnize(vocab, text)  # 匹配并记录结果
    
    # 把 df(匹配完成) 存储到 data_match 中
    data_match = pd.concat((data_match, df), axis=0)

# 对 data_match 的 id 列进行排序，用于恢复顺序
data_match = data_match.sort_values('id', ascending=True)
data_match = data_match.drop(['id'], axis=1) # 删除 id 列
data_match.to_excel('./8月分析抽检清单稽查结果.xlsx') # 保存结果


# 查看 核查结果
# data_match[data_match['主题'] == '反向有功异常走字']['核查结果'].value_counts()
# data_match['核查结果'].value_counts()

