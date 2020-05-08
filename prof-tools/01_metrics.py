#!/usr/bin/env python
import pandas as pd
import sys
import os

metrics = [
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
def extrat_time(dir):
    files = sorted(os.listdir(dir))
    data = []
    f = []
    for fname in files:
        if not '.csv' in fname:
            continue

        f.append(fname)
        curr_csv = pd.read_csv(dir + "/" + fname, header=5)

        local = []
        for met in metrics:
            fun = getattr(curr_csv, met)
            tmp_data = fun.tolist()
            if "utilization" not in met:
                max_val = []
                for i in tmp_data[1:]:
                    max_val.append(float(i))
                local.append(sum(max_val)/len(max_val))
            else:
                max_val = []
                for i in tmp_data[1:]:
                    max_val.append(float(i.split('(')[1].rstrip(')')))
                local.append(sum(max_val)/len(max_val))        
        data.append(local)
    return f, data


if __name__ == "__main__":
    files, data = extrat_time(sys.argv[1])
    ans = []
    for f, m in zip(files, data):
        tmp = []
        for i in m:
            tmp.append(i)
        ans.append((f, tmp))
    
    header = "Filename"
    for met in metrics:
        header += "," + met
    
    print(header)
    for item in sorted(ans):
        tmp = [str(i) for i in item[1]]
        print("{},{}".format(item[0], ",".join(tmp)))

    # key=lambda x: int(x[0].split("_")[-1].rstrip('.csv'))