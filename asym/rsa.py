from base64 import b64encode
from pyasn1.codec.der.encoder import encode as der_encoder
from asn1 import pkcs1
from util.crypto import recursive_egcd as egcd
from util.crypto import generate_prime_number
import math


def gen_private_key(size):
    '''
    Generates a RSA private key using the specified bit size.

    Args:
        size -- int -- the bitsize of the keypair
    return a UTF-8 formatted private key
    '''
    # check that size is an int
    if isinstance(size, int) is False:
        raise TypeError("Bit size must be an integer")
    # prime 1
    p = generate_prime_number(size)
    # prime 2
    q = generate_prime_number(size)
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
    # Build ASN.1 using new primitives
    asn1_key = pkcs1.RSAPrivateKey()
    asn1_key['version'] = 0
    asn1_key['modulus'] = n
    asn1_key['publicExponent'] = e
    asn1_key['privateExponent'] = d
    asn1_key['prime1'] = p
    asn1_key['prime2'] = q
    asn1_key['exponent1'] = 0
    asn1_key['exponent2'] = 0
    asn1_key['coefficient'] = 0
    der = der_encoder(asn1_key)
    b64 = b'-----BEGIN RSA PRIVATE KEY-----\n'
    b64 += b64encode(der)
    b64 += b'\n-----END RSA PRIVATE KEY-----'
    return str(b64, 'utf-8')
