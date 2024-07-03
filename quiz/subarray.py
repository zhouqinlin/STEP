import math, random

# Problem: L is an array of integers. K is an integer (1 <= K <= len(L)).
# Find a subarray of L such that 1) the length of the subarray is equal to or
# larger than K, and 2) the sum of the elements in the subarray is maximized.
#
# For example, if L is [2, -1, -1, -1, 4, -1, 3, 1] and K=3, the subarray
# [4, -1, 3, 1] maximizes the sum and the sum is 7.
#
# Input: L and K
# Output: The maximum sum


# O(N^3) algorithm
def solve_n3(L, K):
    N = len(L)
    max_sum = float("-inf")
    for k in range(K, N + 1):
        for i in range(0, N - k + 1):
            sum = 0
            for j in range(i, i + k):
                sum += L[j]
            max_sum = max(max_sum, sum)
    return max_sum


# O(N^2) algorithm
def solve_n2(L, K):
    n = len(L)
    # Calculate the prefix sum
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + L[i]
    max_sum = float("-inf")
    for left in range(n - K + 1):
        for right in range(left + K - 1, n):
            max_sum = max(max_sum, prefix_sum[right + 1] - prefix_sum[left])
            # print(left, right)
    return max_sum


# O(N) algorithm
# Transform this question into finding two numbers in the prefix sum array,
# with indices i and j, such that j - i >= K.
# Find the maximum value of prefix_sum[j] - prefix_sum[i].
# Use another array min_prefix_sum to keep track of the minimum value up to each index
# in the prefix_sum array.
# Since i is in the range of [0, j-K],
# and the minimum prefix sum in range [0, j-K] is min_prefix_sum[j-K], so
# max_sum = max(max_sum, prefix_sum[j] - min_prefix_sum[j-K]).
def solve_n(L, K):
    n = len(L)
    if n == 0 or K > n:
        return 0
    # Calculate the prefix sum
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + L[i]
    # Calculate the minimum prefix sum up to each index
    min_prefix_sum = [0] * (n + 1)
    for i in range(1, n + 1):
        min_prefix_sum[i] = min(min_prefix_sum[i - 1], prefix_sum[i])
    # Find the maximum subarray sum with length at least K
    max_sum = float("-inf")
    for i in range(K, n + 1):
        max_sum = max(max_sum, prefix_sum[i] - min_prefix_sum[i - K])
    return max_sum


# For a given L and K, run the three algorithms (O(N^3), O(N^2) and O(N))
# and check that all the answers are equal.
def check_answers(L, K):
    answer_n3 = solve_n3(L, K)
    answer_n2 = solve_n2(L, K)
    answer_n = solve_n(L, K)
    if answer_n3 != answer_n2:
        print(L, K)
        print(
            "Correct answer is %d but the O(N^2) algorithm answered %d"
            % (answer_n3, answer_n2)
        )
        exit(0)

    if answer_n3 != answer_n:
        print(L, K)
        print(
            "Correct answer is %d but the O(N) algorithm answered %d"
            % (answer_n3, answer_n)
        )
        exit(0)


# Run tests.
def run_tests():
    # Add your test cases here.
    check_answers([1, -1, -1, -1, 3, 2], 1)
    check_answers([1, -1, -1, -1, 3, 2], 2)
    check_answers([1, -1, -1, -1, 3, 2], 3)
    check_answers([1, -1, -1, -1, 3, 2], 4)
    check_answers([1, 0, -1, -2, 1, 3], 2)

    # Generate many test cases and run.

    for iteration in range(1000):
        length = random.randint(1, 30)
        L = [random.randint(-10, 10) for i in range(length)]
        for K in range(1, length + 1):
            check_answers(L, K)

    print("All tests pass!")


if __name__ == "__main__":
    run_tests()
