# Purpose: String concatenation inside loop → list accumulation cure
def concat_in_loop(strings):
    result = ""
    for s in strings:
        result += s
    return result
