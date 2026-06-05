# Task 01: A Cash Register System $\textendash$ return a change to a customer.

## Problem Statement

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
| Time complexity | $O(k)$ | $O(n \cdot k)$ | 
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
* **DP** scales linearly: sum $\times 10$ $\rightarrow$  time $\times 10$ $\rightarrow$ confirms $O(n \cdot k)$.
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


# Task 02: Computation of a Definite Integral Using the Monte Carlo Method

## Problem Statement
Computet the value of the defiinte integral

$$
\int_0^2 x^2 \, dx
$$

using the Monte Carlo method and compare the result with the analytical solution and the result obtained using `scipy.integrate.quad`.

## Monte Carlo Method $\textemdash$ Algorithm
The idea behind the Monte Carlo method is the geometric interpretation of an integral as the area under a curve:
1. Construct a bounding rectangle with base `[a, b]` and height `f(b)` (the maximum value of the function on the interval).
2. Randomly generate `N` points inside the rectangle: $(x_i, y_i)$.
3. Count the fraction of points that fall below the curve $(y_i \le f(x_i))$.
4. Multiply the area of the rectangle by this fraction:

$$
I \approx (b-a) \cdot f_{\max} \cdot \frac{|\lbrace y_i \leq f(x_i) \rbrace|}{N}
$$

```python
N = 1_000_000                               # number of random points

x_random = np.random.uniform(a, b, N)       # uniformly distributed on [0, 2]
y_random = np.random.uniform(0, f(b), N)    # uniformly distributed on [0, f(2)=4]

under_curve = y_random <= f(x_random)       # boolean mask

area_rectangle = (b - a) * f(b)             # 2 * 4 = 8
monte_carlo_result = area_rectangle * np.sum(under_curve) / N 
```
### Results

| Method | Value | Absolute Error | Relative Error |
| --- | --- | --- | --- |
| Monte Carlo (N = 1,000,000) | 2.667240 | 0.000573 | 0.0215% |
| scipy.quad | 2.666667 | $\approx 3 \times 10^{-14}$ | $\approx 0$% | 
| Analytical Solution $(\frac{x^3}{3})$ | 2.666667 | $\textemdash$ | $\textemdash$ |

### Alalytical Solution 

$$
\int_{0}^{2} x^2 \ dx = \left[\frac{x^3}{3}\right]_{0}^{2} = \frac{8}{3}
$$

Therefore, $8 / 3 \approx 2.666667$

<img width="744" height="623" alt="image" src="https://github.com/user-attachments/assets/c089c1c8-2175-460e-878c-85efd39e9fcc" />

### Convergence Analysis

The theoretical error of the Monte Carlo method decreases as $O(\frac{1}{\sqrt{N}})$ 

| N | Expected Relative Error |
| --- | --- |
| 100 | $\sim 10$% |
| 10,000 | $\sim 1$% | 
| 1,000,000 | $\sim 0.1$% |

The convergence plot clearly shows that as the number of sampled points increases, the estimate stabilizes around the exact value:


<img width="728" height="620" alt="image" src="https://github.com/user-attachments/assets/efce1c7c-476b-4118-a689-634bc5a625f0" />

## Conclusions
* The Monte Carlo method demonstrated its correctness: with **N = 1,000,000**, it produced a value of **2.667240**, which differs from the exact value **8/3 ≈ 2.666667** by only 0.0215%, well within the expected statistical error of approximately **1/√N ≈ 0.1%**
* Agreement with `scipy.quad`: the `quad` function returns **2.666667** with a numerical error on the order of **3×10⁻¹⁴**, which is essentially machine precision. The Monte Carlo method produces a comparable result, although with greater statistical variance.
* Practical accuracy: for most engineering applications, an error below **0.1%** is acceptable. If higher precision is required, it is advisable to increase **N** or use deterministic numerical integration methods such as `quad`, the trapezoidal rule, or similar techniques.
* Advantages of the Monte Carlo method: the algorithm scales naturally to multidimensional integrals, where classical grid-based methods suffer from the **curse** of **dimensionality**. The Monte Carlo error remains **O(1/√N)** regardless of the number of dimensions.
* Disadvantage: slow convergence. To reduce the error by a factor of two, the number of samples **N** must be increased by a factor of four.

# Files
| File | Description | 
| --- | --- |
| `cash_register.py` | Completed solution to Task 01: A Cash Register System $\textendash$ return a change to a customer. | 
| `monte_carlo.py` | Completed solution to Task 02: Computation of a Definite Integral Using the Monte Carlo Method | 
| `README.md` | This document containing the analysis and conclusions | 
| `requirements.txt` | Python packages and versions required for the `monte_carlo.py` project | 
| `.gitignore` | ignored and not track files | 
