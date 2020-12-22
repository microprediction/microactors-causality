# Testing 1,2,3 
import datetime as datetime
with open('timestamp.txt','a') as f:
   f.write(str(datetime.now())+'\n')


import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import sklearn
import tigramite
from tigramite import data_processing as pp
from tigramite import plotting as tp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests import ParCorr, GPDC, CMIknn, CMIsymb
from tigramite.models import LinearMediation, Prediction
from microprediction import MicroReader


mr = MicroReader()
z3s = [ name for name in mr.get_stream_names() if 'z3~' in name]
z2s = [ name for name in mr.get_stream_names() if 'z3~' in name]

# Group greedily using z-streams as a hint  
groups = dict()
unique_parents = set()
for zstream in z3s+z2s:
   parents = [ n+'.json' for n in zstream.split('~')[1:-1] ]
   if not any([ p in unique_parents for p in parents ]):
      groups[parents[0]]=parents
with open('groups.csv','w') as f:
   for group in groups:
      f.write( ','.join([parents[0],len(parents),parents]) )
    
     

