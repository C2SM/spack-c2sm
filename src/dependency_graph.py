#!/usr/bin/python

import matplotlib.pyplot as plt
import networkx as nx
import test_spack
from networkx.drawing.nx_agraph import graphviz_layout

G = nx.DiGraph()
for case in test_spack.all_test_cases:
    G.add_node(case.package_name)
    for dep in case.depends_on:
        G.add_edge(case.package_name, dep)

pos = graphviz_layout(G, prog='neato')

nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, font_size=10)

plt.show()