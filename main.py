from decimal import Decimal
from dateutil.parser import parse
import csv

block_contr = [
    "BTC",
    "XBT",
]

__start_date = "10:00:00.000"
__end_date = "10:00:05.000"


def get_sorted_table():
    with open('./example.csv', newline='') as csvfile:
        sorted_table = []
        tasks = csv.reader(csvfile, delimiter=';')
        header = False

        for log_action in tasks:
            if not header:
                header = log_action
                continue

            if log_action[2][:3] in block_contr:
                continue

            sorted_table.append(log_action)

        sorted_table.sort(key=lambda x: x[6])
        sorted_table.insert(0, header)

    return sorted_table


def calculate_param(start_date, end_date):
    result_contractors = {}
    flag_header = True

    for row in get_sorted_table():
        if flag_header:
            flag_header = False
            continue

        param = {
            "strategy": row[1],
            "contract": row[2],
            "time_close": row[6],
            "custom": row[11]
        }

        if not param["contract"][-1].isdigit():
            continue

        if parse(start_date) <= parse(param["time_close"]) <= parse(end_date):
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

        elif parse(end_date) < parse(param["time_close"]):
            return result_contractors


contractors = calculate_param(__start_date, __end_date)
next_contractors = calculate_param(__start_date, "18:00:00.000")

print(f"Шаг 1: {__start_date} по {__end_date}")
print(f"Шаг 1: {__start_date} по 18:00:00.000")
print(f"\nКонтрагент\t\tШаг 1\t\t\tШаг 2\n")

count_negative_5 = 0
count_positive_5 = 0

count_negative_18 = 0
count_positive_18 = 0

for contractor in contractors.keys():
    print(f"{contractor}\n", end='')
    for strategy in contractors[contractor]:
        # Отображение контрагентов
        if len(strategy) > 12:
            print(f"-> {strategy}", end='\t')
        else:
            print(f"-> {strategy}", end='\t\t')

        total_5 = contractors[contractor][strategy][1] - contractors[contractor][strategy][0]
        total_18 = next_contractors[contractor][strategy][1] - next_contractors[contractor][strategy][0]

        if total_5 < 0:
            count_negative_5 += 1
        else:
            count_positive_5 += 1

        if total_18 < 0:
            count_negative_18 += 1
        else:
            count_positive_18 += 1

        if len(f"{total_5}") == 13:
            print(f"{total_5}", end='\t')
        elif len(f"{total_5}") < 8:
            print(f"{total_5}", end='\t\t\t')
        else:
            print(f"{total_5}", end='\t\t')

        print(f"{total_18}")

    print()

print(f"Убыточные стратегии в течении 5 секунд: {count_negative_5}")
print(f"Прибыльные стратегии в течении 5 секунд: {count_positive_5}")
print(f"Убыточные стратегии в течении 8 часов: {count_negative_18}")
print(f"Прибыльные стратегии в течении 8 часов: {count_positive_18}")

# # Отображение убыток/профита/Итогов
# if len(f"{contractors[contractor][strategy][0]}") < 8:
#     print(f"{contractors[contractor][strategy][0]}", end='\t\t')
# else:
#     print(f"{contractors[contractor][strategy][0]}", end='\t')
#
# if len(f"{contractors[contractor][strategy][1]}") < 8:
#     print(f"{contractors[contractor][strategy][1]}", end='\t\t')
# else:
#     print(f"{contractors[contractor][strategy][1]}", end='\t')
