# shadowverse-analyzer-beyond
**S**haderverse analy**Z**er **B**eyond (SZB) is a Shaderverse WB data analyze tool, which helps you to analyze the data of your battle result.

## Get Start
`npm install element-plus axios`

- 后端启动：`cd backend && python main.py`
- 前端启动：`cd frontend && npm run dev`

## TODOS
1. 数据记录
  - 记录每场对局的
    - 己方职业
    - 己方卡组
    - 敌方职业
    - 敌方卡组
    - 先/后手
    - win/lose

2. 数据可视化，用pyecharts绘制，需要：
  最近 20/50/100 场的对局情况，包括
  - 职业分布（饼图）
  - 胜率走势（折线图）