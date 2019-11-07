from base64 import b64encode, b64decode
from pyasn1.codec.der.encoder import encode as der_encoder
from asn1 import pkcs1
from util.crypto import is_prime_v3 as is_prime
from util.crypto import generate_prime_number, egcd
import math


def gen_rsa():
    asn1_key = pkcs1.RSAPrivateKey()
    asn1_key['version'] = 0
    asn1_key['modulus'] = 22535825661165800725868572364451265589142895093190544211019790997410746344984952964662993823177710976693754073427594820232776250347282356107925406399269502417422584322036232808395557063323920944435545075393071613311899970806619942129910400707753439107594145133600617846373503806020860647783963396429628765528060988032151484401718700316964422645847859427392734067322259401910675669300226174713257018563337901829206660625692532836535012265438873274414275158231226456115980026413894857223585804211478198463343224076173629831024734285540655496537018251005520831848983637953336165087260153651412753135474360477826171988183
    asn1_key['publicExponent'] = 65537
    asn1_key['privateExponent'] = 11605071642563507769616223640506366821306797175642578643784532803936940635013765927711237599194723099202549799717837215436104271983313734780145178152325349605346518734217324885950557018632513052989230675029994871258423670823391617360305569578802368378811889529790610673318268763437417428354379673560027789001577694523691566476297269370748384826706501581344408997040221409388995203157448849434240211488204432794540192676196878806842664421714021767929271980621425716032941614645883386787760852846636292933504542271552503651268892523371672604010187243881615815526226500451815779782274891536977293245838830369052700202449
    asn1_key['prime1'] = 150970044329794516179259747467430651791284988190128364042635115061642217647199100140388347687660943141275113153660351436347080560535563007326862059369058482272523126416970980503697535597452797663290880509143945778060236168394998216818454561107763727306660635118398872463832251335521271839120150795355079754959
    asn1_key['prime2'] = 149273491712940229043125337912740715859768781655166299474326633374068900723229888126698392043638856461027621209923234576162102844614950771849607599618149568804762580193455343729000153025118981943698460878631911325084874741513510921337111160866690829922562234808902424639459501277079046336724608038078463913337
    asn1_key['exponent1'] = 4485079822239497123777693948747844409076275569619908216595367029693415898791471199068253245462499905336872992510745140097468084461643669610531462068626224346317386012997886675323849150987085112996129581019931678744576038266400072144674474426305994736806204992226110512948126910756670526126721296344909597371
    asn1_key['exponent2'] = 53858446145599961181527102862271189819797863970246766214045921735252349459106976740526880666858177821344570717760117258768773118448588216597583369708268073057317484340974488576162131596380112715575839692633629479423180007290972721454099676668962133822861995579463611898998418713059968104707113259203249426961
    asn1_key['coefficient'] = 129397642324742632140599585803777112136531526689224890542770950417738565668979600723360914982534740630511612243730947027035926391884916885393046619539447369966617426681637395860676661139377635609534704428624409254497201029032428163306359889188261500303305116724626845679239724607679503608334720234259596537197
    print(asn1_key)
    der = der_encoder(asn1_key)
    print(der)
    b64 = b'-----BEGIN RSA PRIVATE KEY-----\n'
    b64 += b64encode(der)
    b64 += b'\n-----END RSA PRIVATE KEY-----'
    print(str(b64, 'utf-8'))


def gen_rsa_v2(size):
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
    return(e, n, d)


def gen_rsa_v3(size):
    '''
    Generates an RSA key pair using the specified bit size.
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
    print(asn1_key)
    der = der_encoder(asn1_key)
    print(der)
    b64 = b'-----BEGIN RSA PRIVATE KEY-----\n'
    b64 += b64encode(der)
    b64 += b'\n-----END RSA PRIVATE KEY-----'
    print(str(b64, 'utf-8'))