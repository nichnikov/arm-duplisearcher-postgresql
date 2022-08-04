from itertools import groupby

l = [("a", "1"), ("a", "2"), ("b", "3"), ("a", "4"), ("c", "5"), ("a", "6"), ("c", "7"), ("b", "8"), ("c", "9")]

print(sorted(l, key=lambda x: x[0]))
it = groupby(sorted(l, key=lambda x: x[0]), key=lambda x: x[0])

result = []
for k, v in it:
    result.append({k: [x[1] for x in v]})

print(result)