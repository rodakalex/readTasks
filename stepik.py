input_string = str(input())
temp_list = []

split_str = list(map(int, input_string.split()))

if len(split_str) == 1:
    print(split_str[0])
else:
    index = 0
    while index < len(split_str):
        if index == 0:
            temp_list.append(split_str[-1] + split_str[index + 1])
        elif index == len(split_str) - 1:
            temp_list.append(split_str[0] + split_str[-2])
        else:
            temp_list.append(split_str[index + 1] + split_str[index - 1])
        index += 1

    print(" ".join(map(str, temp_list)))
