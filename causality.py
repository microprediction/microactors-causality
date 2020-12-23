# We'll use microprediction.org histories and the tigramite causality library

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
plt.style.use('ggplot')
plt.rcParams["figure.figsize"] = (14,10)
import tigramite
from tigramite import data_processing as pp
from tigramite import plotting as tp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests import ParCorr
import os
from microprediction import MicroReader
import json
import pandas as pd
mr = MicroReader()

with open('data/groups.json') as f:
    groups = json.load(f)

for k, names in groups.items():
    stem = k.replace('.json','')
    if len(names):
        columns = [n.replace('.json','') for n in names]
        df = pd.DataFrame(columns=columns)
        all_values = [ list(reversed(mr.get_lagged_values(name=name,count=1000)))[:1000] for name in names ]
        num = np.min([len(v) for v in all_values])
        for name, col, values in zip(names, columns, all_values):
            sigma = np.nanstd(values[-num:])
            if sigma>1e-4:
                df[col] = values[-num:]
            else:
                print('Dropping '+col+' as it appears to be constant.')
                del df[col]
        try:
            os.mkdir('data/'+stem)
        except Exception as e:
            pass
        df.to_csv('data/' + stem + '/chronological.csv')

        prefix = os.path.commonprefix(columns)
        var_names = [ col.replace(prefix,'') for col in columns]
        pp_frame = pp.DataFrame(data=df.values, var_names=var_names)
        parcorr = ParCorr()
        pcmci_parcorr = PCMCI(dataframe=pp_frame, cond_ind_test=parcorr, verbosity=0)
        try:
            all_parents = pcmci_parcorr.run_pc_stable(tau_max=2, pc_alpha=0.2)
            success=True
        except ValueError as e:
            print(e)
            success=False
        if success:
            results = pcmci_parcorr.run_pcmci(tau_max=2, pc_alpha=0.2)
            pcmci_parcorr.print_significant_links(p_matrix=results['p_matrix'],
                                                  val_matrix=results['val_matrix'], alpha_level=0.01)
            link_matrix = pcmci_parcorr.return_significant_links(pq_matrix=results['p_matrix'],
                                                                 val_matrix=results['val_matrix'], alpha_level=0.01)[
                'link_matrix']
            tp.plot_time_series_graph(
                val_matrix=results['val_matrix'],
                link_matrix=link_matrix,
                var_names=var_names,
                link_colorbar_label='MCI',
            )
            try:
                os.mkdir('gallery/' + stem)
            except Exception as e:
                pass
            plt.savefig('gallery/'+stem+'/causality.png')
            plt.close()
