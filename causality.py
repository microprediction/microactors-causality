# We'll use microprediction.org histories and the tigramite causality library

from microprediction import MicroReader
import json
from pprint import pprint
mr = MicroReader()

with open('data/groups.json') as f:
    groups = json.load(f)
pprint(groups)

