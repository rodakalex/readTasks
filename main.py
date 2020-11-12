from decimal import Decimal
from dateutil.parser import parse
import csv

__start_date = "10:00:00.000"
__end_date = "10:00:05.000"

contractors = {}  # ключи словаря - это контрагент и словарь со словарём из стратегий

with open('./sorted_by_close.csv', newline='') as csvfile:
    tasks = csv.reader(csvfile, delimiter=',')
    flag_header = True

    for row in tasks:
        if flag_header:
            flag_header = False
            continue

        param = {
            "strategy": row[1],
            "contract": row[2],
            "time_close": row[6],
            "custom": row[11]
        }

        if parse(__start_date) <= parse(param["time_close"]) <= parse(__end_date):
            # Заведение контракта, если он до этого не встречался
            if not param["contract"] in contractors:
                # Проверка убыток, или прибыль
                if Decimal(param["custom"]) > 0:
                    # Если по этому контракту прибыль
                    contractors[param["contract"]] = {
                        param["strategy"]: [
                            0,
                            Decimal(param["custom"]),
                        ]
                    }
                else:
                    # Если по этому контракту убыток
                    contractors[param["contract"]] = {
                        param["strategy"]: [
                            Decimal(param['custom']) * -1,
                            0,
                        ]
                    }
            else:
                # Проверка убыток, или прибыль
                if float(param["custom"]) > 0:
                    # Если по этому контракту прибыль нужно выполнить проверку по ключам, не было ли этой стратегии
                    # ранее
                    if param['strategy'] in contractors[param['contract']]:
                        contractors[param["contract"]][param["strategy"]][0] += Decimal(param['custom'])
                    else:
                        contractors[param["contract"]][param["strategy"]] = [0, Decimal(param["custom"])]
                else:
                    # Если по этому контракту убыток нужно выполнить проверку по ключам, не было ли этой стратегии
                    # ранее
                    if param['strategy'] in contractors[param['contract']]:
                        contractors[param["contract"]][param["strategy"]][1] += Decimal(param['custom']) * -1
                    else:
                        contractors[param["contract"]][param["strategy"]] = [Decimal(param["custom"]) * -1, 0]

        elif parse(__end_date) < parse(row[6]):
            break

print(f"Контрагент              Убыток\t\tПрофит\n")
for contractor in contractors.keys():
    print(f"{contractor}\n", end='')
    for strategy in contractors[contractor]:
        # print(f"-> {strategy}\t\t{contractors[contractor][strategy][0]}\t{contractors[contractor][strategy][1]}")
        if len(strategy) > 12:
            print(f"-> {strategy}", end='\t')
        else:
            print(f"-> {strategy}", end='\t\t')
        print(f"{contractors[contractor][strategy][0]}\t{contractors[contractor][strategy][1]}")
    #     if type(strategy) == str and len(strategy) > 12:
    #         print(f"{strategy}", end='\t')
    #     elif len(str(strategy)) >= 8 and type(strategy) == float:
    #         print(f"{strategy}", end='\t')
    #     else:
    #         print(f"{strategy}", end='\t\t')
    print()
