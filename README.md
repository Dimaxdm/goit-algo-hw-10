# Task 01: A Cash Register System $\textendash$ return a change to a customer.

## Problem statement

Use a set of coin denominations: `[50, 25, 10, 5, 2, 1]`. 
You need to implement two functions for the cash register system:

| Function | Method |
| --- | --- |
| `find_coins_greedy` | Greedy Algorithm (should always choose the largest available coin denomination first). |
| `find_min_coins` | Dynamic Programming (use dynamic programming approach to find the minimum number of coins required to make up the amount. |

## Implementation 

### 01.1. Greedy Algorithm Function $\textendash$ `find_coins_greedy`
```python
def find_coins_greedy(amount: int) -> dict[int, int]:
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
```
#### The principle:
- is that at every stage, we choose the largest denomination that does not exceed the remaining amount.

#### Example for the sum 113:
```
113 // 50 = 2 -> leftover: 13
 13 // 10 = 1 -> leftover: 3
  3 //  2 = 1 -> leftover: 1
  1 //  1 = 1 -> leftover: 0

Result: {50: 2, 10: 1, 2: 1, 1: 1} => 5 coins 
```

### 01.2. Dynamic Programming Function $\textendash$ `find_min_coins`

```python
def find_min_coins(amount: int) -> dict[int, int]:
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
```
#### The principle:
- build table `dp[i]` $\textendash$  the minimum number of coins required to make up the sum `i`. Each value is calculated using the already known optimal subproblems.

#### Example for the sum 113:
```
dp[0] = 0
dp[1] = dp[0] + 1 = 1  (coin 1)
dp[2] = dp[0] + 1 = 1  (coin 2)
...
dp[113] = 5  ->  {1: 1, 2: 1, 10: 1, 50: 2}
```

### The complexity of algorithms
| Description | Greedy | Dynamic Programming |
| --- | --- | --- |
| Time complexity | $O(k)$ | $O(n \times k)$ | 
| Space complexity | $O(k)$ | $O(n)$ |
| $k$ $\textendash$ number of denominations | 6 | 6 |
| $n$ $\textendash$ size of sum | $textemdash$ | depends of the sum |

> Greedy: $k = 6$ $\textendash$ effectively  $O(1)$ (constant), independent of the sum.
> DP: time and memory increase linearly as the sum increases.


### Banchmark result

Measurement: average time over 10 runs, Python `time.perf_counter()`

| Sum | Greedy $(\mu \text{s})$ | DP $(\mu \text{s})$ | Greedy advantage | 
| --- | --- | --- | --- |
| 113 | 3.61 | 205.53 | 56.9x | 
|1,000 | 0.98 | 725.31 | 740.1x |
| 10,000 | 1.14 | 6,177.10 | 5,418.5x |
| 100,000 | 1.07 | 73,956.00 | 69,117.2x |
| 1,000,000 | 1.05 | 717,536.26 | 683,362.7x |

### Key conclusion from the benchmark:

* **Greedy** runs in $\approx 1–2$ microseconds regardless of the sum $\rightarrow$ confirms $O(1) / O(k)$.
* **DP** scales linearly: sum $\times 10$ $\rightarrow$  time $\times 10$ $\rightarrow$ confirms $O(n \times k)$.
* For a sum of $1,000,000$, DP is $\approx 684,000$ times slower.

### When to Choose Each Algorithm

#### Choose the Greedy Algorithm when: 

* The coin system is **canonical** (each denomination is a multiple of a smaller one, or the set guarantees an optimal result).
  The set `[50, 25, 10, 5, 2, 1]` is such a system: the greedy algorithm always finds the optimal solution.
* Maximum speed is required $\textendash$ for example, in a real-time cash register or a high-load system.
* Amounts can be arbitrarily large $\textendash$ $O(k)$ does not depend on the amount itself.
* Memory is limited $\textendash$ no array of size n is needed.

#### Choose Dynamic Programming (DP) when:
* The coin system is arbitrary or **non-canonical**, for example `[1, 3, 4]`.
  For an amount of 6, the greedy algorithm returns:
  ```python
  {4: 1, 1: 2}  # 3 coins
  ```
  While DP returns:
  ```python
  {3: 2}        # 2 coins - which is optimal
  ```
* A guaranteed optimal solution is required regardless of the coin set.
* Amounts are moderate $(n \le 10,000–100,000)$ and sufficient CPU/RAM resources are available.

## Conclusions

For the given coin set `[50, 25, 10, 5, 2, 1]`, both algorithms produce the same optimal result.

This is confirmed by the fact that they return the same number of coins in all tested examples.

The greedy algorithm is clearly more efficient for practical use in a cash register system with this coin set because:

* Its execution time does not depend on the amount $(O(k) \approx O(1))$.
* It uses minimal memory.
* For amounts around $1,000,000$, it is more than $600,000$ times faster.

Dynamic programming is a more universal but computationally expensive approach. It should be used when the coin set does not guarantee the correctness of the greedy strategy or when the problem includes additional constraints (for example, a limited number of coins of each denomination).

## Code implementation: 

### See file `cash_register.py`.

Demo data: 
<img width="531" height="552" alt="image" src="https://github.com/user-attachments/assets/b4e19e6c-304b-4d9f-abac-e5299e3ea465" />


# Task 02

