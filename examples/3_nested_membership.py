# Purpose: if x in list inside loop → hash table cure
def nested_membership(A, B):
    count = 0
    for a in A:
        if a in B:
            count += 1
    return count
