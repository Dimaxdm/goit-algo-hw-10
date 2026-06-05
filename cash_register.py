"""
Касова система: видача решти покупцеві
"""
import time
import random
from typing import Callable

# Variables
COINS_DENOMINATIONS = [50, 25, 10, 5, 2, 1]
BENCHMARK_REPETITION = 10

# 1. Greedy algorithm O(k)
def find_coins_greedy(amount: int) -> dict[int, int]:
    """
    Return dictionary {denomination of the coin: quantity}
    Complexity:
        Time  - O(k), k - available coin's denomination 
        Space - O(k)
    """
    if amount < 0:
        raise ValueError("Quantity can not be negative.")
    result: dict[int, int] = {}
    for coin in sorted(COINS_DENOMINATIONS, reverse=True):
        if amount == 0:
            break
        count = amount // coin
        if count:
            result[coin] = count
            amount -= coin * count
    return result

# Dynamic programming O(n*k)
def find_min_coins(amount: int) -> dict[int, int]:
    """
    Return dictionary {denomination of the coin: quantity} with mininum coins quantity.
    Complexity:
        Time  - O(n * k), where n = sum, k = denominations
        Space - O(n) 
    """
    if amount < 0:
        raise ValueError("Quantity can not be negative.")
    if amount == 0:
        return {}

    INF = float("inf")
    dp = [INF] * (amount + 1)
    dp[0] = 0
    last_coin = [0] * (amount + 1)

    for i in range(1, amount + 1):
        for coin in COINS_DENOMINATIONS:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                last_coin[i] = coin

    if dp[amount] == INF:
        return {}

    result: dict[int, int] = {}
    remaining = amount
    while remaining > 0:
        coin = last_coin[remaining]
        result[coin] = result.get(coin, 0) + 1
        remaining -= coin

    return dict(sorted(result.items()))

# 3. Benchmark
def benchmark(func: Callable, amount: int, repeats: int = BENCHMARK_REPETITION) -> float:
    """Return average time in microseconds"""
    times = []
    for _ in range(repeats):
        t_start = time.perf_counter()
        func(amount)
        times.append(time.perf_counter() - t_start)
    return (sum(times) / len(times)) * 1_000_000


def run_benchmarks():
    TEST_AMOUNTS = [113, 1_000, 10_000, 100_000, 1_000_000]

    header = f"{'T':>12} | {'Greedy (μs)':>15} | {'DP (μs)':>15} | {'DP/Greedy':>10}"
    print(header)
    print("-" * len(header))

    for amount in TEST_AMOUNTS:
        g_time = benchmark(find_coins_greedy, amount)
        dp_time = benchmark(find_min_coins, amount)
        ratio = dp_time / g_time if g_time > 0 else float("inf")
        print(f"{amount:>12,} | {g_time:>15.2f} | {dp_time:>15.2f} | {ratio:>10.1f}x")


# Demonstration
def demo():
    TEST_CASES = [0, 1, 113, 877, 10_001]

    print("\n", "~" * 5, " DEMO / BENCHMARK ", "~" * 5, "\n")
    for amount in TEST_CASES:
        g = find_coins_greedy(amount)
        dp = find_min_coins(amount)
        g_total = sum(v for v in g.values())
        dp_total = sum(v for v in dp.values())
        print(f"Total {amount:>6}:")
        print(f"  Greedy [{g_total:>3} coins]: {g}")
        print(f"  DP     [{dp_total:>3} coins]: {dp}")
        assert sum(k * v for k, v in g.items()) == amount, "Greedy: quantity is not matching!"
        assert sum(k * v for k, v in dp.items()) == amount, "DP: quantity is not matching!"
        print()


if __name__ == "__main__":
    demo()
    print(f"\n~~~ Benchmark (average running time, test repetitions quantity: \"{BENCHMARK_REPETITION}\") ~~~\n")
    run_benchmarks()
