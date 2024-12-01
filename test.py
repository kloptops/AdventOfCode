import collections

def permutations(amount, size):
    stack = collections.deque((
        (i, [amount - i])
        for i in range(amount + 1)))

    while len(stack) > 0:
        i, items = stack.popleft()
        if i == 0:
            while len(items) < size:
                items.append(0)

            yield items
            continue

        if len(items) == size-1:
            items.append(i)
            yield items
            continue

        for j in range(i + 1):
            temp = items[:]
            temp.append(amount - j - sum(temp))
            stack.append((j, temp))


for items in permutations(3, 4):
    print(items)
