from math import floor, sqrt
from random import randrange, getrandbits
import sys


def is_prime_v1(n):
    '''
    Test if a number is prime

    Args:
        n -- int -- the number to test
    return True if n is prime
    '''

    # 1 is not prime nor composite
    if n == 1:
        return False

    # n is composite if divided with no remainder.
    for value in range(2, n):
        '''
        if n = 6
        value = [ 2, 3, 4, 5 ]
        6 / 2 = 3 ; divisible, thus composite
        6 / 3 = 2 ; divisible, thus composite
        6 / 4 = 1.5
        6 / 5 = 1.2
        '''
        if n % value == 0:
            return False

    # n passed tests and is prime
    return True


def is_prime_v2(n):
    '''
    Test if a number is prime

    Args:
        n -- int -- the number to test
    return True if n is prime
    '''
    # 1 is not a prime nor composite
    if n == 1:
        return False

    # Even numbers, except for 2, are not prime
    if n > 2 and n % 2 == 0:
        return False

    max_divider = floor(sqrt(n))
    for value in range(3, 1 + max_divider, 2):
        if n % value == 0:
            return False
    return True


def is_prime_v3(n, k=128):
    '''
    From this guide on how to efficiently generate prime numbers:
    https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb

    Test if a number is prime
    Args:
        n -- int -- the number to test
        k -- int -- the number of tests to do
    return True if n is prime
    '''
    # 1 is not a prime nor composite
    if n == 1:
        return False

    # Even numbers, except for 2, are not prime
    if n > 2 and n % 2 == 0:
        return False

    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True


def generate_prime_candidate(length):
    '''
    Generate an odd integer randomly

    Args:
        length -- int -- the length of the number to generate, in bits
    return a integer
    '''
    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p


def generate_prime_number(length=2048):
    '''
    Generate a prime

    Args:
        length -- int -- length of the prime to generate, in          bits
    return a prime
    '''
    p = 4
    # keep generating while the primality test fails
    while not is_prime_v3(p):
        p = generate_prime_candidate(length)
    return p


def iterative_egcd(a, b):
    '''
    Simple Euclidean Example.
    Note that the quotient and remainder become the next a and b.
    To find the gcd(2024, 748).
    Formula: a = b * q + r

    2024 = 748 * 2 + 528
    748 = 528 * 1 + 220
    528 = 220 * 2 + 88
    220 = 88 * 2 + 44
    88 = 44 * 2 + 0 <- GCD = 44

    Performs a Iterative Extended Euclidean Algorithm
    https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm

    Args:
        a   --  The output of phi(n) -- phi_n = (prime1 - 1) * (prime2 - 1)
        b   --  The public exponent (e)
    returns
        b   --  Always 1
        y0  --  a*y0 + b*x0 = b = 1
        x0  --  a*y0 + b*x0 = b = 1
    '''
    assert a > b, 'a must be larger than b'
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, y0, x0


def recursive_egcd(a, b):
    '''
    Recursive Extended Euclidean Algorithm
    https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm

    Args:
        a   --  The output of phi(n) -- phi_n = (prime1 - 1) * (prime2 - 1)
        b   --  The public exponent (e)
    returns
        g   --  Always 1
        new_x  --  a * new_x + b * old_x = g = 1
        old_x  --  a * new_x + b * old_x = g = 1
    '''
    # set limit on recursive operations
    sys.setrecursionlimit(1000000)
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = recursive_egcd(b % a, a)
        old_x = x
        new_x = y - (b // a) * x
        return g, new_x, old_x
