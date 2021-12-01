from collections import Counter

output_jolts = sorted(list(map(int, open("input.txt"))))
output_jolts.insert(0, 0)
output_jolts.append(max(output_jolts) + 3)
diffs = []
for i in range(len(output_jolts) - 1):
    diffs.append(output_jolts[i + 1] - output_jolts[i])
print("answer 1:", Counter(diffs)[1] * Counter(diffs)[3])


def fib3(term):
    if term <= 2:
        return max(1, term)
    else:
        return fib3(term - 1) + fib3(term - 2) + fib3(term - 3)


last = 0
variations = []
for diff in diffs:
    if last == 1:
        variations[-1] += 1
    else:
        variations.append(0)
    last = diff
count = 1
for variation in variations:
    count *= fib3(variation)
print("answer 2:", count)
