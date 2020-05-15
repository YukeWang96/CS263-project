#!/usr/bin/env python3
import subprocess
import datetime
import os

run_gcn = False
overall = True

if run_gcn:
	hidden = [16] # [16, 32, 64, 128, 256, 512, 1024, 2048]
else:
	hidden = [64] # [16, 32, 64, 128, 256, 512, 1024, 2048] # 64

data_dir = '/home/yuke/.graphs/orig/'
# data_dir = '/home/yuke/.graphs/rabbit-new-orders/'
print(data_dir)

if not os.path.exists("results"):
	os.mkdir("results")

if not os.path.exists("results/archived"):
	os.mkdir("results/archived")

if not os.path.exists("logs/"):
	os.mkdir("logs/")

if not os.path.exists("logs/archived"):
	os.mkdir("logs/archived")

if not os.path.exists("logs/overall"):
	os.mkdir("logs/overall")

if not os.path.exists("logs/metrics"):
	os.mkdir("logs/metrics")

dataset = [
		# ('toy'	        , 3	    , 2   ),  
		# ('citeseer'	        , 3703	    , 6   ),  
		# ('cora' 	        , 1433	    , 7   ),  
		# ('pubmed'	        , 500	    , 3   ),      
		# ('ppi'	            , 50	    , 121 ),   

		# ('ENZYMES'                   , 18       , 6) ,
		('PROTEINS_full'             , 29       , 2) ,   
		# ('YeastH'                    , 75       , 2) ,   
		('OVCAR-8H'                  , 66       , 2) ,   
		# ('SW-620H'                   , 66       , 2) ,
		('Yeast'                     , 74       , 2) ,
		('DD'                        , 89       , 2) ,
		('COLLAB'                    , 100      , 3) ,
		('TWITTER-Real-Graph-Partial', 1323     , 2) ,   

		# ( 'Reddit'                   , 602    , 41),
		# ( 'amazon0505'               , 96	  , 22),
		# ( 'artist_edges'             , 100	  , 12),
		# ( 'com-amazon'               , 96	  , 22),
		# ( 'web-BerkStan'             , 100	  , 12),
		# ( 'soc-BlogCatalog'	         , 128	  , 39),      
		# ( 'amazon0601'  	         , 96	  , 22), 
		
		# ( 'wiki-topcats'             , 300	  , 12),
		# ( 'Reddit'                   , 602    , 41),
		# ( 'enwiki-2013'	             , 100	  , 12),      
		# ( 'amazon_also_bought'       , 96     , 22),
]


os.system("mv results/*_* results/archived")
x = datetime.datetime.now()
result_timestmp= "{}_{}_{}-{}".format(x.month, x.day, x.hour, x.minute)

# if not os.path.exists("results/{}".format(result_timestmp)):
	# os.mkdir("results/{}".format(result_timestmp))

x = datetime.datetime.now()
day_time = "{}_{}_{}-{}-{}".format(x.month, x.day, x.hour, x.minute, x.second)

if overall:
	os.system("mv logs/overall/* logs/archived/overall")
	if not os.path.exists("logs/overall/{}".format(day_time)):
		os.mkdir("logs/overall/{}".format(day_time))
else:
	os.system("mv logs/metrics/* logs/archived/metrics")
	if not os.path.exists("logs/metrics/{}".format(day_time)):
		os.mkdir("logs/metrics/{}".format(day_time))

for hid in hidden:
	print("### hidden: {}".format(hid))
	for data, d, c in dataset:
		print("=> {}".format(data))
		if overall:
			common = [
						'nvprof', 
						'--log-file', 
						'logs/overall/{}/{}.csv'.format(day_time, data), 
						'--csv', '--print-gpu-trace']
		else:
			common = [
						'sudo',
						'nvprof', 
						'--metrics', 'all', 
						'--log-file', 'logs/metrics/{}/{}.csv'.format(day_time,data), 
						'--csv', '--print-gpu-trace']

		if run_gcn:
			sample = [
						"./pr-gcn"	, 
						"--input"	, os.path.join(data_dir, data), 
						"--embed"	, os.path.join(data_dir, data),
						'--ebdSize' , str(d), 
						'--hidden'	, str(hid),
						'--class'	, str(c) ]
		else:
			sample = [  
						"./pr-gin"  , 
						"--input"	, os.path.join(data_dir, data), 
						"--embed"	, os.path.join(data_dir, data), 
						'--ebdSize' , str(d), 
						'--hidden'	, str(hid),
						'--class'	, str(c)
					]
					
		subprocess.run(common + sample)

if overall:
	os.system('./1_latency.py logs/overall/{} {} > results/{}.csv'\
			.format(day_time, 1, result_timestmp))
else:
	os.system('./2_metrics.py logs/metrics/{} {} > results/met_{}.csv'\
			.format(day_time, 1, result_timestmp))