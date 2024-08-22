import math


def enumerate_trees(max_n):
    if max_n == 0:
        return ["1"]

    if max_n == 1:

        return ["1", "011"]

    # the first iteration of n is equal to 0 + n-1 first iter + 1
    else:
        enums = [["1"], ["011"]]
        for i in range(2, max_n + 1):
            new_enum = []
            for item in enums[i - 1]:
                n = len(item)
                for j in range(n):
                    next_order_enum = ""
                    if item[j] == "1":
                        # find alternatives to slicing
                        start = item[:j]
                        middle = "011"
                        end = item[j + 1:]

                        next_order_enum = "".join((start, middle, end))
                        new_enum.append(next_order_enum)

            enums.append(new_enum)

    return enums


# SOLVE: Remove duplicates

# def partitions(n):
#     partition = [(n-1, 0)]
#     n -= 2
#     k = 1
#
#     while n >= 0:
#         partition.append(tuple((n, k)))
#         n -= 1
#         k += 1
#
#     return partition

def get_all_duplicates(lst):
    dupe_list = []
    instance_list = []
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] == lst[j]:
                dupe_list.append(lst[i])
                instance_list.append(i)

    return dupe_list, instance_list

def is_even(n):
    return not n % 2

if __name__ == '__main__':
    # print(enumerate_trees(3))
    n = 3
    print(enumerate_trees(n)[n])
    print(get_all_duplicates(enumerate_trees(n)[n])[0])
    print(get_all_duplicates(enumerate_trees(n)[n])[1])
    print(len(get_all_duplicates(enumerate_trees(n)[n])[0]))







# TODO: do we have to enumerate absolutely all cases or are they handled in previous enums?
