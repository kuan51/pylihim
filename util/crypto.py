from math import floor, sqrt
from random import randrange, getrandbits


def is_prime_v1(n):
    '''
    Return 'True' if a number is likely prime. Return 'False' if a composite number.
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
    Return 'True' if a number is likely prime. Return 'False' if a composite number.
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
    """ Test if a number is prime
        Args:
            n -- int -- the number to test
            k -- int -- the number of tests to do
        return True if n is prime
    """
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
    """ Generate an odd integer randomly
        Args:
            length -- int -- the length of the number to generate, in bits
        return a integer
    """
    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p


def generate_prime_number(length=2048):
    """ Generate a prime
        Args:
            length -- int -- length of the prime to generate, in          bits
        return a prime
    """
    p = 4
    # keep generating while the primality test fails
    while not is_prime_v3(p):
        p = generate_prime_candidate(length)
    return p


def egcd(a, b):
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
    '''
    assert a > b, 'a must be larger than b'
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, y0, x0
