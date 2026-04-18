# Purpose: Test empirical scaling via if __name__ == "__main__"
def square_numbers(n):
    result = []
    for i in range(n):
        result.append(i * i)
    return result


if __name__ == "__main__":
    square_numbers(10000)
