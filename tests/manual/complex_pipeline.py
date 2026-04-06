import random
import string


def generate_users(n):
    users = []
    for i in range(n):
        users.append(
            {
                "id": i,
                "name": "".join(random.choices(string.ascii_lowercase, k=5)),
                "age": random.randint(18, 70),
            }
        )
    return users


def generate_transactions(n, user_count):
    txs = []
    for i in range(n):
        txs.append(
            {
                "tx_id": i,
                "user_id": random.randint(0, user_count - 1),
                "amount": random.randint(10, 500),
            }
        )
    return txs


# ❌ INTENTIONALLY INEFFICIENT FUNCTION
def process_transactions(users, transactions):
    result = []

    for tx in transactions:  # O(N)
        for user in users:  # O(N)
            if user["id"] == tx["user_id"]:
                if user["age"] > 30:
                    result.append(
                        {
                            "tx_id": tx["tx_id"],
                            "user": user["name"],
                            "amount": tx["amount"],
                        }
                    )
    return result


# ❌ ANOTHER INEFFICIENT PATTERN
def find_high_spenders(transactions):
    output = []

    for t1 in transactions:
        total = 0
        for t2 in transactions:
            if t1["user_id"] == t2["user_id"]:
                total += t2["amount"]

        if total > 1000:
            output.append(t1["user_id"])

    return list(set(output))


def data_gen(n):
    u = generate_users(n)
    t = generate_transactions(n, n)
    # This dictionary "pins" the empirical test to the bottleneck
    return {"target": "process_transactions", "args": (u, t)}


# DRIVER
def run_pipeline():
    users = generate_users(2000)
    transactions = generate_transactions(4000, 2000)

    processed = process_transactions(users, transactions)
    high_spenders = find_high_spenders(transactions)

    return processed, high_spenders


if __name__ == "__main__":
    run_pipeline()
