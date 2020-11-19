import pandas as pd
import numpy as np
import get_struckt_table
import matplotlib.pyplot as plt

pd.options.display.max_columns = None
pd.options.display.max_rows = None

# need_time = (
#     ("10:00:00.000", "18:45:10.000"),
#     ("19:00:00.000", "23:50:00.000"),
# )

need_time = (
    ("10:00:00.000", "10:00:05.000"),
    ("10:00:05.000", "10:00:30.000"),
    ("10:00:30.000", "18:45:00.000"),
)

dict_for_print = get_struckt_table.get_struct_data(need_time)


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
    if choice_contractor:
        pass

    temp_list = []
    for contr in dict_for_print:
        if choice_strategy in dict_for_print[contr]:
            for column in range(0, len(need_time)):
                pr = next((x for x in dict_for_print[contr][choice_strategy] if column in x.keys()), {
                    'sum': 0,
                    'count': 0,
                })
                temp_list.append(pr)

    return temp_list


def print_graph_only_contractor(contractor):
    pass


if __name__ == '__main__':
    data = get_data__for_show_graph_only_strategy(choice_strategy='QcEu_2010_2')
    data[0]['sum'] = data[0].pop(0)
    data[2]['sum'] = data.pop(2)
    print(pd.DataFrame(data))
    data.plot(kind='bar', x='count', y='1')
    plt.show()
    # print_all_table()
    # get_result_array_for_all_print()