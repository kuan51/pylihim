from base64 import b64encode, b64decode
from pyasn1.codec.der.encoder import encode as der_encoder
from pyasn1.codec.der.decoder import decode as der_decoder
from asn1 import pkcs1
from util.crypto import recursive_egcd as egcd
from util.crypto import generate_prime_number
from pathlib import Path
import math
import os
import errno


def gen_private_key(size):
    '''
    Generates a RSA private key using the specified bit size.

    Args:
        size -- int -- the bitsize of the keypair
    return a UTF-8 formatted private key
    '''
    # check that size is an int
    size = int(size)
    if isinstance(size, int) is False:
        raise TypeError("Bit size must be an integer")
    # prime 1
    p = generate_prime_number(size)
    # prime 2
    q = generate_prime_number(size)
    # If q > p, swap primes
    if not p > q:
        p, q = q, p
    # modulus
    n = q * p
    # Calc phi(n)
    phi = (p - 1) * (q - 1)
    # public exponent
    e = 65537
    # Generate private exponent
    # e * d = 1 (mod z)
    # (e * d) / z = soemthing with the remainder of 1
    while True:
        if math.gcd(e, phi) == 1:
            gcd, s, t = egcd(phi, e)
            if gcd == (s*phi + t*e):
                d = t % phi
                break
    # Calculate the CRT exponents for better efficiency
    # https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Using_the_Chinese_remainder_algorithm
    exp1 = d % (p - 1)  # d mod (p-1) OR (1/e) mod (p-1)
    exp2 = d % (q - 1)  # d mod (q-1) OR (1/e) mod (q-1)
    # p must be greater than q
    if not p > q:
        raise ValueError('The prime p must be greater than the prime q.')
    qInv = (1 / q) % p  # (1/q) mod p  where p > q
    # Build ASN.1 using new primitives
    asn1_key = pkcs1.RSAPrivateKey()
    asn1_key['version'] = 0
    asn1_key['modulus'] = n
    asn1_key['publicExponent'] = e
    asn1_key['privateExponent'] = d
    asn1_key['prime1'] = p
    asn1_key['prime2'] = q
    asn1_key['exponent1'] = exp1
    asn1_key['exponent2'] = exp2
    asn1_key['coefficient'] = qInv
    der = der_encoder(asn1_key)
    b64 = b'-----BEGIN RSA PRIVATE KEY-----\n'
    b64 += b64encode(der)
    b64 += b'\n-----END RSA PRIVATE KEY-----'
    return str(b64, 'utf-8')


def gen_public_key(key):
    '''
    Accepts a PEM encoded PKCS1 private key and generates a PKCS1 public key

    Args:
        key -- str -- a PEM encoded PKCS1 private key
    return a UTF-8 formatted public key
    '''
    # Test that filepath exists
    if not Path(key).is_file():
        raise FileNotFoundError('Cannot find file ' + str(Path(key).absolute()))
    # Open the private key file
    with open(key, 'r') as f:
        key_string = f.read()
        key_string = key_string.replace('-----BEGIN RSA PRIVATE KEY-----\n', '')
        key_string = key_string.replace('\n-----END RSA PRIVATE KEY-----', '')
    # Test if private key is a string
    if isinstance(key_string, str) is False:
        raise TypeError("Private key file must be a string.")
    # base64 decode to get der
    der = b64decode(key_string)
    # Instantiate a RSAPrivateKey object
    asn1_priv = pkcs1.RSAPrivateKey()
    private_key, rest_of_input = der_decoder(der, asn1Spec=asn1_priv)
    # Instantiate a RSAPublicKey object
    asn1_pub = pkcs1.RSAPublicKey()
    asn1_pub['modulus'] = private_key['modulus']
    asn1_pub['publicExponent'] = private_key['publicExponent']
    # der encode the public key
    der = der_encoder(asn1_pub)
    b64 = b'-----BEGIN RSA PRIVATE KEY-----\n'
    b64 += b64encode(der)
    b64 += b'\n-----END RSA PRIVATE KEY-----'
    return str(b64, 'utf-8')
