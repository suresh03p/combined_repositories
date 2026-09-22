import numpy as np

np.random.seed(1)
numbers = np.random.randint(1, 101, size=100)
print("Original numbers:", numbers)

# Primes
is_prime = np.ones_like(numbers, dtype=bool)
for i, num in enumerate(numbers):
    if num < 2:
        is_prime[i] = False
    else:
        for d in range(2, int(np.sqrt(num)) + 1):
            if num % d == 0:
                is_prime[i] = False
                break
primes = numbers[is_prime]

# Even and odd
evens = numbers[numbers % 2 == 0]
odds = numbers[numbers % 2 != 0]

avg = numbers.mean()
greater_than_avg = numbers[numbers > avg]
less_than_avg = numbers[numbers < avg]

ascending = np.sort(numbers)
descending = ascending[::-1]
unique = np.unique(numbers)

# Frequency
values, counts = np.unique(numbers, return_counts=True)
frequency = dict(zip(values, counts))

print("Primes:", primes)
print("Even numbers:", evens)
print("Odd numbers:", odds)
print("Greater than average:", greater_than_avg)
print("Less than average:", less_than_avg)
print("Sorted ascending:", ascending)
print("Sorted descending:", descending)
print("Unique values:", unique)
print("Frequency count:", frequency)
