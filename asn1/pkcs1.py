from pyasn1.type.namedtype import NamedType, NamedTypes
from pyasn1.type.univ import Sequence, Integer


class Version(Integer):
    pass


class RSAPrivateKey(Sequence):
    '''
    Example ASN1 for PKCS1 Private Key
    RSAPrivateKey ::= SEQUENCE {
      version           Version,
      modulus           INTEGER,  -- n
      publicExponent    INTEGER,  -- e
      privateExponent   INTEGER,  -- d
      prime1            INTEGER,  -- p
      prime2            INTEGER,  -- q
      exponent1         INTEGER,  -- d mod (p-1)
      exponent2         INTEGER,  -- d mod (q-1)
      coefficient       INTEGER,  -- (inverse of q) mod p
      otherPrimeInfos   OtherPrimeInfos OPTIONAL
    }
    '''
    componentType = NamedTypes(
        NamedType('version', Version()),
        NamedType('modulus', Integer()),
        NamedType('publicExponent', Integer()),
        NamedType('privateExponent', Integer()),
        NamedType('prime1', Integer()),
        NamedType('prime2', Integer()),
        NamedType('exponent1', Integer()),
        NamedType('exponent2', Integer()),
        NamedType('coefficient', Integer())
    )
