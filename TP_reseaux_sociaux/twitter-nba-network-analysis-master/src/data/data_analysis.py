import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from adjustText import adjust_text
import csv

from networkx.drawing.nx_pydot import graphviz_layout


def plot_in_vs_out_degree(filepath):
    """
     plots the in-degree vs out-degree of our network and saves the plot into a file
    :param filepath: the filepath in which we want to save our png plot
    """
    data_file_path = "graph.csv" ## this file was generated from gephi. I simply exported the data from gephi into a csv
    df = pd.read_csv(data_file_path)
    ax = df.set_index('outdegree')['indegree'].plot(style='o')
    texts = []
    def label_point(outdegree, indegree, Label, ax):
        a = pd.concat({'outdegree': outdegree, 'indegree': indegree, 'Label': Label}, axis=1)
        for i, point in a.iterrows():
            #only include labels for players with >= 90 followers
            if point['indegree'] >= 90:
                texts.append(plt.text(x=point['outdegree'], y=point['indegree'], s=str(point['Label'])))
    label_point(df.outdegree, df.indegree, df.Label, ax)
    adjust_text(texts, arrowprops=dict(arrowstyle="->", color='b'))
    plt.title("Plot of follower count vs following count amongst NBA players")
    plt.xlabel("following count in NBA")
    plt.ylabel("follower count in NBA")
    # plt.show()
    plt.savefig(filepath)


def create_networkx_graph_from_edge_list_csv():
    """
    creates a networkX digraph based on the data in our nba network
    :return:
    """
    graph = nx.DiGraph()
    with open("../all.csv", "r", newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)  # move the reader cursor to next line
        # extracting each data row one by 
        for row in csvreader:
            graph.add_edge(row[0], row[1])
    return graph


def getMutualFollowers(graph, filepath):
    """
    takes a digraph and finds the number of mutual connections each node has.
    A mutual connection between u and v means that the graph has the edge u->v and v->u
    It writes this out into a csv file which we can use in gephi to create a separate analysis for mutual friends network
    :param graph: a networkx digraph
    :return: a dictionary where the key is each node and the value is the number of mutual connections it has
    """
    nodes = list(graph.nodes)
    output = {}
    with open(filepath, "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["source", "target"])
        for i in range(0, len(nodes) - 1):
            for j in range(i+1, len(nodes)):
                u,v = nodes[i], nodes[j]
                if graph.has_edge(u, v) and graph.has_edge(v, u):
                    csvwriter.writerow([u,v])
                    if u in output:
                        output[u] += 1
                    else:
                        output[u] = 1
                    if v in output:
                        output[v] += 1
                    else:
                        output[v] = 1
    return output


# plot_in_vs_out_degree(filepath="visualizations/indegree_vs_outdegree.png")

# use this graph object + networkx to do any additional graph analysis you might want
# most of my analysis was actually done in gephi
#graph = create_networkx_graph_from_edge_list_csv()
#average_shortest_path_length = nx.average_shortest_path_length(graph)
#print(average_shortest_path_length)
# getMutualFollowers(graph, "mutual_connections.csv")



import pandas
import csv
def replaceNumsWithNames(csvFile,separator,csvLabels,out):
    fichier=pandas.read_csv(csvFile,sep=separator,header=None)
    reader = csv.reader(open(csvLabels, 'r'))
    dico = {}
    for row in reader:
        k, v = row
        try:
            dico[int(k)] = v
        except:
            pass
    fichier2=fichier.replace(dico)
    fichier2.to_csv(out,index=False,header=None)
replaceNumsWithNames("graph.csv",";","../nbaplayers.csv","graph2.csv")
# replaceNumsWithNames("../all.csv",",","../nbaplayers.csv","all2.csv")

