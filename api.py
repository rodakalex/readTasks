from decimal import Decimal
from dateutil.parser import parse
import csv

block_contr = [
    "BTC",
    "XBT",
]


def get_table(need_sort=True, sort_column=5):
    with open('./example.csv', newline='') as csvfile:
        result = []
        tasks = csv.reader(csvfile, delimiter=';')
        header = False
        for log_action in tasks:

            if not header:
                header = log_action
                continue

            if not log_action[2][-1].isdigit():
                continue

            if log_action[2][:3] in block_contr:
                continue

            result.append(log_action)

        if need_sort:
            result.sort(key=lambda x: x[sort_column])

        # result.insert(0, header)

    return result


table = get_table()


def get_all_contr():
    temp_set = set()
    for i in table:
        temp_set.add(i[2])
    return temp_set


def calculate_param(start_date, end_date):
    result_contractors = {}

    for row in table:

        param = get_param_for_table(row)

        if parse(start_date) <= parse(param["time_open"]) <= parse(end_date):
            # Заведение контракта, если он до этого не встречался
            if not param["contract"] in result_contractors:
                # Проверка убыток, или прибыль
                if Decimal(param["custom"]) > 0:
                    # Если по этому контракту прибыль
                    result_contractors[param["contract"]] = {
                        param["strategy"]: [
                            0,                                  # Заполнение убытка нулевым значением
                            Decimal(param["custom"]),           # Заполнение прибыли
                            Decimal(param["custom"]),           # Заполнение итогов прибыли
                            1,                                  # Количество стратегий упавших в таблицу
                        ]
                    }
                else:
                    # Если по этому контракту убыток
                    result_contractors[param["contract"]] = {
                        param["strategy"]: [
                            0,
                            Decimal(param['custom']) * -1,      # Подсчёт убытка
                            Decimal(param['custom']),           # Параметр отвечающий за итог
                            1,                                  # Количество стратегий упавших в таблицу
                        ]
                    }
            else:
                # Проверка убыток, или прибыль
                if Decimal(param["custom"]) > 0:
                    # Если по этому контракту прибыль нужно выполнить проверку по ключам, не было ли этой стратегии
                    # ранее
                    if param['strategy'] in result_contractors[param['contract']]:
                        # Добавление к прибыли текущей прибыли
                        result_contractors[param["contract"]][param["strategy"]][1] += Decimal(param['custom'])
                        # Добавление к итогу текущей прибыли
                        result_contractors[param["contract"]][param["strategy"]][2] += Decimal(param['custom'])
                        # Добавление к количеству стратегий упавших в таблицу
                        result_contractors[param["contract"]][param["strategy"]][3] += 1
                    else:
                        result_contractors[param["contract"]][param["strategy"]] = [
                            # Если этой стратегии не было ранее, но есть прибыль есть, то нужно её добавить в общий
                            # список
                            0,                                  # Параметр убытка
                            Decimal(param["custom"]),           # Параметр прибыли
                            Decimal(param["custom"]),           # Параметр отвечающий за итог
                            1,                                  # Количество стратегий упавших в таблицу
                        ]
                else:
                    # Если по этому контракту убыток нужно выполнить проверку по ключам, не было ли этой стратегии
                    # ранее
                    if param['strategy'] in result_contractors[param['contract']]:
                        # Сложение убытка
                        result_contractors[param["contract"]][param["strategy"]][1] += Decimal(param['custom']) * -1
                        # Сложение итогов
                        result_contractors[param["contract"]][param["strategy"]][2] += Decimal(param['custom'])
                        # Добавление к количеству стратегий упавших в таблицу
                        result_contractors[param["contract"]][param["strategy"]][3] += 1
                    else:
                        result_contractors[param["contract"]][param["strategy"]] = [
                            Decimal(param["custom"]) * -1,      # Параметр убытка
                            0,                                  # Параметр прибыли
                            Decimal(param["custom"]),           # Параметр отвечающий за итог
                            1,                                  # Количество стратегий упавших в таблицу
                        ]

        elif parse(end_date) < parse(param["time_open"]):
            return result_contractors

    # Возврат на случай, если выбранный период превышает заданный интервал
    return result_contractors


def get_param_for_table(row):
    param = {
        "strategy": row[1],
        "contract": row[2],
        "time_open": row[5],
        "time_close": row[6],
        "custom": row[11]
    }
    return param


def calculate_only_sum(start_date, end_date):
    result_contractors = {}

    for row in table:

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
                result_contractors[param["contract"]] = {
                    param["strategy"]: [
                        Decimal(param["custom"]),           # Заполнение итогов прибыли
                        1,                                  # Количество стратегий упавших в таблицу
                    ]
                }
            else:
                # Если по этому контракту прибыль нужно выполнить проверку по ключам, не было ли этой стратегии
                # ранее
                if param['strategy'] in result_contractors[param['contract']]:
                    # Добавление к итогу текущей прибыли
                    result_contractors[param["contract"]][param["strategy"]][0] += Decimal(param['custom'])
                    # Добавление к количеству стратегий упавших в таблицу
                    result_contractors[param["contract"]][param["strategy"]][1] += 1
                else:
                    result_contractors[param["contract"]][param["strategy"]] = [
                        # Если этой стратегии не было ранее, то нужно её добавить в общий список
                        Decimal(param["custom"]),           # Параметр отвечающий за итог
                        1,                                  # Количество стратегий упавших в таблицу
                    ]
        elif parse(end_date) < parse(param["time_open"]):
            return result_contractors

    # Возврат на случай, если выбранный период превышает заданный интервал
    return result_contractors


def get_struct_data(need_time):
    steps = return_stepts(need_time)
    result_dict = {}
    index = 0

    for step in steps:
        for contr in step:
            temp_dict = {}
            for strategy in step[contr]:

                temp_dict[strategy] = [
                    {
                        index: step[contr][strategy][0],
                        'count': step[contr][strategy][1],
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


def return_stepts(need_time):
    steps = []
    index = 1
    for time in need_time:
        steps.append(calculate_only_sum(time[0], time[1]))
        print(f"Период {index}: {time[0]} по {time[1]}")
        index += 1
    return steps


if __name__ == '__main__':
    # need_time = (
    #     ("10:00:00.000", "10:00:05.000"),
    #     ("10:00:05.000", "10:00:30.000"),
    #     ("10:00:30.000", "18:45:00.000"),
    # )
    # get_table()
    print(get_all_contr())
