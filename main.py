from decimal import Decimal
from dateutil.parser import parse
import csv

block_contr = [
    "BTC",
    "XBT",
]


def __get_table(need_sort=False, sort_column=None):
    with open('./example.csv', newline='') as csvfile:
        result = []
        tasks = csv.reader(csvfile, delimiter=';')
        header = False

        for log_action in tasks:
            if not header:
                header = log_action
                continue

            if log_action[2][:3] in block_contr:    # log_action[1] == 'QcEu_2010_2'
                continue

            result.append(log_action)

        if need_sort:
            result.sort(key=lambda x: x[sort_column])

        result.insert(0, header)

    return result


def calculate_param(start_date, end_date):
    result_contractors = {}
    flag_header = True

    for row in __get_table():
        if flag_header:
            flag_header = False
            continue

        param = {
            "strategy": row[1],
            "contract": row[2],
            "time_open": row[5],
            "time_close": row[6],
            "custom": row[11]
        }

        if not param["contract"][-1].isdigit():
            continue

        if parse(start_date) <= parse(param["time_open"]) <= parse(end_date):
            # Заведение контракта, если он до этого не встречался
            if not param["contract"] in result_contractors:
                # Проверка убыток, или прибыль
                if Decimal(param["custom"]) > 0:
                    # Если по этому контракту прибыль
                    result_contractors[param["contract"]] = {
                        param["strategy"]: [
                            0,
                            Decimal(param["custom"]),
                        ]
                    }
                else:
                    # Если по этому контракту убыток
                    result_contractors[param["contract"]] = {
                        param["strategy"]: [
                            Decimal(param['custom']) * -1,
                            0,
                        ]
                    }
            else:
                # Проверка убыток, или прибыль
                if Decimal(param["custom"]) > 0:
                    # Если по этому контракту прибыль нужно выполнить проверку по ключам, не было ли этой стратегии
                    # ранее
                    if param['strategy'] in result_contractors[param['contract']]:
                        result_contractors[param["contract"]][param["strategy"]][1] += Decimal(param['custom'])
                    else:
                        result_contractors[param["contract"]][param["strategy"]] = [0, Decimal(param["custom"])]
                else:
                    # Если по этому контракту убыток нужно выполнить проверку по ключам, не было ли этой стратегии
                    # ранее
                    if param['strategy'] in result_contractors[param['contract']]:
                        result_contractors[param["contract"]][param["strategy"]][1] += Decimal(param['custom']) * -1
                    else:
                        result_contractors[param["contract"]][param["strategy"]] = [Decimal(param["custom"]) * -1, 0]

        elif parse(end_date) < parse(param["time_open"]):
            return result_contractors


def get_struct_data(need_time):
    steps = print_header(need_time)
    result_dict = {}
    index = 0

    for step in steps:
        for contr in step:
            temp_dict = {}
            for strategy in step[contr]:

                temp_dict[strategy] = [
                    {
                        index: step[contr][strategy][1] - step[contr][strategy][0]
                    }
                ]

            if contr in result_dict:
                # Если ключи совпадают, то их нужно объеденить, если нет, то их нужно добавить
                for temp_contr in temp_dict:
                    if temp_contr not in result_dict[contr]:
                        result_dict[contr][temp_contr] = temp_dict[temp_contr]
                    else:
                        result_dict[contr][temp_contr] += temp_dict[temp_contr]
            else:
                # Если нет контрагента, то нужно добавить его в список
                result_dict[contr] = temp_dict
        index += 1

    return result_dict


def print_header(need_time):
    steps = return_stepts(need_time)
    print_stepts(need_time)
    return steps


def print_stepts(need_time):
    index = 1
    while index < len(need_time) + 1:
        print(f"Шаг {index}", end='\t\t\t')
        index += 1
    print()


def return_stepts(need_time):
    steps = []
    index = 1
    for time in need_time:
        steps.append(calculate_param(time[0], time[1]))
        print(f"Шаг {index}: {time[0]} по {time[1]}")
        index += 1
    print(f"\nКонтрагент", end='\t\t')
    return steps


if __name__ == '__main__':
    need_data = (
        ("10:00:00.000", "10:00:05.000"),
        ("10:00:05.000", "10:00:30.000"),
        ("10:00:30.000", "18:45:00.000"),
    )

    dict_for_print = get_struct_data(need_data)

    for strategy in dict_for_print:
        print(f"{strategy}")
        for contr in dict_for_print[strategy]:
            if len(contr) > 12:
                print(f"-> {contr}", end='\t')
            else:
                print(f"-> {contr}", end='\t\t')

            column = 0
            while column < len(need_data):
                pr = next((x for x in dict_for_print[strategy][contr] if column in x.keys()), None)

                if pr and len(f"{pr[column]}") == 16:
                    print(pr[column], end='\t')
                elif pr and len(f"{pr[column]}") < 8:
                    print(pr[column], end='\t\t\t')
                elif pr:
                    print(pr[column], end='\t\t')
                else:
                    print(0, end='\t\t\t')
                column += 1
            print()

    print("\n__________________________________________________\n")
    # get_struct_data(("10:00:00.000", "18:45:10.000"), ("19:00:00.000", "23:50:00.000"))


#
#     # Количество стратегий которые сначала торгуют в убыток/прибыль, а затем в прибыль/убыток
#     if step_1 < 0 and 0 < step_2:
#         count_pre_loss += 1
#
#     if step_1 < 0:
#         count_negative_5 += 1
#     else:
#         count_positive_5 += 1
#
#     if step_2 < 0:
#         count_negative_18 += 1
#     else:
#         count_positive_18 += 1
#
#     if len(f"{step_1}") == 16:
#         print(f"{step_1}", end='\t')
#     elif len(f"{step_1}") < 8:
#         print(f"{step_1}", end='\t\t\t')
#     else:
#         print(f"{step_contr}", end='\t\t')
#
# print(f"{step_2}")
# for contractor in step:
#     print(f"{contractor}\n", end='')
#     for strategy in step[contractor]:
#         step_contr = step[contractor][strategy][1] - step[contractor][strategy][0]
#         #
#         # # Отображение контрагентов
#         # if len(strategy) > 12:
#         #     print(f"-> {strategy}", end='\t')
#         # else:
#         #     print(f"-> {strategy}", end='\t\t')
#
#     print()

# print(f"Убыточные стратегии в течении 5 секунд: {count_negative_5}")
# print(f"Прибыльные стратегии в течении 5 секунд: {count_positive_5}")
# print(f"Убыточные стратегии в течении 8 часов: {count_negative_18}")
# print(f"Прибыльные стратегии в течении 8 часов: {count_positive_18}")
# print(f"Количество стратегий, которые торгуют в минус, а затем в плюс: {count_pre_loss}\n")
#
# for time in list_strategy:
#     print(time)

# count_pre_loss = 0
# count_negative_5 = 0
# count_positive_5 = 0
# count_negative_18 = 0
# count_positive_18 = 0
