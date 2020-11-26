import copy
import pandas as pd
import api
import matplotlib.pyplot as plt

pd.options.display.max_columns = None
pd.options.display.max_rows = None

need_time = (
    ("10:00:00.000", "10:00:02.000"),
    ("10:00:02.000", "10:00:04.000"),
    ("10:00:04.000", "10:00:06.000"),
    ("10:00:06.000", "10:00:08.000"),
    ("10:00:08.000", "10:00:10.000"),
    ("10:00:10.000", "10:00:12.000"),
    ("10:00:12.000", "10:00:14.000"),
    ("10:00:14.000", "10:00:16.000"),
    ("10:00:16.000", "10:00:18.000"),
    ("10:00:18.000", "10:00:20.000"),
    ("10:00:20.000", "10:00:22.000"),
    ("10:00:22.000", "10:00:24.000"),
    ("10:00:24.000", "10:00:26.000"),
    ("10:00:26.000", "10:00:28.000"),
    ("10:00:28.000", "10:00:30.000"),
)

# need_time = (
#     ("10:00:00.000", "10:00:05.000"),
#     ("10:00:05.000", "10:00:30.000"),
#     ("10:00:30.000", "10:03:00.000"),
#     ("10:03:30.000", "10:30:00.000"),
#     ("10:30:30.000", "11:00:00.000"),
#     ("11:00:00.000", "12:00:00.000"),
#     ("12:00:00.000", "12:30:00.000"),
#     ("12:30:00.000", "13:30:00.000"),
#     ("13:30:00.000", "14:00:00.000"),
#     ("14:00:00.000", "14:30:00.000"),
#     ("14:30:00.000", "15:00:00.000"),
#     ("15:00:00.000", "15:30:00.000"),
#     ("15:30:00.000", "16:00:00.000"),
#     ("16:00:00.000", "16:30:00.000"),
#     ("16:30:00.000", "17:00:00.000"),
#     ("17:00:00.000", "17:30:00.000"),
#     ("17:30:00.000", "18:00:00.000"),
#     ("18:00:00.000", "18:30:00.000"),
#     ("18:30:00.000", "18:45:00.000"),
# )
#
# need_time = (
#     ("10:00:00.000", "11:00:00.000"),
#     ("11:00:00.000", "12:00:00.000"),
#     ("12:00:00.000", "13:00:00.000"),
#     ("13:00:00.000", "14:00:00.000"),
#     ("14:00:00.000", "15:00:00.000"),
#     ("15:00:00.000", "16:00:00.000"),
#     ("16:00:00.000", "17:00:00.000"),
#     ("17:00:00.000", "18:00:00.000"),
#     ("18:00:00.000", "19:00:00.000"),
#     ("19:00:00.000", "20:00:00.000"),
#     ("20:00:00.000", "21:00:00.000"),
#     ("21:00:00.000", "22:00:00.000"),
#     ("22:00:00.000", "23:00:00.000"),
#     ("23:00:00.000", "23:59:59.999"),
# )

# need_time = (
#     ("10:00:00.000", "11:00:00.000"),
#     ("11:00:00.000", "12:00:00.000"),
#     ("12:00:00.000", "13:00:00.000"),
#     ("13:00:00.000", "14:00:00.000"),
#     ("14:00:00.000", "15:00:00.000"),
#     ("15:00:00.000", "16:00:00.000"),
#     ("16:00:00.000", "17:00:00.000"),
#     ("17:00:00.000", "18:00:00.000"),
#     ("18:00:00.000", "19:00:00.000"),
#     ("19:00:00.000", "20:00:00.000"),
#     ("20:00:00.000", "21:00:00.000"),
#     ("21:00:00.000", "22:00:00.000"),
#     ("22:00:00.000", "23:00:00.000"),
#     ("23:00:00.000", "23:59:59.999"),
# )

dict_for_print = api.get_struct_data(need_time)


def get_colums():
    index = 1
    colums_lists = []

    while index < len(need_time) + 1:
        colums_lists.append(f"Период {index}")
        colums_lists.append(f"Количество {index}")
        index += 1

    return colums_lists


def get_result_column():
    result_column = []
    for i in dict_for_print:
        result_column.append(i)
        for j in dict_for_print[i]:
            result_column.append(f"-> {j}")

    return result_column


def get_result_array_for_all_print():
    result_array = []
    for strategy in dict_for_print:
        result_array.append(['' for i in range(0, (len(need_time) * 2))])
        for contr in dict_for_print[strategy]:
            column = 0
            temp_list = []
            while column < len(need_time):
                pr = next((x for x in dict_for_print[strategy][contr] if column in x.keys()), {
                    "sum": 0,
                    'count': 0
                })
                temp_list += list(pr.values())
                column += 1

            result_array.append(temp_list)

    return result_array


def print_all_table():
    table = pd.DataFrame(
        get_result_array_for_all_print(),
        columns=get_colums(),
        index=get_result_column()
    )

    print(table)


def get_data_for_show_graph_only_strategy(choice_strategy, choice_contractor=None):
    temp_list = []
    for contr in dict_for_print:
        if choice_contractor and choice_contractor != contr:
            continue

        if choice_strategy in dict_for_print[contr]:
            for column in range(0, len(need_time)):
                pr = next((x for x in dict_for_print[contr][choice_strategy] if column in x.keys()), {
                    'val': float(0),
                    'count': 0,
                })
                temp_list.append(pr)

    index = 0
    copy_temp = copy.deepcopy(temp_list)
    for i in copy_temp:
        for j in i:
            if type(j) == int:
                temp_list[index]['val'] = float(temp_list[index].pop(j))

        index += 1

    if not temp_list:
        print(None)
        return

    index = 0
    while index < len(temp_list):
        temp_list[index]['Период'] = need_time[index % len(need_time)][0]
        index += 1

    return temp_list


def print_choice_strategy(choice_strategy, choice_contractor=None):
    data = get_data_for_show_graph_only_strategy(
        choice_strategy=choice_strategy,
        choice_contractor=choice_contractor,
    )

    if not data:
        return

    df = pd.DataFrame(data).groupby(by='Период').sum()
    # print(df)
    if choice_contractor:
        title = f"{choice_contractor} | {choice_strategy}"
    else:
        title = f"All | {choice_strategy}"

    temp_list = []
    for i in df['val']:
        if i < 0:
            temp_list.append(abs(i))
        else:
            temp_list.append(i)

    df['sum'] = pd.Series(temp_list, index=df.index)
    # print(df)

    df.plot(
        kind='bar',
        y=['sum', "count"],
        # x='Период',
        secondary_y='count',
        color={"sum": (df['val'] > 0).map({True: 'g', False: 'r'}), "count": "b"},
        rot=0,
        figsize=(25, 8),
        title=title,
    )
    # plt.show()
    plt.savefig(f'./графики/с 10 до 18:45/стратегии/{choice_strategy}.png')
    plt.close()


def print_graph_contractor(choice_contractor):
    temp_list = []
    for contr in dict_for_print:
        if choice_contractor != contr:
            continue

        for i in dict_for_print[contr]:
            index = 0
            while index < len(need_time):
                pr = next((x for x in dict_for_print[contr][i] if index in x.keys()), {
                    index: 0,
                    'sum': 0,
                    'count': 0,
                })

                temp_list.append(pr)
                index += 1

    result_list = []
    copy_temp = copy.deepcopy(temp_list)
    for i in copy_temp:
        index_period = list(i.keys())[0]
        result_list.append({
            'count': i['count'],
            'val': float(i[index_period]),
            'date': f"{need_time[index_period][0]}",
        })

    if not result_list:
        return None

    df = pd.DataFrame(result_list).groupby(by='date').sum()

    temp_list = []
    for i in df['val']:
        if i < 0:
            temp_list.append(abs(i))
        else:
            temp_list.append(i)

    df['sum'] = pd.Series(temp_list, index=df.index)

    df.plot(
        kind='bar',
        y=['sum', "count"],
        secondary_y='count',
        color={"sum": (df['val'] > 0).map({True: 'g', False: 'r'}), "count": "b"},
        rot=0,
        figsize=(25, 8),
        title=choice_contractor,
    )

    plt.savefig(f'./графики/с 10 до 18:45/контрагенты/{choice_contractor}.png')
    plt.close()


if __name__ == '__main__':
    strategy = api.get_all_strategy()
    contractor = api.get_all_contr()

    for j in contractor:
        print(f"Контрагент {j}")
        print_graph_contractor(j)

    for i in strategy:
        print_choice_strategy(choice_strategy=i)
        print(f"Стратегия {i}")

