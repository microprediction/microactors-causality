# Testing 1,2,3 
from datetime import datetime
import json

with open('data/timestamp.txt', 'a') as f:
    f.write(str(datetime.now()) + '\n')

from microprediction import MicroReader

mr = MicroReader()
ALL_NAMES = mr.get_stream_names()

# Define some obviously related streams
# This belongs somewhere else, probably 
GROUP_DEFINITIONS = [dict(start='sox_unlimited', end='salad'),
                     dict(start='traffic-nj511-minutes-', middle='fort_lee'),
                     dict(start='traffic-nj511-minutes-', middle='alexander'),
                     dict(start='traffic-nj511-minutes-', middle='triborough'),
                     dict(start='traffic-nj511-minutes-', middle='gw_bridge'),
                     dict(start='traffic-nj511-minutes-', middle='nj_495'),
                     dict(start='traffic-nj511-minutes-', middle='exit_1'),
                     dict(start='traffic-nj511-minutes-', middle='exit_6'),
                     dict(start='traffic-nj511-minutes-', middle='exit_14'),
                     dict(start='traffic-nj511-minutes-', middle='exit_18'),
                     dict(start='traffic-nj511-minutes-', middle='295'),
                     dict(start='traffic-nj511-minutes-', middle='278'),
                     dict(start='traffic-nj511-minutes-', middle='87'),
                     dict(start='traffic-nj511-minutes-', middle='i-95'),
                     dict(start='hospital-er-wait-minutes-', middle='piedmont'),
                     dict(start='hospital-er-wait-minutes-', middle='columbus'),
                     dict(start='emojitracker-twitter-',middle='kissing_face',end='eyes'),
                     dict(start='emojitracker-twitter-', middle='smiling_face', end='eyes'),
                     dict(start='emojitracker-twitter-',middle='disappointed'),
                     dict(start='emojitracker-twitter-', middle='cat'),
                     dict(start='electricity-lbmp-nyiso'),
                     dict(start='electricity-load'),
                     dict(start='electricity-fueltype-nyiso'),
                     dict(start='pandemic_'),
                     dict(start='c5_'),
                     dict(start='copula_'),
                     dict(start='coin_'),
                     dict(start='three_body_'),
                     dict(start='helicopter'),
                     dict(start='traffic_')]


def condition_match(cond: dict, name: str) -> bool:
    """ Does condition match a stream name, after .json is removed? """
    for k, v in cond.items():
        if k == 'start' and not name[:len(v)] == v:
            return False
        if k == 'end':
            n_ = name.replace('.json', '')
            if not n_[-len(v):] == v:
                return False
        if k == 'middle' and not v in name:
            return False
    return True

DEFINED_LIST_OF_LISTS = [[n for n in ALL_NAMES if condition_match(cond=cond, name=n)] for cond in GROUP_DEFINITIONS]


def greedy_groups(lists_of_parents: [[str]]) -> dict:
    """
       Takes a list of list of parents and creates some groups
       returns: dict of set
    """
    # I'm sure this could be more elegant :)
    unique_parents = set()
    groups = dict()
    for ps in lists_of_parents:
        if len(ps):
            if not any([p in unique_parents for p in ps]):
                first_parent = ps[0]  # Arbitrary key
                groups[first_parent] = set(ps)
            else:
                for p in ps:
                    if p in groups:
                        for p1 in ps:
                            groups[p].add(p1)
            for p in ps:
                unique_parents.add(p)
    # Convert to sets
    return dict([ (k,list(g)) for k,g in groups.items()])


def zlists(names: [str]) -> dict:
    """
       returns: dict of sets of stream names   
       names: list of all stream names
   """
    # To make interesting causality plots with smaller groups (as a start) we
    # take a hint from the existence of z2 and z3 streams. If this is completely.
    # new, either don't worry or see https://www.microprediction.com/knowledge-center
    z3s = [name for name in names if 'z3~' in name]
    z2s = [name for name in names if 'z3~' in name]
    zs = z3s + z2s
    list_of_lists = [[n + '.json' for n in zstream.split('~')[1:-1]] for zstream in zs]
    return list_of_lists


Z_LIST_OF_LISTS = zlists(ALL_NAMES)

GROUPS = greedy_groups(Z_LIST_OF_LISTS + DEFINED_LIST_OF_LISTS)


with open('data/groups.json', 'w') as f:
    json.dump(GROUPS,f)

