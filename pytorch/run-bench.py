#!/usr/bin/env python3
import subprocess
import datetime
import os

overall = True
hidden = 16

dataset = [
        ('toy',         100,            10),
        # ('ENZYMES'                   , 18       , 6) ,
        # ('PROTEINS_full'             , 29       , 2) ,   
        # ('YeastH'                    , 75       , 2) ,   
        # ('OVCAR-8H'                  , 66       , 2) ,   
        # ('SW-620H'                   , 66       , 2) ,
        # ('Yeast'                     , 74       , 2) ,
        # ('DD'                        , 89       , 2) ,
        # ('COLLAB'                    , 100      , 3) ,
        # ('TWITTER-Real-Graph-Partial', 1323     , 2) ,   

        # ( 'Reddit'                   , 602    , 41	),
        # ( 'amazon0505'               , 96	  , 22	),
        # ( 'artist_edges'             , 100	  , 12	),
        # ( 'com-amazon'               , 96	  , 22	),
        # ( 'web-BerkStan'             , 100	  , 12	),
        # ( 'wiki-topcats'             , 300	  , 12	),
        # ( 'soc-BlogCatalog'	         , 128	  , 39  ),      
        # ( 'NELL'	                 , 5414	  , 210 ),      
        # ('amazon0601'  	    , 96	    , 22  ), 
     
        # ('citeseer'	        , 3703	    , 6   ),  
        # ('cora' 	        , 1433	    , 7   ),  
        # ('pubmed'	        , 500	    , 3   ),      
        # ('ppi'	            , 50	    , 121 ),    

        # ('ms_academic'	    , 500	    , 25  ),  
		# ('enwiki-2013'	           , 100	, 12),
        # ( 'amazon_also_bought'       , 96     , 22),
        # ( 'amazon_also_viewed'       , 96     , 22),     
]

# x = datetime.datetime.now()
# result_timestmp= "{}_{}_{}-{}".format(x.month, x.day, x.hour, x.minute, x.second)
# if not os.path.exists("results/{}".format(result_timestmp)):
#     os.mkdir("results/{}".format(result_timestmp))

# data_dir = "/home/yuke/.graphs/orig/"
data_dir = "/graphs/orig/"
print(data_dir)
x = datetime.datetime.now()
day_time = "{}_{}_{}-{}-{}".format(x.month, x.day, x.hour, x.minute, x.second)

# if overall:
#     os.system("mv logs/overall/* logs/archived/overall")
#     if not os.path.exists("logs/overall/{}".format(day_time)):
#         os.mkdir("logs/overall/{}".format(day_time))
# else:
#     os.system("mv logs/metrics/* logs/archived/metrics")
#     if not os.path.exists("logs/metrics/{}".format(day_time)):
#         os.mkdir("logs/metrics/{}".format(day_time))

for data, d, c in dataset:

    print("=> {}".format(data))

    if overall:
        common = [
                    # 'nvprof', 
                    # '--log-file', 
                    # 'logs/overall/{}/{}.csv'.format(day_time, data), 
                    # '--csv', '--print-gpu-trace'
                    ]
    else:
        common = [
                    # 'nvprof', 
                    # '--metrics', 'all', 
                    # '--log-file', 'logs/metrics/{}/{}.csv'.format(day_time, data), 
                    # '--csv', '--print-gpu-trace'
                    ]
    
    sample = [	
                'python', 
                'custom_kernel/main.py',
                '--graph_path', data_dir + "{}".format(data),
                '--feature', str(d),
                '--hidden', str(hidden),
                '--classes', str(c),
                # '--kernel', 'SAG',
                '--gpu'
                ]

    subprocess.run(common + sample)

# if overall:
#     os.system('./1_latency.py logs/overall/{} {} > results/{}/trans_{}_med_{}.csv'\
#             .format(day_time, iteration, result_timestmp, trans_val, trans_method))