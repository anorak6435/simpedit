# build a grammar using the parse_def file
# This becomes purely a string that helps me debugging the code
from pyvis import network as net
print("Hello world!")
import re
# import networkx as nx
# import matplotlib.pyplot as plt
# G = nx.DiGraph()
G =  net.Network(height='600px',width='90%',
                  bgcolor='white',font_color="red")



with open("parse_def.py", "r") as f:
    contents = f.readlines()

# def del_last_3_chars(value):
#     return value[:-3]

productions = [ line for line in contents if line.startswith("@pg.production")]
productions = list(map(lambda value: re.sub("@pg.production\(\"", "", value), productions))

all_nodes = set()
for i, prod in enumerate(productions):
    line : str = prod.split(":")[1]
    assert line.endswith('")\n'), f"Line:`{line}` does not seem to end with \")"
    line = line[1:-3] # Remove the last characters and the first space of the line
    # splitted node information used later for edge detection
    productions[i] = (prod.split(":")[0][:-1], line.split(" "))
    all_nodes.update(line.split(" "))
# for node in all_nodes:
#     if node.isupper():
#         print(node)

# # G.add_nodes_from(all_nodes)
rule_index = {}
# add rule names to the rule_index
for idx, (rulename, children) in enumerate(productions):
    if not rulename in rule_index.keys():
        G.add_node(idx*2, label=rulename)
        rule_index[rulename] = idx*2

# turn a list of nodes into to mapping if name and index
def node_data(value):
    node = G.get_node(value)
    return (node["label"], node['id'])
    
def get_first_el(value : tuple[str, int]):
    return value[0]

# get the edges of a given rule
count = 2*len(productions)
for rulename, children in productions:
    previous_children = []
    for idx, child in enumerate(children):
        # generate the next node
        if child in rule_index.keys():
            child_index = rule_index[child] # references to existing rules are linked to the node of the rule
        else:
            # if the child is already an connection to the rule. use that connection
            neighbors = list(map(node_data, list(G.neighbors(rule_index[rulename]))))
            bor_names = list(map(get_first_el, neighbors))
            # print("ADJ:", neighbors)
            if child in bor_names:
                child_index = neighbors[bor_names.index(child)][1]
            else:
                # no existing child was found.
                # set the color of the child
                clr = "blue"
                if child.isupper():
                    clr = "green" # the color for Tokens
                # G.add_node(count+idx, child, color=clr)
                child_index = count+idx

        if idx == 0:
            G.add_node(child_index, child, color="orange")
            # the first child is connected to the rule_name
            G.add_edge(source=rule_index[rulename], to=child_index)
        else:
            # next nodes are connected to the previous nodes
            # check if the node has the same neighbor as the given child.
            neighbors = list(map(node_data, list(G.neighbors(previous_children[-1]))))
            bor_names = list(map(get_first_el, neighbors))
            if child in bor_names:
                # use the existing child
                child_index = neighbors[bor_names.index(child)][1]
            else:
                # create the new child node
                G.add_node(child_index, child, color="red")
            G.add_edge(source=previous_children[-1], to=child_index)
        previous_children.append(child_index)
    # over the children of the given rule
    # add the length of the children to the count
    count += len(children)

G.write_html("Grammar_Graph.html")

# # print("all nodes!")
# # print(all_nodes)

print("all productions:")
print(productions)

print("rule_index")
print(rule_index)
# # rule_names = list(set([prod.split(":")[0].strip() for prod in productions]))

# # G.add_nodes_from(rule_names)
# # G.add_edges_from([(rule_names[0], rule_names[1])])
# # print(rule_names)


# plt.figure(1)
# pos = nx.spring_layout(G, scale=2)
# nx.draw_networkx(G, pos)

# plt.show()

# for prod in productions:
#     print(prod)

"""
let's define what the rules should look like
How can they be linked efficiëntly to the ast that will be build from them
"""

