import snap
from sets import Set


DATA_SOURCE = "uniq-mal-dump.txt"

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

if __name__ == "__main__":
    #find_nonexistent_anime()
    create_edge_list("uniq-mal-dump.txt")
    #get_id_to_name("maldump.txt", "maldump-key")
