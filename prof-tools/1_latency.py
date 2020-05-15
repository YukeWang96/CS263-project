#!/usr/bin/env python
import pandas as pd
import sys
import os

graphs = [
        ('citeseer'	        , 3703	    , 6   ),  
        ('cora' 	        , 1433	    , 7   ),  
        ('pubmed'	        , 500	    , 3   ),      
        ('ppi'	            , 50	    , 121 ),   

        ('ENZYMES'                   , 18       , 6) ,
        ('PROTEINS_full'             , 29       , 2) ,   
        ('YeastH'                    , 75       , 2) ,   
        ('OVCAR-8H'                  , 66       , 2) ,   
        ('SW-620H'                   , 66       , 2) ,
        ('Yeast'                     , 74       , 2) ,
        ('DD'                        , 89       , 2) ,
        ('COLLAB'                    , 100      , 3) ,
        ('TWITTER-Real-Graph-Partial', 1323     , 2) ,   

        ( 'Reddit'                   , 602    , 41),
        ( 'amazon0505'               , 96	  , 22),
        ( 'artist_edges'             , 100	  , 12),
        ( 'com-amazon'               , 96	  , 22),
        ( 'web-BerkStan'             , 100	  , 12),
        ( 'wiki-topcats'             , 300	  , 12),
        ( 'soc-BlogCatalog'	         , 128	  , 39),      
        ( 'amazon0601'  	         , 96	  , 22), 
        
        ( 'Reddit'                   , 602    , 41),
        ( 'enwiki-2013'	             , 100	  , 12),      
        ( 'amazon_also_bought'       , 96     , 22),
] 


# extract the time information of the directory
def extrat_time(dir):
    files = sorted(os.listdir(dir))
    mem_times = []
    cpt_times = []
    f = []

    for fname in files:
        if not '.csv' in fname:
            continue

        # print(fname)
        f.append(fname)
        curr_csv = pd.read_csv(dir + "/" + fname, header=3)
        duration = curr_csv.Duration.tolist()
        cuda_type = curr_csv.Name.tolist()

        use_s = False
        use_us = False
        use_ms = False
        mem_time = 0
        cpt_time = 0

        for tpe, time in zip(cuda_type, duration):
            if "ms" in str(time):
                use_ms = True
                continue
            elif "us" in str(time):
                use_us = True
                continue
            elif "s" in str(time):
                use_s = True
                continue

            if "memcpy" in str(tpe) or  "memset" in str(tpe):
                mem_time += float(time)
            else:
                cpt_time += float(time)

        if use_us:
            mem_times.append(mem_time/1e3)
            cpt_times.append(cpt_time/1e3)
        elif use_ms:
            mem_times.append(mem_time)
            cpt_times.append(cpt_time)
        elif use_s:
            mem_times.append(mem_time * 1e3)
            cpt_times.append(cpt_time * 1e3)
        else:
            print("error")
    
    return f, mem_times, cpt_times


if __name__ == "__main__":
    files, mem_time, cpt_time = extrat_time(sys.argv[1])
    ans = []
    for f, m, c in zip(files, mem_time, cpt_time):
        ans.append((f, m, c))
    
    iteration = int(sys.argv[2])
    print("Filename, Mem(ms), Compute(ms)")
    for gr, _, _ in graphs:
        for item in sorted(ans):
            if gr + ".csv" == item[0]:
                print("{}, {:3f}, {:3f}".format(item[0], float(item[1])/iteration, float(item[2])/iteration))

    # for gr, mem_time, cpt_time in sorted(ans, key=lambda x: int(x[0].strip('.csv').split('h')[1])):
    #     print("{}, {:3f}, {:3f}".format(gr, mem_time, cpt_time))