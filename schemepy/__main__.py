#!/usr/bin/env python
"""
Scheme interpreter.
"""
import argparse
import logging
import sys
from schemepy import repl


def main():
    """
    Program entry point.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=logging_level)
    repl.repl()


if __name__ == "__main__":
    main()
