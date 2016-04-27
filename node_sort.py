import natsort
import layers
import time

def node_sort(upper_limit, lower_limit, location_code, file_append):

	with open ('data/nodes-%s.txt' %file_append, 'r') as nodes_file:
		devices = nodes_file.read().splitlines() 					
		
	nodes_dict = layers.nodes_dict()
 	layers_key = layers.layers_key()

	for i in range (0, len(devices)):

		device_type = devices[i][devices[i].find("-") + 1 : devices[i].find("-") + 3]
		node_location_code = devices[i][0:len(location_code)]
	
		if node_location_code != location_code:
			continue
		elif (layers.layers_dict(device_type) < layers.layers_dict(upper_limit)) or (layers.layers_dict(device_type) > layers.layers_dict(lower_limit)):
			continue
		else:
			nodes_dict[device_type].append(devices[i])			
	
	for i in nodes_dict:
		for j in nodes_dict[i]:
			nodes_dict[i] = natsort.natsorted(nodes_dict[i])


	return nodes_dict