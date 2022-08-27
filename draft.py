
nums = [1,1,2,1]
nums = [1, 4, 2 ,5, 7, 1, 3]
nums = [7, 3, 9, 7, 6, 5, 9, 1, 3, 3]
def myfun(nums, n):
    res = 0
    stack = []
    for i in range(n-1):
        if stack:
            if nums[i]==stack[-1][0]:
                stack[-1][1] += 1
            elif nums[i]>stack[-1][0]:
                stack.append([nums[i], 1])
            else:
                print(stack)
                while stack:
                    node = stack.pop()
                    if node[0]>=nums[i]:
                        res += node[1]
                    if node[1]>=2:
                        res += (node[1]*(node[1]-1))/2
                stack.append([nums[i], 1])
        else:
            stack.append([nums[i], 1])
        

    stack = []
    print(res)
    for i in range(n-1, -1, -1):
        if stack:
            if nums[i]==stack[-1][0]:
                stack[-1][1] += 1
            elif nums[i]>stack[-1][0]:
                stack.append([nums[i], 1])
            else:
                while stack:
                    node = stack.pop()
                    if node[0]>=nums[i]:
                        res += node[1]
                stack.append([nums[i], 1])
        else:
            stack.append([nums[i], 1])
    
    print(res)
    return res

myfun(nums, len(nums))



n = 3
map = [
    list('#.#'),
    list('.**'),
    list('*.#')]
direction = [(1,0),(-1,0),(0,1),(0,-1)]
visited = map.copy()
n_super = 0
for i in range(len(map)):
    for j in range(len(map[0])):
        if visited[i][j] not in set(['.', '#']):
            continue
        n_super += 1
        stack = [(i,j)]
        while stack:
            x, y = stack.pop()
            visited[x][y] = '1'
            for d1, d2 in direction:
                x_new, y_new = x+d1, y+d2
                if 0<=x_new<len(map) and 0<=y_new<len(map[0]) and visited[x_new][y_new] \
                    in set(['.', '#']):
                    stack.append((x_new, y_new))

from enum import EnumMeta
import re
re.findall('/', 'abcdefg')



n, m = 8, 1
s = 'aababaaaabaa'

# dp[i][j]  前i，使用j词转变，最大连续长度
# dp[i][j] = dp[i-1][j] + 1 if s[i-1]==s[i]
# 
n = 2
pi = [1, 2]
cur = 1
catch = {i:0 for i in range(1, n+1)}
cnt = 0
while cur!=n+1:
    catch[cur] += 1
    if catch[cur]%2 == 0:
        cur += 1
    else:
        cur = pi[cur-1]
    cnt += 1
    cnt = cnt % (10e9+7)
print(cnt)





if __name__=="__main__":
    n = int(input())
    s = input()
    s = '010101'

    res = myfun(s)
    print(res[0])


n, m, p = 2, 2, 5
data = ['1 1 1 2',
        '1 2 1 1',
        '1 3 2 2',
        '2 1 1 2',
        '2 3 5 5']
data = [[i]+[int(x) for x in y.split(' ')] for i, y in enumerate(data)]
res = []
process = []  # [id, end_dt]
t = 1
while data or process:
    tmp = []
    for i, task in enumerate(process):
        task = process[i]
        if task[-1] == t:
            res.append([task[0], t])
        else:
            tmp.append(i)
    process_last = []
    for i in tmp:
        process_last.append(process[i])
    process = process_last
    if data:
        # 筛选可选择任务列表
        task_list = [task for task in data if t>=task[2]]
        task_last = [task for task in data if t<task[2]]
        task_list = sorted(task_list, key=lambda x:(x[3], x[-1], x[2]))
        last_m = m - len(process)
        for _ in range(last_m):
            if task_list:
                task = task_list.pop(0)
                process.append([task[0], task[2], t+task[-1]])
        data = task_list + task_last
        print(t, process)
    
     
    t += 1
    if t>100:
        break

res = sorted(res, key=lambda x:x[0])
for i in range(p):
    print(res[i][-1])


n = 10
nums = [81, 87 ,47, 59, 81 ,18, 25 ,40, 56, 0] # 16685
# 单调栈， 找到右边第一个比自己小的数，找到左边第一个比自己小的数
pos_right = [i for i in range(n)]
stack = []
for i in range(n):
    while stack and nums[i]<nums[stack[-1]]:
        pos = stack.pop()
        pos_right[pos] = i-1
    stack.append(i)
while stack:
    pos = stack.pop()
    pos_right[pos] = i
pos_left = [i for i in range(n)]
stack = []
for i in range(n-1, -1, -1):
    while stack and nums[i]<nums[stack[-1]]:
        pos = stack.pop()
        pos_left[pos] = i+1
    stack.append(i)
while stack:
    pos = stack.pop()
    pos_left[pos] = i
res = 0
for i in range(n):
    res = max(res, nums[i] * sum(nums[pos_left[i]:pos_right[i]+1]))


