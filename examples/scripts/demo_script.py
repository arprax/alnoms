def lengthOfLongestSubstring(s: str) -> int:
    seen = {}
    left = 0
    output = 0

    for r in range(len(s)):
        """
        If s[r] not in seen, we can keep increasing the window size
        """
        if s[r] not in seen:
            output = max(output, r - left + 1)
        else:
            if seen[s[r]] < left:
                output = max(output, r - left + 1)
            else:
                left = seen[s[r]] + 1

        seen[s[r]] = r

    return output


# -------------------------------------------------
# 🔬 EMPIRICAL ANALYSIS GENERATOR (REQUIRED BY ALNOMS)
# -------------------------------------------------
def data_gen(n):
    return (periodic_string(n),)


# -------------------------------------------------
# TEST INPUT DISTRIBUTIONS
# -------------------------------------------------
def best_case_string(n):
    return "".join(chr((i % 26) + 97) for i in range(n))


def worst_case_string(n):
    return "a" * n


def periodic_string(n, period=26):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return "".join(alphabet[i % period] for i in range(n))


# -------------------------------------------------
# LOCAL VALIDATION RUN
# -------------------------------------------------
if __name__ == "__main__":
    print("\n=== BEST CASE ===")
    for n in [100, 200, 400, 800, 1600]:
        s = best_case_string(n)
        print(n, lengthOfLongestSubstring(s))

    print("\n=== WORST CASE ===")
    for n in [100, 200, 400, 800, 1600]:
        s = worst_case_string(n)
        print(n, lengthOfLongestSubstring(s))

    print("\n=== PERIODIC CASE ===")
    for n in [100, 200, 400, 800, 1600]:
        s = periodic_string(n)
        print(n, lengthOfLongestSubstring(s))
