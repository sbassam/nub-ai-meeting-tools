from pyvis.network import Network
import networkx as nx

class Graph:
    
    def __init__(self, html_filename, bgcolor='#22222'):
        self.net = Network(height="780px", width="780", bgcolor="white", font_color="black")
        self.net.barnes_hut(central_gravity=3.0, spring_strength=0.11, damping=0.1)
        self.html_filename = html_filename


    
    def add_node(self, node_id, node_label, node_type):
        if node_type == 'person':
            self.net.add_node(node_id, label=node_label, title=node_type, shape='dot', size=50, color='#2daaf7')
        elif node_type == 'task':
            self.net.add_node(node_id, label=node_label, title=node_type, shape='star', size=50, color='#f7c12d')
        else:
            self.net.add_node(node_id, label=node_label, title=node_type, shape='triangleDown', size=50, color='#eeedf5')
    
    def add_edge(self, src_id, dest_id, label, title):
        self.net.add_edge(src_id, dest_id, label=label, title=title, width=5, font_size=150)

    def get_node_count(self):
        return len(self.net.nodes)
    def get_edge_count(self):
        return len(self.net.edges)



    def display_graph(self):
        # self.net.show_buttons(filter_=['physics'])
        self.net.show(self.html_filename)
    
    def get_html(self):
        HtmlFile = open(self.html_filename, 'r', encoding='utf-8')
        return HtmlFile.read()