#!/usr/bin/env python
import pandas as pd
import sys
import os

# extract the time information of the directory
def extrat_time(dir):
    files = sorted(os.listdir(dir))
    mem_time = []
    f = []
    for fname in files:
        if not '.csv' in fname:
            continue

        # print(fname)
        f.append(fname)
        curr_csv = pd.read_csv(dir + "/" + fname, header=4)

        dram_read_bytes = float(curr_csv.dram_read_bytes.tolist()[1])
        dram_write_bytes = float(curr_csv.dram_write_bytes.tolist()[1])
        dram_read_throughput = float(curr_csv.dram_read_throughput.tolist()[1])
        dram_write_throughput = float(curr_csv.dram_write_throughput.tolist()[1])
        
        read_time = dram_read_bytes/dram_read_throughput/1e9 if dram_read_throughput else 0
        write_time = dram_write_bytes/dram_write_throughput/1e9 if dram_write_throughput else 0
        
        mem_time.append(read_time + write_time)

    return f, mem_time


if __name__ == "__main__":
    files, mem_time = extrat_time(sys.argv[1])
    ans = []
    for f, m in zip(files, mem_time):
        ans.append((f, m))
    
    print("Filename, Mem(ms)")
    for item in sorted(ans, key=lambda x: int(x[0].split("_")[-1].rstrip('.csv'))):
        print("{}, {:3f}".format(item[0], item[1] * 1e3))

        # key=lambda x: int(x[0].split("_")[-1].rstrip('.csv'))