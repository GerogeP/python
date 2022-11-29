"""题目：我们做了一个活动，根据用户的积分来抽奖，用户的积分都保存在一个数组里面

arr = [20, 34, 160, 2…]，数组下标就是用户的 ID，则这里：

ID 为 0 的用户的积分是 arr[0] 等于 20 分。

ID 为 1 的用户的积分是 arr[1] 等于 34 分。

请你设计一个抽奖算法，随机抽出一位中奖用户，要求积分越高中奖概率越高。

返回值是中奖用户的 ID

PS: 1<= arr.length <= 50000 且 1<= arr[i] <= 50000

代码写出算法，

并分析其时间复杂度，

为其编写尽量多 unit test。

FAQ：

我可以上网吗？－－ 可以，make yourself comfortable。

我可以问别人吗？ －－ 请独立完成，if you lie , we’ll know sooner or later。

我超过 30 分钟怎么办？请尽量按时提交。如果超过 30 分钟，请标注下完成用时。

我做不完怎么办？没关系请尽量按点顺序完成

完成后，可以发到邮箱：bhruan@riches.ai
"""

import random


# print('groups')
def scored_random(data, groups):
    data_origin = data
    # 将全部数据排序
    data = sorted(data, reverse=True)
    # print('data :', data, data_origin)
    # 将数据按大小不同分组，数值越大的组中数据的数量越少
    group_numbers = []
    blocks = 0
    serial = 0
    while serial < groups:
        blocks += serial + 1
        group_numbers.append(blocks)
        # print('blocks : ', blocks)
        serial += 1

    # print('group_numbers : ', group_numbers, sum(group_numbers))

    group_items = []
    group_serial = 0
    courser = 0
    while group_serial < len(group_numbers) - 1:
        # print('group_serial : ', group_serial)
        start = courser
        end = int(len(data) * group_numbers[group_serial] / sum(group_numbers))
        # print(start, end)
        group_items.append(data[start: end])
        group_serial += 1
        courser = end
    group_items.append(data[courser:])

    # print(group_items)

    # 分组之间抽签
    group_number = int(random.random() * groups)

    # print('group_number : ', group_number)
    # 中签组中抽签
    group_scale = len(group_items[group_number])
    # print(group_scale)
    item_key = int(group_scale * random.random())
    # print('item_key : ', item_key)
    chosen_value = group_items[group_number][item_key]
    # print(chosen_value)

    # print('data_origin :', data_origin)
    return data_origin.index(chosen_value)


# taotal+value : 一共有多少个数据，本题中为都少个有积分的用户，随机生成。
# groups， 将数据分成不同权重的分组数量，本题中至少为3个，最多为：积分个数的20分之一
arr = []
total_values = 200
groups = 3 if total_values < 20 else total_values / 20
x = 0
while x < total_values:
    arr.append(int(random.random() * 1000))
    x += 1

# print(arr)
group = 1
while group < groups:
    print(scored_random(arr, group))
    group += 1

# 本程序对哦数据进行了两次以为遍历，股器事件复杂读为O(2n)。
