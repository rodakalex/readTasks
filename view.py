import copy

import pandas as pd
import api
import matplotlib.pyplot as plt

pd.options.display.max_columns = None
pd.options.display.max_rows = None


need_time = (
    ("10:00:00.000", "10:00:05.000"),
    # ("10:00:05.000", "10:00:30.000"),
    # ("10:00:30.000", "10:03:00.000"),
    # ("10:03:30.000", "10:30:00.000"),
    # ("10:30:30.000", "11:00:00.000"),
    # ("11:00:00.000", "12:00:00.000"),
    # ("12:00:00.000", "12:30:00.000"),
    # ("12:30:00.000", "13:30:00.000"),
    # ("13:30:00.000", "14:00:00.000"),
    # ("14:00:00.000", "14:30:00.000"),
    # ("14:30:00.000", "15:00:00.000"),
    # ("15:00:00.000", "15:30:00.000"),
    # ("15:30:00.000", "16:00:00.000"),
    # ("16:00:00.000", "16:30:00.000"),
    # ("16:30:00.000", "17:00:00.000"),
    # ("17:00:00.000", "17:30:00.000"),
    # ("17:30:00.000", "18:00:00.000"),
    # ("18:00:00.000", "18:30:00.000"),
    # ("18:30:00.000", "18:45:00.000"),
)
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


def get_data__for_show_graph_only_strategy(choice_strategy, choice_contractor=None):

    temp_list = []
    for contr in dict_for_print:
        if choice_contractor and choice_contractor != contr:
            continue

        if choice_strategy in dict_for_print[contr]:
            for column in range(0, len(need_time)):
                pr = next((x for x in dict_for_print[contr][choice_strategy] if column in x.keys()), {
                    'sum': float(0),
                    'count': 0,
                })
                temp_list.append(pr)

    index = 0
    copy_temp = copy.deepcopy(temp_list)
    for i in copy_temp:
        for j in i:
            if type(j) == int:
                temp_list[index]['sum'] = float(temp_list[index].pop(j))

        index += 1

    index = 0
    while len(need_time) > index:
        temp_list[index]['Период'] = f"С {need_time[index][0]}\nпо {need_time[index][1]}"
        index += 1

    return temp_list


def print_graph_only_contractor(contractor):
    pass


if __name__ == '__main__':
    choice_strategy = 'QcEu_2010_2'
    choice_contractor = 'EuZ0'
    data = get_data__for_show_graph_only_strategy(
        choice_strategy=choice_strategy,
        choice_contractor=choice_contractor,
    )
    df = pd.DataFrame(data)
    df.plot(
        kind='bar',
        y='sum',
        rot=0,
        x='Период',
        figsize=(20, 8),
        title=f'{choice_contractor} / {choice_strategy}',
    )
    plt.show()
    # print_all_table()
    # get_result_array_for_all_print()
