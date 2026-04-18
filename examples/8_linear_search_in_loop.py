# Purpose: Repeated membership → hash table cure
def linear_search_in_loop(A, B):
    found = 0
    for a in A:
        for b in B:
            if a == b:
                found += 1
    return found
