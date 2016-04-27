import pydot
import layers
import node_sort
import hlink_detect

def plot (upper_limit,lower_limit, location_code, file_append):

	with open ('data/links_sorted-%s.txt' %file_append, 'r') as links_file:
		lines = links_file.readlines()

	g1 = pydot.Dot (graph_type = 'graph', splines='spline', ranksep="1.0", nodesep="0.3")

	for j in range (0, len(lines)):
		delimited = lines[j].split()
		
		device_type_1 = delimited[0][delimited[0].find("-") + 1 : delimited[0].find("-") + 3]			
		device_type_2 = delimited[1][delimited[1].find("-") + 1 : delimited[1].find("-") + 3]

		if (layers.layers_dict(device_type_1) < layers.layers_dict(upper_limit)) or (layers.layers_dict(device_type_2) < layers.layers_dict(upper_limit)):
			continue

		if (layers.layers_dict(device_type_1) > layers.layers_dict(lower_limit)) or (layers.layers_dict(device_type_2) > layers.layers_dict(lower_limit)):
			continue
		
		edge = pydot.Edge (str(delimited[0]), str(delimited[1]),
							color="black",
							fontsize='10',
							minlen="2.5",
							penwidth="0.7",
							labeldistance="1.2")
		g1.add_edge (edge)

	nodes = node_sort.node_sort(upper_limit,lower_limit, location_code, file_append)

	layer = pydot.Subgraph(rank='same')
	h_node = hlink_detect.hlink_detect(upper_limit,lower_limit, location_code, file_append)

	for i in range (0, len(nodes)):
		layers_key = layers.layers_key()[i]	
		list = nodes[str(layers_key)]
			
		if len(list) != 0:
			for k in range (0, len(list)):
				node = pydot.Node(str(list[k]),
								shape="record",
								width="1.0",
								height="0.5",
								fillcolor="grey", 
								style="rounded, filled, bold",
								align="center",
								fontsize="10.0",
								fontname="arial")
				layer.add_node(node)			
		
		g1.add_subgraph(layer)

		layer = pydot.Subgraph(rank='same')
		
		if len(list) != 0:
			for k in range (0, len(list)-1):
				if list[k] not in h_node:	
	
					edge = pydot.Edge (str(list[k]), 
						str(list[k+1]),	
						minlen="1.0",						
						style='invis')
					g1.add_edge (edge)

	g1.write_svg('img/topology-%s.svg' %file_append)					