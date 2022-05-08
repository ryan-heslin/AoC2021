#! /usr/bin/env python3
import re
import regex
from math import floor, ceil
from functools import reduce


with open("inputs/day18.txt") as f:
    raw_input = f.read()

processed = raw_input.split("\n")[:-1]


def add(lhs, rhs):
    temp = eval(lhs)
    temp.append(eval(rhs))
    return str(temp)


def split(num, pattern=r"(?!-)(\d{2,})"):
    if not (replace := regex.findall(pattern, num)):
        return num, False
    replace = replace[0]
    div = float(replace) / 2
    sub = f"[{floor(div)}, {ceil(div)}]"
    num = re.sub(pattern, sub, num, 1)
    return num, True


# We all cheat sometimes
# Possible to match all nested pairs, get correct by counting brackets
def count_brackets(string):
    count = 0
    for i, char in enumerate(string):
        if char == "[":
            count += 1
        elif char == "]":
            count -= 1
        if count == 5:
            yield i
    yield None


def explode(num, pattern=r"((\[[^[]*?)((?1)|(\])){4})|\[{4}(?:\d+,)?(\[\d+,\d+\])"):
    # result = regex.match(pattern, num)
    # Kludge pattern has two groups, one for special case
    # breakpoint()
    # if result is None:
    # return num, False
    # if result.groups(5) is not None:
    # matched = result.groups(5)
    # start, end = result.span(5)
    #
    # elif result.groups(2) is not None:
    # matched = result.groups(2)
    # start, end = result.span(2)
    if (start := next(count_brackets(num))) is None:
        return num, False
    # Ending position - off by one?
    end = regex.search(r"\]", num[start:]).end() + start - 1
    assert num[end] == "]"

    left_num, right_num = (int(x) for x in regex.findall(r"\d+", num[start:])[0:2])
    if prev_num := regex.findall(r"\d+", num[0:start]):
        sub = str(int(prev_num[-1]) + left_num)
        left = regex.sub(r"\d+(?=[^\d]*$)", sub, num[0:start])
    else:
        left = num[0:start]
        # num = left + num[start:]
    if next_num := regex.findall(r"\d+", num[(1 + end) :]):
        sub = str(int(next_num[0]) + right_num)
        right = regex.sub(r"\d+", sub, num[(end + 1) :], 1)
    else:
        right = num[(end + 1) :]
    middle = "0"
    # Add appropriate commas
    middle = middle + "," if regex.match(r"\d", right[0]) else middle
    middle = "," + middle if regex.match(r"\d", left[-1]) else middle
    # num = regex.sub(f"\\[{matched}\\]", "0", num)
    return left + middle + right, True


def find_magnitude(lst):
    if isinstance(lst, int):
        return lst
    else:
        return 3 * find_magnitude(lst[0]) + 2 * find_magnitude(lst[1])


def process(nums):
    while len(nums) > 1:
        cur = [nums.pop(0)]
        cur.extend([nums[0]])
        cur = regex.sub(r"'|\s", "", str(cur))
        nums[0] = cur

        while True:
            # print(nums[0])
            nums[0], has_exploded = explode(nums[0])
            # print("Explode\n" + nums[0] + str(has_exploded))
            if not has_exploded:
                nums[0], has_split = split(nums[0])
                # print("Split\n" + nums[0] + str(has_split))
                if not has_split:  # Finish if neither operation performed
                    # print(nums[0])
                    assert not regex.match(r"\d{2,}", nums[0])
                    break
    return nums[0]


def find_largest(nums):
    highest_magnitude = 0

    for i, num1 in enumerate(nums):
        for j, num2 in enumerate(nums):
            if not i == j:
                result = process([num1, num2])
                highest_magnitude = max(highest_magnitude, find_magnitude(eval(result)))
    return highest_magnitude


summed = eval(process(processed.copy()))
magnitude = find_magnitude(summed)  # sum([find_magnitude(x) for x in summed])
print(f"Answer 1: {magnitude}")

answer2 = find_largest(processed)
print(f"Answer 2: {answer2}")

# processed = [eval(num) for num in raw_input.split("\n")[:-1]]

# def add(lhs, rhs):
# concatenated = lhs + rhs
# traverse(concatenated)
#
# def split(num):
# first = num // 2
# return [first, num - first]
#
# def is_pair(el):
# return (isinstance(el, list) and
# isinstance(el[0], int) and
# isinstance(el[1], int))
#
# def explode(pair, lhs = None, rhs = None):
# lhs = -pair[0] if not lhs else lhs
# rhs = -pair[1] if not rhs else rhs
# pair[0] += lhs
# pair[1] == rhs
# return pair
#
# def print_tree(l, depth = 0):
# for el in l:
# if isinstance(el, list):
# print_tree(el, depth + 1)
# else:
# print((" " * depth * 2) + str(el))
#
# def traverse(number, depth = 1):
# pass
#
#
#
##answer1 =
##print(f"Answer 1 = {answer1}")
#
##answer2 =
##print(f"Answer 2 = {answer2}")
#
# class SnailNumber():
#
# def __init__(self, l):
# depth = 0
# cur = l.pop(0)
# while not isinstance(cur, int):
# cur = cur.pop(0)
# depth += 1
# self.head = Node(cur, depth)
#
# while l:
# cur = l.pop(0)
#
#
#
# def extend(self, other):
# cur = self.head
# other_head = other.head
## Increase depth of each element by 1 before joining
# while other_head is not None:
# other_head.depth += 1
# other_head = other_head.next
# other_head.depth += 1
# while cur.next is not None:
# cur.depth += 1
# cur = cur.next
# cur.depth += 1
# cur.next = other.head
#
# class Node():
# def __init__(self, val, depth, next = None):
# self.val = val
# self.depth = depth
# self.next = next
# def join(self, other):
# self.next = other
# def __repr__(self):
# return f'Val = {self.val}\nDepth = {self.depth}'
