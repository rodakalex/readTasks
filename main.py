from dateutil.parser import parse
import csv

test_date = "2020-11-10 01:40:56.552"
test_date2 = "2020-11-10 01:43:41.103"

with open('./example.csv', newline='') as csvfile:
    tasks = csv.reader(csvfile, delimiter=';')
    flag_header = True
    instr_dict = {}
    for row in tasks:
        if flag_header:
            flag_header = False
            continue

        if parse(test_date) <= parse(row[3]) <= parse(test_date2):
            pass

        elif parse(test_date2) < parse(row[3]):
            break
