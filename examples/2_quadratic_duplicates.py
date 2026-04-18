# Purpose: Shallow nested loop → hash‑based cure
def find_duplicates(items):
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                return True
    return False
