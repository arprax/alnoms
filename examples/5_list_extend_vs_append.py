# Purpose: Inefficient list building → extend vs append


def build_list(chunks):
    result = []
    for chunk in chunks:
        for item in chunk:
            result.append(item)
    return result
