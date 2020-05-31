#!/usr/bin/env python
import os
import collections 
import threading

if not os.path.exists('orig-metis-naive'):
    os.mkdir('orig-metis-naive')

if not os.path.exists('orig-metis-Sort'):
    os.mkdir('orig-metis-Sort')

if not os.path.exists('orig-metis-BFS'):
    os.mkdir('orig-metis-BFS')

def metis_navie(gr):

    out_degree = collections.defaultdict(int)
    fnodes = open("orig/{}.el".format(gr))
    for line in fnodes:
        tmp = line.rstrip("\n").split() 
        src, trg = int(tmp[0]), int(tmp[1])
        out_degree[src] += 1

    fnodes.seek(0)
        
    nid = 0
    fp = open("orig_metis_part/{}.part".format(gr))
    graphs = collections.defaultdict(list)
    for line in fp:
        subg_id = int(line.rstrip("\n"))
        graphs[subg_id].append(nid)
        nid += 1
    fp.close()
    
    mapping1 = {}
    cnt = 0
    for subgid in sorted(graphs.keys()):
        for nid in sorted(graphs[subgid]):
            mapping1[nid] = cnt
            cnt += 1

    new_edges = []
    for line in fnodes:
        tmp = line.rstrip("\n").split() 
        src, trg = int(tmp[0]), int(tmp[1])
        new_src, new_trg = mapping1[src], mapping1[trg]
        new_edges.append((new_src, new_trg))
    
    fout = open("orig-metis-naive/{}".format(gr), "w")
    new_edges.sort(key=lambda x: x[0])
    for edge in new_edges:
        fout.write("{} {}\n".format(edge[0], edge[1]))
    fout.close()


def metis_sort(gr):

    out_degree = collections.defaultdict(int)
    fnodes = open("orig/{}.el".format(gr))
    for line in fnodes:
        tmp = line.rstrip("\n").split() 
        src, trg = int(tmp[0]), int(tmp[1])
        out_degree[src] += 1

    fnodes.seek(0)
        
    nid = 0
    fp = open("orig_metis_part/{}.part".format(gr))
    graphs = collections.defaultdict(list)
    for line in fp:
        subg_id = int(line.rstrip("\n"))
        graphs[subg_id].append(nid)
        nid += 1
    fp.close()
    
    mapping1 = {}
    cnt = 0
    for subgid in sorted(graphs.keys()):
        for nid in sorted(graphs[subgid]):
            mapping1[nid] = cnt
            cnt += 1
        
    fout = open("orig-metis-Sort/{}".format(gr), "w")
    mapping = collections.defaultdict()
    for gid in graphs.keys():
        old_nids = sorted(graphs[gid])
        new_nids = sorted(old_nids, key=lambda x: out_degree[x])
        for old, new in zip(old_nids, new_nids):
            mapping[mapping1[new]] = mapping1[old] 
    
    # for key in sorted(mapping.keys()):
    #     print(key, mapping[key])
    new_edges = []
    for line in fnodes:
        tmp = line.rstrip("\n").split() 
        src, trg = int(tmp[0]), int(tmp[1])
        new_src, new_trg = mapping[mapping1[src]], mapping[mapping1[trg]]
        new_edges.append((new_src, new_trg))
    
    new_edges.sort(key=lambda x: x[0])
    for edge in new_edges:
        fout.write("{} {}\n".format(edge[0], edge[1]))

    fout.close()

def RCM_algo(graph, point_set):

    start_vid = min(point_set, key=lambda x: len(graph[x]))
    que = [start_vid]
    unvisited = set(point_set)
    unvisited.remove(start_vid)

    schedule = []
    while len(que) or len(unvisited):
        curr_id = que.pop(0)
        schedule.append(curr_id)

        tmp = []
        for nb in graph[curr_id]:
            if nb in unvisited:
                unvisited.remove(nb)
                tmp.append(nb)
        que += sorted(tmp, key=lambda x: len(graph[x]))

        if len(que) == 0:
            if len(unvisited):
                que.append(unvisited.pop())
            else:
                break

    schedule_lookup = {}
    for idx, nid in enumerate(schedule):
        schedule_lookup[nid] = idx        
    
    return schedule, schedule_lookup


def metis_BFS(gr):

    nid = 0
    fp = open("orig_metis_part/{}.part".format(gr))
    graph_nid2cluster = collections.defaultdict()
    for line in fp:
        subg_id = int(line.rstrip("\n"))
        graph_nid2cluster[nid] = subg_id
        nid += 1
    fp.close()

    fnodes = open("orig/{}.el".format(gr))
    graphs = collections.defaultdict(dict)
    for line in fnodes:
        tmp = line.rstrip("\n").split() 
        src, trg = int(tmp[0]), int(tmp[1])
        src_cid = graph_nid2cluster[src]
        trg_cid = graph_nid2cluster[trg]

        if src_cid == trg_cid:
            if src not in graphs[src_cid]:
                graphs[src_cid][src] = [trg]
            else:
                graphs[src_cid][src].append(trg)
        else:
            if src not in graphs[src_cid]:
                graphs[src_cid][src] = []

        if trg not in graphs[trg_cid]:
            graphs[trg_cid][trg] = []

    # print(graphs[1449].keys())
    fnodes.seek(0)
    
    mapping1 = {}
    cnt = 0
    for subgid in sorted(graphs.keys()):
        for nid in sorted(graphs[subgid]):
            mapping1[nid] = cnt
            cnt += 1

    fout = open("orig-metis-BFS/{}".format(gr), "w")
    mapping = collections.defaultdict()
    for sub_gid in graphs.keys():
        old_nids = sorted(graphs[sub_gid].keys())
        new_nids, _ = RCM_algo(graphs[sub_gid], graphs[sub_gid].keys())
        assert set(old_nids) == set(new_nids)
        for old, new in zip(old_nids, new_nids):
            mapping[mapping1[new]] = mapping1[old]

    assert set(mapping.keys()) == set(mapping.values())

    new_edges = []
    for line in fnodes:
        tmp = line.rstrip("\n").split() 
        src, trg = int(tmp[0]), int(tmp[1])
        new_src, new_trg = mapping[mapping1[src]], mapping[mapping1[trg]]
        new_edges.append((new_src, new_trg))

    new_edges.sort(key=lambda x: x[0])
    for edge in new_edges:
        fout.write("{} {}\n".format(edge[0], edge[1]))
    fout.close()

if __name__ == "__main__":

    # method_func = metis_navie
    method_func = metis_sort
    # method_func = metis_BFS

    parallel = 2
    parallel = min(5, parallel)

    graphs = [
        # 'ENZYMES'                   ,
        # 'PROTEINS_full'             ,

        # 'YeastH'                    ,
        # 'OVCAR-8H'                  ,
        # 'SW-620H'                   ,
        # 'Yeast'                     ,
        # 'DD'                        ,
        # 'COLLAB'                    ,
        # 'TWITTER-Real-Graph-Partial',
       
        # 'Reddit'                    ,
        'amazon0505'                ,
        'artist_edges'              ,
        'com-amazon'                ,
        'web-BerkStan'              ,
        'wiki-topcats'              ,

        # 'amazon_also_bought'        ,
        # 'amazon_also_viewed'        ,
        # 'enwiki-2013'               ,

        # 'ppi'               ,
        # 'amazon0601'        ,
        # 'ms_academic'       ,
        # 'enwiki-2013'       ,
        # 'soc-BlogCatalog'   ,
        # 'cora'              ,
        # 'NELL'              ,
        # 'citeseer'          ,
        # 'pubmed'            ,
    ]

    for idx in range(0, len(graphs), parallel):
        print("=> " + graphs[idx])
        t1 = threading.Thread(target=method_func, args=(graphs[idx],))
        t1.start() 

        if parallel >= 2:
            if idx + 1 < len(graphs):
                print("=> "+ graphs[idx + 1]) 
                t2 = threading.Thread(target=method_func, args=(graphs[idx + 1],)) 
                t2.start()
        
        if parallel >= 3:
            if idx + 2 < len(graphs):
                print("=> "+ graphs[idx + 2]) 
                t3 = threading.Thread(target=method_func, args=(graphs[idx + 2],)) 
                t3.start()

        if parallel >= 4:
            if idx + 3 < len(graphs):
                print("=> "+ graphs[idx + 3]) 
                t4 = threading.Thread(target=method_func, args=(graphs[idx + 3],)) 
                t4.start()
        
        if parallel >= 5:
            if idx + 4 < len(graphs):
                print("=> "+ graphs[idx + 4]) 
                t5 = threading.Thread(target=method_func, args=(graphs[idx + 4],)) 
                t5.start()    
    
        t1.join()

        if parallel >= 2:
            if idx + 1 < len(graphs):
                t2.join()
        
        if parallel >= 3:
            if idx + 2 < len(graphs):
                t3.join()

        if parallel >= 4:
            if idx + 3 < len(graphs):
                t4.join()
        
        if parallel >= 5:
            if idx + 4 < len(graphs):
                t5.join()
            
        print("-----------------------------") 
  
    print("Done!!!") 