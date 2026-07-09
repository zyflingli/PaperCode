# ARAS 数据格式分析

## 分析范围

读取并分析的 ARAS 数据目录为：

`/home/zyflingli/PaperCode/CPS40/2. ARAS datasets`

本文档只基于该目录中的真实文件内容、`README` 文本、样例行和全量字段检查结果整理，不假设未出现的格式。

## 目录结构

```text
CPS40/2. ARAS datasets/
├── ARAS.py
├── data_highest.py
├── data_modeling.py
├── data_transformation.py
├── data_visualization.py
├── kmean.py
├── mergefiles.py
├── House A/
│   ├── README
│   ├── DAY_1.txt ... DAY_30.txt
│   ├── processed_ARAS_R1.txt
│   └── processed_ARAS_R2.txt
└── House B/
    ├── README
    ├── DAY_1.txt ... DAY_30.txt
    ├── processed_ARAS_R1.txt
    └── processed_ARAS_R2.txt
```

## 文件角色

| 文件 | 角色 | 说明 |
|---|---|---|
| `House A/README` | 传感器定义文件；活动标签定义文件 | 定义 House A 的 20 个传感器列，以及活动 ID 到活动名称的映射。 |
| `House B/README` | 传感器定义文件；活动标签定义文件 | 定义 House B 的 20 个传感器列，以及活动 ID 到活动名称的映射。 |
| `House A/DAY_1.txt` 到 `DAY_30.txt` | 时间序列数据文件 | House A 的 30 天秒级数据。每个文件 86400 行，每行 22 列。 |
| `House B/DAY_1.txt` 到 `DAY_30.txt` | 时间序列数据文件 | House B 的 30 天秒级数据。每个文件 86400 行，每行 22 列。 |
| `processed_ARAS_R1.txt` / `processed_ARAS_R2.txt` | 派生统计文件 | 不是原始标签定义文件。内容为按活动聚合后的统计字段。 |

目录中没有单独的原始活动标签文件。活动标签字典写在每个 house 的 `README` 中；每秒的活动标签直接存放在 `DAY_*.txt` 的第 21、22 列。

## 原始时间序列文件格式

适用文件：

```text
House A/DAY_1.txt ... House A/DAY_30.txt
House B/DAY_1.txt ... House B/DAY_30.txt
```

真实检查结果：

| 属性 | 结果 |
|---|---|
| 文件格式 | 纯文本 |
| 分隔符 | 空格 |
| 表头 | 无表头 |
| 行数 | 每个 `DAY_*.txt` 均为 86400 行 |
| 时间粒度 | 1 秒 |
| 时间范围 | 每天从 `00:00:00` 到 `23:59:59` |
| 列数 | 每行 22 列 |
| 第 1-20 列 | 传感器值 |
| 第 21 列 | Resident 1 活动标签 ID |
| 第 22 列 | Resident 2 活动标签 ID |
| 传感器取值 | 全量检查中第 1-20 列最小值为 0、最大值为 1 |
| 活动标签取值 | 全量检查中第 21-22 列最小值为 1、最大值为 27 |

行索引和时间的关系：

| 文件行号 | 秒偏移 | 时间 |
|---:|---:|---|
| 1 | 0 | `00:00:00` |
| 2 | 1 | `00:00:01` |
| ... | ... | ... |
| 86400 | 86399 | `23:59:59` |

因此加载时可用 `day` + `line_number - 1` 恢复一天内的秒级时间。

## House A 传感器字段

来源：`House A/README`。以下顺序就是 `House A/DAY_*.txt` 的第 1-20 列顺序。

| 列号 | 字段名 | 传感器类型 | 位置 |
|---:|---|---|---|
| 1 | `Ph1` | Photocell | Wardrobe |
| 2 | `Ph2` | Photocell | Convertible Couch, used as bed for Resident 2 |
| 3 | `Ir1` | IR | TV receiver |
| 4 | `Fo1` | Force Sensor | Couch |
| 5 | `Fo2` | Force Sensor | Couch |
| 6 | `Di3` | Distance | Chair |
| 7 | `Di4` | Distance | Chair |
| 8 | `Ph3` | Photocell | Fridge |
| 9 | `Ph4` | Photocell | Kitchen Drawer |
| 10 | `Ph5` | Photocell | Wardrobe |
| 11 | `Ph6` | Photocell | Bathroom Cabinet |
| 12 | `Co1` | Contact Sensor | House Door |
| 13 | `Co2` | Contact Sensor | Bathroom Door |
| 14 | `Co3` | Contact Sensor | Shower Cabinet Door |
| 15 | `So1` | Sonar Distance | Hall |
| 16 | `So2` | Sonar Distance | Kitchen |
| 17 | `Di1` | Distance | Tap |
| 18 | `Di2` | Distance | Water Closet |
| 19 | `Te1` | Temperature | Kitchen |
| 20 | `Fo3` | Force Sensor | Bed |
| 21 | `R1` | Activity label | Resident 1 |
| 22 | `R2` | Activity label | Resident 2 |

House A 样例，`DAY_1.txt` 前 8 行：

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 12 17
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 12 17
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 12 17
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 12 17
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 12 17
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 12 17
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 12 17
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 12 17
```

House A 样例，`DAY_1.txt` 第 11 行，第 15 列 `So1` 为 1：

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 12 17
```

House A 样例，`DAY_1.txt` 最后 3 行：

```text
0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 12 12
0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 12 12
0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 12 12
```

## House B 传感器字段

来源：`House B/README`。以下顺序就是 `House B/DAY_*.txt` 的第 1-20 列顺序。

| 列号 | 字段名 | 传感器类型 | 位置 |
|---:|---|---|---|
| 1 | `co1` | Contact Sensor | Kitchen cupboard |
| 2 | `co2` | Contact Sensor | Kitchen cupboard |
| 3 | `co3` | Contact Sensor | House Door |
| 4 | `co4` | Contact Sensor | Wardrobe Door |
| 5 | `co5` | Contact Sensor | Wardrobe Door |
| 6 | `co6` | Contact Sensor | Shower Cabinet Door |
| 7 | `di2` | Distance | Tap |
| 8 | `fo1` | Force Sensor | Chair |
| 9 | `fo2` | Force Sensor | Chair |
| 10 | `fo3` | Force Sensor | Chair |
| 11 | `ph1` | Photocell | Fridge |
| 12 | `ph2` | Photocell | Kitchen Drawer |
| 13 | `pr1` | Pressure Mat | Couch |
| 14 | `pr2` | Pressure Mat | Couch |
| 15 | `pr3` | Pressure Mat | Bed |
| 16 | `pr4` | Pressure Mat | Bed |
| 17 | `pr5` | Pressure Mat | Armchair |
| 18 | `so1` | Sonar Distance | Bathroom Door |
| 19 | `so2` | Sonar Distance | Kitchen |
| 20 | `so3` | Sonar Distance | Closet |
| 21 | `R1` | Activity label | Resident 1 |
| 22 | `R2` | Activity label | Resident 2 |

House B 样例，`DAY_1.txt` 前 8 行：

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 11 11
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 11 11
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 11 11
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 11 11
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 11 11
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 11 11
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 11 11
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 11 11
```

House B 样例，`DAY_1.txt` 最后 3 行：

```text
0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 12 12
0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 12 12
0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 12 12
```

## 活动标签字段

来源：`House A/README` 和 `House B/README`。两个 house 的活动 ID 映射一致。

| ID | 活动 |
|---:|---|
| 1 | Other |
| 2 | Going Out |
| 3 | Preparing Breakfast |
| 4 | Having Breakfast |
| 5 | Preparing Lunch |
| 6 | Having Lunch |
| 7 | Preparing Dinner |
| 8 | Having Dinner |
| 9 | Washing Dishes |
| 10 | Having Snack |
| 11 | Sleeping |
| 12 | Watching TV |
| 13 | Studying |
| 14 | Having Shower |
| 15 | Toileting |
| 16 | Napping |
| 17 | Using Internet |
| 18 | Reading Book |
| 19 | Laundry |
| 20 | Shaving |
| 21 | Brushing Teeth |
| 22 | Talking on the Phone |
| 23 | Listening to Music |
| 24 | Cleaning |
| 25 | Having Conversation |
| 26 | Having Guest |
| 27 | Changing Clothes |

全量数据中实际出现的活动 ID：

| House | Resident | 实际出现的 ID |
|---|---|---|
| A | R1 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27 |
| A | R2 | 1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 27 |
| B | R1 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 21, 22, 23, 24, 25, 27 |
| B | R2 | 1, 2, 3, 4, 6, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 25, 27 |

## 派生统计文件格式

适用文件：

```text
House A/processed_ARAS_R1.txt
House A/processed_ARAS_R2.txt
House B/processed_ARAS_R1.txt
House B/processed_ARAS_R2.txt
```

这些文件不是原始 ARAS 数据，也不是活动标签字典。根据文件内容和 `data_transformation.py` 中的字段构造逻辑，格式为制表符分隔、无表头、每行 4 列：

| 列号 | 字段名 | 含义 |
|---:|---|---|
| 1 | `activitiesID` | 活动 ID，对应 README 中的活动标签字典。 |
| 2 | `avgDuration` | 该活动每次连续片段的平均时长，单位为小时。由活动总秒数换算为小时后除以出现次数。 |
| 3 | `numOfoccurrences` | 活动连续片段出现次数。 |
| 4 | `numOfsensors` | 在该活动对应样本中，曾出现值为 1 的传感器数量。 |

House A `processed_ARAS_R1.txt` 样例：

```text
1	0.17	100	20
2	2.23	43	19
3	0.24	40	15
4	0.47	29	16
5	0.3	27	11
```

House B `processed_ARAS_R2.txt` 样例：

```text
1	0.13	76	16
2	17.11	23	17
3	0.04	1	4
4	0.2	19	13
6	0.18	3	4
```

注意：`data_transformation.py` 中读取的是 `House B/ARAS_Dataset.txt`，但当前目录中未发现该合并文件。`mergefiles.py` 展示了将 30 个日文件合并为 `ARAS_Dataset.txt` 的意图，不过脚本里使用了 `Day_` 文件名前缀，而真实文件名为 `DAY_`。

## 文件之间的关联关系

1. `House A/README` 只适用于 `House A/DAY_*.txt` 的传感器列定义；`House B/README` 只适用于 `House B/DAY_*.txt` 的传感器列定义。两个 house 的传感器字段名、类型和位置不同，不能混用同一套传感器列名。

2. 两个 house 的活动标签字典一致。`DAY_*.txt` 第 21 列和第 22 列中的整数 ID 都通过对应 house 的 `README` 活动表解释。

3. `DAY_n.txt` 的 `n` 表示第 n 天。每个文件内部没有显式日期或时间戳，需要通过文件名的 day index 和行号恢复时间。

4. 每一行表示同一秒内 20 个传感器状态和两名住户的活动标签。也就是说，传感器观测和 `R1`、`R2` 标签在行级别对齐。

5. `processed_ARAS_R1.txt` 和 `processed_ARAS_R2.txt` 通过活动 ID 关联到 `README` 的活动字典，是从原始 `DAY_*.txt` 或合并后的 `ARAS_Dataset.txt` 统计得到的派生结果。它们不包含逐秒传感器序列，不能替代 `DAY_*.txt` 用于训练时序模型。

## 加载模块实现要点

1. 对 House A 和 House B 分别维护传感器 schema。
2. 读取 `DAY_*.txt` 时使用空格分隔、无表头、固定 22 列。
3. 为每行补充派生字段时，可添加 `house`、`day`、`second_of_day`、`time_of_day`。
4. 第 1-20 列应按 0/1 传感器状态读取；第 21、22 列应按活动 ID 整数读取。
5. 活动名称映射来自 `README`，不是从 `processed_ARAS_R*.txt` 推断。
6. 不要把 House A 的传感器列名套用到 House B；两个 house 只有活动标签字典一致。
