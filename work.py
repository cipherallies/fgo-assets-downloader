#!/usr/bin/env python3
from argparse import ArgumentParser
from termcolor import colored
from tempfile import mkstemp
from urllib import parse
import os

# Initialize arg parser & parse
parser = ArgumentParser(
  description='Download F/GO assets from a server. Developed to work with Atlas Academy\'s directory structure.'
)
parser.add_argument(
  '-a', '--asset-storage',
  help='AssetStorage file (decrypted if encrypted before).',
  metavar='file.txt', dest='asset_storage'
)
parser.add_argument(
  '-b', '--base-url',
  help='Base URL of files.',
  metavar='https://example.com/path/to/assets/folder', dest='base_url'
)
args = parser.parse_args()

# Declare constants
asset_path : str = args.asset_storage
base_url : str = args.base_url

# Read file
files = []
print('Loading asset declaration...', end='')
with open(asset_path, "r") as f:
  for lines in f.readlines():
    l = list(lines.strip().split(","))
    if (l[0] == '1'): files.append(l[1:])

# tabular output
_____ = 0
for _ in files:
  b_s = str(_[1])
  if len(b_s) > _____: _____ = len(b_s)
  print(
    colored(' ' * (_____ - len(b_s)) + b_s, 'yellow')
    + colored('B', 'cyan')
    + ' | '
    + colored(_[3], 'green')
  )

# create temp file
fd, filename = mkstemp()
print(colored(f"Writing URLs to {colored(filename, 'green')}."))

with os.fdopen(fd, 'w') as f:
  for _ in files:
    b = parse.urljoin(base_url, _[-1])
    print(b, file=f)

print(f"""Now execute {colored(
  f"aria2c --dir=./ --input-file={filename} --max-concurrent-downloads=4 --human-readable=true --download-result=full --file-allocation=none",
  "green"
)}.""")