#!/usr/bin/python
import argparse
from asym.rsa import gen_rsa_v3 as gen_rsa


def pylihim():
    # Main ArgParse Parser
    parser = argparse.ArgumentParser(prog='PyLihim', add_help=True)
    subparsers = parser.add_subparsers(dest='cmd')

    # Main options
    parser.add_argument("--test", help="Test Function", action="store_true")

    # Argparse RSA Sub Parser
    parser_cert = subparsers.add_parser('rsa')
    parser_cert.add_argument("--gen-key", help="Generate a RSA keypair with the specified bit size")

    # Parse argument list
    args = parser.parse_args()

    # Command list
    if args.test:
        pass

    # RSA subparser
    if args.cmd == 'rsa':
        if args.gen_key:
            keysize = int(args.gen_key)
            print(gen_rsa(keysize))


# Run application
if __name__ == '__main__':
    pylihim()
