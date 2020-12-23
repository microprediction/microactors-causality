# We'll use microprediction.org histories and the tigramite causality library
# Assuming we can get the thing to install
import numpy as np
from microprediction import MicroReader

mr = MicroReader()



# Define some obviously related streams
# This belongs somewhere else, probably 
GROUP_DEFINITIONS = [ dict(start='sox',end='salad'),
               dict(start='sox',end='shake'),
               dict(start='sox',middle='oopah'),
               dict(start='traffic-nj511-minutes-'),
               dict(start='hospital-er-wait-times-'),
               dict(start='emojitracker-twitter-),
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
                        
def condition_match(cond:dict, name:str)->bool:
   """ Does condition match a stream name, after .json is removed? """
   for k,v in cond:
      if k=='start' and not name[:len(v)]==v:
         return False
      if k=='end':
         n_ = name.replace('.json','')
         if not n_[-len(v):]==v:
            return False
      if k=='middle' and not v in name:
         return False
   return True  

DEFINED_LIST_OF_LISTS = [ [n for n in ALL_NAMES if condition_match(cond=cond,name=n) ] for cond in GROUP_DEFINITIONS ]
                    
def greedy_groups(lists_of_parents:[[str]])->dict:
   """
       Takes a list of list of parents and creates some groups
       returns: dict of set 
   """
   # I'm sure this could be more elegant :)
   unique_parents = set()
   groups = dict()
   for ps in lists_of_parents:
      if not any([ p in unique_parents for p in ps ]):
         first_parent = ps[0] # Arbitrary key
         groups[first_parent]=set(ps)
      else:
         for p in ps:
            if p in groups:
               for p1 in ps: 
                  groups[p].add(p1)
   return groups
   
                    
def zlists(names:[str])->dict:
   """ 
       returns: dict of sets of stream names   
       names: list of all stream names
   """
   # To make interesting causality plots with smaller groups (as a start) we 
   # take a hint from the existence of z2 and z3 streams. If this is completely. 
   # new, either don't worry or see https://www.microprediction.com/knowledge-center 
   z3s = [ name for name in names if 'z3~' in name]
   z2s = [ name for name in names if 'z3~' in name]
   zs = z3s + z2s 
   list_of_lists = [ [ n+'.json' for n in zstream.split('~')[1:-1] ] for zstream in zs ]
   return list_of_lists
                    
Z_LIST_OF_LISTS = zlists(ALL_NAMES)

GROUPS = greedy_groups(Z_LIST_OF_LISTS+DEFINED_LISTS_OF_LISTS)
        
   
with open('z_groups.csv','w') as f:
   for k,s in GROUPS.items():
      f.write( ','.join([k,len(s)]+list(s) ) )
    
     

