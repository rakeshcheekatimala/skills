#!/usr/bin/env python3
"""Check a brief's whitespace-token budget. Exit 0=pass, 1=over, 2=input error."""
import argparse
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('brief', type=Path)
    parser.add_argument('--max-words', type=int, default=80)
    args = parser.parse_args()
    if args.max_words < 1:
        parser.error('--max-words must be positive')
    try:
        content = args.brief.read_text(encoding='utf-8')
    except (OSError, UnicodeError) as exc:
        print(f'Input error: {exc}', file=sys.stderr)
        return 2
    count = len(content.split())
    if count == 0:
        print('Input error: the brief is empty', file=sys.stderr)
        return 2
    result = {'words': count, 'limit': args.max_words, 'within_limit': count <= args.max_words}
    print(json.dumps(result))
    return 0 if result['within_limit'] else 1


if __name__ == '__main__':
    sys.exit(main())
