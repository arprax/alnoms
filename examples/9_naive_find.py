# Purpose: Repeated scanning → hash table cure
def naive_find(items, targets):
    count = 0
    for t in targets:
        for item in items:
            if item == t:
                count += 1
    return count
