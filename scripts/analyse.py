import json
from collections import defaultdict

# 参数
USER = 'czqmike'   # 这里替换成你要分析的user_identifier
CNM = {'1': '妖', '2': '皇', '3': '法', '4': '龙', 
       '5': '梦', '6': '教', '7': '鱼'}  # Class Name Map 职业编号映射

# 加载数据
with open('D:\Downloads\matches.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 只分析指定用户
user_games = [d for d in data if d.get('user_identifier') == USER]

# 先后手胜率统计
first_total = 0
first_win = 0
second_total = 0
second_win = 0

# 各职业对战胜率
versus_class_total = defaultdict(int)
versus_class_win = defaultdict(int)

for g in user_games:
    is_win = g.get('is_win', False)
    is_first = g.get('is_first', False)
    enemy_class = str(g.get('enemy_class'))

    # 先后手统计
    if is_first:
        first_total += 1
        if is_win:
            first_win += 1
    else:
        second_total += 1
        if is_win:
            second_win += 1

    # 各职业统计
    versus_class_total[enemy_class] += 1
    if is_win:
        versus_class_win[enemy_class] += 1

# 输出先后手胜率
print(f"用户 {USER} 统计：")
if first_total:
    print(f"先手胜率: {first_win}/{first_total} = {first_win/first_total:.2%}")
else:
    print("没有先手对局")

if second_total:
    print(f"后手胜率: {second_win}/{second_total} = {second_win/second_total:.2%}")
else:
    print("没有后手对局")

# 输出各职业胜率
print("\n与各职业对战胜率：")
for cls in sorted(versus_class_total.keys()):
    total = versus_class_total[cls]
    win = versus_class_win[cls]
    print(f"vs {CNM[cls]}: {win}/{total} = {win/total:.2%}")