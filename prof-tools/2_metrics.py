#!/usr/bin/env python
import pandas as pd
import sys
import os

graphs = [
        ('citeseer'	        , 3703	    , 6   ),  
        ('cora' 	        , 1433	    , 7   ),  
        ('pubmed'	        , 500	    , 3   ),      

        ('PROTEINS_full'             , 29       , 2) ,   
        ('OVCAR-8H'                  , 66       , 2) ,   
        ('Yeast'                     , 74       , 2) ,
        ('DD'                        , 89       , 2) ,
        ('TWITTER-Real-Graph-Partial', 1323     , 2) ,   
        ('SW-620H'                   , 66       , 2) ,

        ( 'amazon0505'               , 96	  , 22	),
        ( 'artist_edges'             , 100	  , 12	),
        ( 'com-amazon'               , 96	  , 22	),
        ( 'web-BerkStan'             , 100	  , 12	),
        ( 'wiki-topcats'             , 300	  , 12	),
        ( 'soc-BlogCatalog'	         , 128	  , 39  ), 
] 

metrics = [
    'atomic_transactions',
    'atomic_transactions_per_request',
    'global_atomic_requests',
    
    'dram_utilization',
    'sm_efficiency',
    
    'dram_read_bytes',
    'dram_read_throughput',
    'dram_write_bytes',
    'dram_write_throughput',

    'flop_count_sp',
    'flop_count_sp_add',
    'flop_count_sp_fma',
    'flop_count_sp_mul',
    'flop_count_sp_special',

    'flop_sp_efficiency',
    'gld_efficiency',
    'branch_efficiency',
    'tex_cache_hit_rate',
    'l2_tex_hit_rate',
    'global_hit_rate',
    'local_hit_rate',
]

# extract the time information of the directory
def extrat_metric(dir):
    files = sorted(os.listdir(dir))
    data = []
    f = []

    header = "data," + ",".join(metrics)
    print(header)
    
    for fname, _, _ in graphs:
        abs_path = os.path.join(dir, fname + ".csv")
        if not os.path.exists(abs_path): continue
        curr_csv = pd.read_csv(abs_path, header=4)
        local = [fname]
        for met in metrics:
            fun = getattr(curr_csv, met)
            tmp_data = fun.tolist()
            if "utilization" not in met:
                max_val = []
                for i in tmp_data[1:]:
                    try:
                        tmp = float(i)
                    except ValueError:
                        continue
                    max_val.append(float(i))
                local.append("{:.3f}".format(sum(max_val)/len(max_val)))
            else:
                max_val = []
                for i in tmp_data[1:]:
                    try:
                        tmp = float(i.split('(')[1].rstrip(')'))
                    except IndexError:
                        continue
                    max_val.append(tmp)
                local.append("{:.3f}".format(sum(max_val)/len(max_val)))
        output_line = ",".join(local)
        print(output_line)


if __name__ == "__main__":
    extrat_metric(sys.argv[1])
    # files, data = extrat_metric(sys.argv[1])
    # ans = []
    # for f, m in zip(files, data):
    #     tmp = []
    #     for i in m:
    #         tmp.append(i)
    #     ans.append((f, tmp))
    
    # header = "Filename"
    # for met in metrics:
    #     header += "," + met
    
    # print(header)
    # for item in sorted(ans):
    #     tmp = [str(i) for i in item[1]]
    #     print("{},{}".format(item[0], ",".join(tmp)))

    # key=lambda x: int(x[0].split("_")[-1].rstrip('.csv'))