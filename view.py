import pandas as pd
import get_struckt_table

pd.options.display.max_columns = None
pd.options.display.max_rows = None

need_time = (
    ("10:00:00.000", "18:45:10.000"),
    ("19:00:00.000", "23:50:00.000"),
)

# table = get_struckt_table.calculate_only_sum("10:00:00.000", "18:45:10.000")
#
# for i in table:
#     print(pd.Series(table[i]))


def get_colums():
    index = 1
    colums_lists = []

    while index < len(need_time) + 1:
        colums_lists.append(f"Период {index}")
        colums_lists.append(f"Количество {index}")
        index += 1

    return colums_lists


# def get_dict_for_print():
#     dict_for_print = get_struckt_table.get_struct_data(need_time)
#     for strategy in dict_for_print:
#         print(f"{strategy}")
#         for contr in dict_for_print[strategy]:
#             print(f"-> {contr}")
#
#             column = 0
#             while column < len(need_time):
#                 pr = next((x for x in dict_for_print[strategy][contr] if column in x.keys()), None)
#                 column += 1
#

dict_for_print = get_struckt_table.get_struct_data(need_time)


def get_result_column():
    result_column = []
    for i in dict_for_print:
        result_column.append(i)
        for j in dict_for_print[i]:
            result_column.append(f"-> {j}")

    return result_column


def get_result_array():
    result_array = []
    for strategy in dict_for_print:
        for contr in dict_for_print[strategy]:
            column = 0
            while column < len(need_time):
                pr = next((x for x in dict_for_print[strategy][contr] if column in x.keys()), 0)
                result_array.append(pr)
                column += 1

    return result_array
# need_data = (
#     ("10:00:00.000", "10:00:05.000"),
#     ("10:00:05.000", "10:00:30.000"),
#     ("10:00:30.000", "18:45:00.000"),
# )

# struct_table = get_struckt_table.get_dict_for_print(need_data)

# table = pd.DataFrame(struct_table, columns=[1, 2, 3, 4, 5])
# print(table)


if __name__ == '__main__':
    table = pd.DataFrame(
        get_result_array(),
        columns=get_colums(),
        index=get_result_column()
    )
    print(table)
