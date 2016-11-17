import snap
from sets import Set
import matplotlib.pyplot as plt
import random
import collections
import numpy as np

DATA_SOURCE = "uniq-mal-dump.txt"


def calculate_degree_dist(graph):
    degmap = {}
    for node in graph.Nodes():
        deg = node.GetOutDeg()
        if not deg in degmap:
            degmap[deg] = 0
        degmap[deg] += 1
    for i in degmap:
        degmap[i] = degmap[i] /float(graph.GetNodes())
    return degmap


def get_x_y_deg(degmap):
    x = []
    y = []

    for item in degmap:
        x.append(item)
        y.append(degmap[item])
    
    return x,y

def plot_degree_dist(filename):
    graph1 = snap.LoadEdgeList(snap.PUNGraph, filename)

    graph1_deg = calculate_degree_dist(graph1)

    plt.xscale('log')
    plt.yscale('log')

    plt.xlabel('degree k')
    plt.ylabel('proportion of nodes with degree k')

    x,y = get_x_y_deg(graph1_deg)
    plt.scatter(x,y, color='red')

    plt.show()

def get_id_to_name(src, dst):
    with open(dst, 'w') as output:
        with open(src) as f:
            for line in f.readlines():
                split_line = line.split("|")
                output.write(split_line[0] + "," + split_line[1] + "\n")
    
def create_edge_list(filename):
    graph = snap.TUNGraph.New()
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            anime_id = int(line.split("|")[0])
            graph.AddNode(anime_id)

        # Add edges
        for line in lines:
            split_line = line.split("|")
            anime_id = int(split_line[0])
            recs = split_line[5].split(",")
            for i in recs:
                if not i or not i.isdigit():
                    break
                if graph.IsNode(int(i)):
                    graph.AddEdge(anime_id, int(i))
    snap.SaveEdgeList(graph, "mal-rec-graph")
                
def find_nonexistent_anime():
    anime_id_set = Set()
    rec_id_set = Set()
    with open(DATA_SOURCE) as f:
        for line in f.readlines():
            split_line = line.split("|")
            anime_id = int(split_line[0])
            anime_id_set.add(anime_id)
            recs = split_line[5].split(",")
            for i in recs:
                if not i or not i.isdigit():
                    break
                if int(i) < 35000:
                    rec_id_set.add(int(i))

    for i in rec_id_set:
        if i not in anime_id_set:
            print i

def get_dist_distribution(filename, sample_count):
    distance_dst = collections.defaultdict(int)
    graph = snap.LoadEdgeList(snap.PUNGraph, filename)
    node_list = []
    for node in graph.Nodes():
        node_list.append(node.GetId())
    for i in range(0, sample_count):
        sample_pair = random.sample(node_list, 2)
        dist = snap.GetShortPath(graph, sample_pair[0], sample_pair[1], False)
        if dist > 0:
            distance_dst[dist] += 1
    print str(calculate_spid(distance_dst)) + " for " + str(sample_count) + " samples"
    for item in distance_dst:
        distance_dst[item] /= float(sample_count)
    return distance_dst

def get_degree_separation(filename, sample_count):
    degree_dst = collections.defaultdict(int)
    nv = snap.TIntV()
    graph = snap.LoadEdgeList(snap.PUNGraph, filename)
    node_list = []
    for node in graph.Nodes():
        node_list.append(node.GetId())
    samples = random.sample(node_list, sample_count)
    for sample in samples:
        hop = 1
        nodes_at_hop = snap.GetNodesAtHop(graph, sample, hop, nv, False)
        while nodes_at_hop > 0:
            degree_dst[hop]+= nodes_at_hop
            hop+=1
            nodes_at_hop = snap.GetNodesAtHop(graph, sample, hop, nv, False)
    for item in degree_dst:
        degree_dst[item] /= float(len(node_list) * sample_count)
    return degree_dst

def pdf_to_cdf(distribution):
    keys = sorted(distribution.keys())
    curr_sum = 0
    for key in keys:
        distribution[key] += curr_sum
        curr_sum = distribution[key]

def calculate_spid(distance_dist):
    degree_list = []
    for item in distance_dist:
        for i in range(0, distance_dist[item]):
            degree_list.append(item)
    return np.std(degree_list) ** 2 / np.mean(degree_list)

def get_two_hop_dist(filename):
    nv = snap.TIntV()
    graph = snap.LoadEdgeList(snap.PUNGraph, filename)
    two_hop = collections.defaultdict(int)
    ratio_list = []
    for node in graph.Nodes():
        nodes_at_two_hop = snap.GetNodesAtHop(graph, node.GetId(), 2, nv, False)
        nodes_at_one_hop = snap.GetNodesAtHop(graph, node.GetId(), 1, nv, False)
        if nodes_at_two_hop > 0 :
            two_hop[nodes_at_two_hop] += 1
            ratio_list.append(float(nodes_at_two_hop)/nodes_at_one_hop)

    print "mean ratio of two hop to one hop was " + str(np.mean(ratio_list))

    for i in two_hop:
        two_hop[i] = two_hop[i] /float(graph.GetNodes())
    return two_hop

if __name__ == "__main__":
    dist = get_two_hop_dist("mal-rec-graph")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('size of two hop neighborhood')
    plt.ylabel('proportion of nodes')
    plt.scatter(dist.keys(), dist.values(), color = 'Red')
    plt.show()
    #dist = get_dist_distribution("mal-rec-graph", 1000)
    #dist1 = get_dist_distribution("mal-rec-graph", 5000)
    #dist2 = get_dist_distribution("mal-rec-graph", 8000)
    #dist = get_degree_separation("mal-rec-graph", 1000)
    ##print dist
    #print sum(dist.values())
    #pdf_to_cdf(dist)
    #print dist
    #plt.plot(dist.keys(), dist.values(), color = 'Red')
    #plt.plot(dist1.keys(), dist1.values(), color = 'Blue')
    #plt.plot(dist2.keys(), dist2.values(), color = 'Green')
    #plt.show()
    #plot_degree_dist()
    #find_nonexistent_anime()
    #create_edge_list("uniq-mal-dump.txt")
    #get_id_to_name("maldump.txt", "maldump-key")
