import csv

block_contr = [
    "BTC",
    "XBT",
]

with open('./example.csv', newline='') as csvfile:
    tasks = csv.reader(csvfile, delimiter=';')
    header = False
    temp_list = []

    for row in tasks:
        if not header:
            header = row
            continue

        if row[2][:3] in block_contr:
            continue

        temp_list.append(row)

    temp_list.sort(key= lambda x: x[6])
    temp_list.insert(0, header)

    wtiter = csv.writer(open ("./sorted_by_close.csv", 'w'))
    for i in temp_list:
        wtiter.writerow(i)
