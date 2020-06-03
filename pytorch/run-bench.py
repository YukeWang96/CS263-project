#!/usr/bin/env python3
import subprocess
import datetime
import os

overall = True
hidden = 16
data_dir = "/graphs/" # graph data directory
# print(data_dir)
iteration = 1

dataset = [
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

x = datetime.datetime.now()
result_timestmp= "{}_{}_{}-{}".format(x.month, 
                                      x.day, 
                                      x.hour, 
                                      x.minute, 
                                      x.second)

# if not os.path.exists("prof-results/{}".format(result_timestmp)):
#     os.mkdir("prof-results/{}".format(result_timestmp))

if overall:
    # os.system("mv logs/overall/* logs/archived/overall")
    if not os.path.exists("logs/overall/{}".format(result_timestmp)):
        os.mkdir("logs/overall/{}".format(result_timestmp))
else:
    # os.system("mv logs/metrics/* logs/archived/metrics")
    if not os.path.exists("logs/metrics/{}".format(result_timestmp)):
        os.mkdir("logs/metrics/{}".format(result_timestmp))

for data, d, c in dataset:

    print("=> {}".format(data))

    if overall:
        common = [
                    'nvprof', 
                    '--log-file', 
                    'logs/overall/{}/{}.csv'.format(result_timestmp, data), 
                    '--csv', '--print-gpu-trace'
                    ]
    else:
        common = [
                    'nvprof', 
                    '--metrics', 'all', 
                    '--log-file', 'logs/metrics/{}/{}.csv'.format(result_timestmp, data), 
                    '--csv', '--print-gpu-trace'
                    ]
    
    sample = [	
                'python', 
                'custom_kernel/main.py',
                '--graph_path', data_dir + "{}".format(data),
                '--feature', str(d),
                '--hidden', str(hidden),
                '--classes', str(c),
                '--kernel', 'auto',
                '--gpu'
                ]

    subprocess.run(common + sample)

if overall:
    os.system('../prof-tools/1_latency.py logs/overall/{} {} > prof-results/overall_{}.csv'.format(result_timestmp, iteration, result_timestmp))
else:
    os.system('../prof-tools/2_metrics.py logs/metrics/{} {} > prof-results/metrics_{}.csv'.format(result_timestmp, iteration, result_timestmp))