#!/usr/bin/env python3
import io
import os
import sys

def rewrite_paths(path: str) -> bool:
    if not os.path.isfile(path):
        return False
    with io.open(path, 'r', encoding='utf-8', errors='ignore') as f:
        s = f.read()

    # Markdown: ](/docs/... -> ](./docs/...
    s = s.replace('](/docs/', '](./docs/')
    # Markdown escaped (embedded JSON): ](\/docs\/ -> ](./docs/
    s = s.replace('](\\/docs\\/', '](./docs/')

    # HTML attributes
    s = s.replace('src="/docs/', 'src="./docs/')
    s = s.replace("src='/docs/", "src='./docs/")
    s = s.replace('href="/docs/', 'href="./docs/')
    s = s.replace("href='/docs/", "href='./docs/")

    # Generic occurrences in embedded JSON: \/docs\/ -> \.\/docs\/
    s = s.replace('\\/docs\\/', '\\./docs\\/')

    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f"Rewrote /docs -> ./docs in {path}")
    return True


def main(argv):
    if len(argv) < 2:
        print("Usage: fix_asset_paths.py <index.html>", file=sys.stderr)
        return 2
    path = argv[1]
    ok = rewrite_paths(path)
    return 0 if ok else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

