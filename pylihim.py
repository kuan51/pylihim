#!/usr/bin/python
import argparse
from asym.rsa import gen_private_key as gen_rsa_private_key
from asym.rsa import gen_public_key as gen_rsa_public_key



def pylihim():
    # Main ArgParse Parser
    parser = argparse.ArgumentParser(prog='PyLihim', add_help=True)
    subparsers = parser.add_subparsers(dest='cmd')

    # Main options
    parser.add_argument("--test", help="Test Function", action="store_true")

    # Argparse RSA Sub Parser
    parser_cert = subparsers.add_parser('rsa')
    parser_cert.add_argument("--gen-priv-key", help="Generate a RSA keypair with the specified bit size")
    parser_cert.add_argument("--gen-pub-key", help="Generate a RSA public key from a private key")

    # Parse argument list
    args = parser.parse_args()

    # Command list
    if args.test:
        pass

    # RSA subparser
    if args.cmd == 'rsa':

        # If --gen-priv-key
        if args.gen_priv_key:
            print(gen_rsa_private_key(args.gen_priv_key))

        # If --gen-pub-key
        if args.gen_pub_key:
            print(gen_rsa_public_key(args.gen_pub_key))


# Run application
if __name__ == '__main__':
    pylihim()
