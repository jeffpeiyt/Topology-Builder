import natsort
import layers
import node_sort
import fileinput

def link_sort(upper_limit, lower_limit, location_code, file_append):
	with open ('data/links-%s.txt' %file_append, 'r') as links_file:
		lines = links_file.readlines()
		
	sorted_1_file = open ('data/links_sorted-%s.txt' %file_append, 'a')
	sorted_1_file.seek(0)
	sorted_1_file.truncate()

	nodes = node_sort.node_sort(upper_limit, lower_limit, location_code, file_append)
	both_found = 0
	k1 = 0
	k2 = 0
	
	for i in range (0, len(lines)):
		delimited = lines[i].split()		
		device_type_1 = delimited[0][delimited[0].find("-") + 1 : delimited[0].find("-") + 3]			
		device_type_2 = delimited[1][delimited[1].find("-") + 1 : delimited[1].find("-") + 3]
		node_location_code_1 = delimited[0][0:len(location_code)]
		node_location_code_2 = delimited[1][0:len(location_code)]

		if (node_location_code_1 != location_code) or (node_location_code_2 != location_code):
			continue

		if (layers.layers_dict(device_type_1) < layers.layers_dict(upper_limit)) or (layers.layers_dict(device_type_2) < layers.layers_dict(upper_limit)):
			continue

		if (layers.layers_dict(device_type_1) > layers.layers_dict(lower_limit)) or (layers.layers_dict(device_type_2) > layers.layers_dict(lower_limit)):
			continue
		
		if layers.layers_dict(device_type_1) < layers.layers_dict(device_type_2):
			new_delimited = delimited[0] + "\t" + delimited[1] + "\t" + delimited[2] + "\t\t" + delimited[3] + "\n"
			sorted_1_file.write(new_delimited)
		
		elif layers.layers_dict(device_type_1) > layers.layers_dict(device_type_2):
			new_delimited = delimited[1] + "\t" + delimited[0] + "\t" + delimited[3] + "\t" + delimited[2] + "\n"
			sorted_1_file.write(new_delimited)
		
		elif layers.layers_dict(device_type_1) == layers.layers_dict(device_type_2):
			
			for key in nodes.keys():
				if delimited[0] in nodes[key]:
					k1 = nodes[key].index(delimited[0])
					both_found+=1
				if delimited[1] in nodes[key]:
					k2 = nodes[key].index(delimited[1])
					both_found+=1
				if both_found is 2:
					both_found = 0
					break
			
			if k1 < k2:
				new_delimited = delimited[0] + "\t" + delimited[1] + "\t" + delimited[2] + "\t" + delimited[3] + "\n"
				sorted_1_file.write(new_delimited)
			elif k1 > k2:
				new_delimited = delimited[1] + "\t" + delimited[0] + "\t" + delimited[3] + "\t" + delimited[2] + "\n"
				sorted_1_file.write(new_delimited)
	
	sorted_1_file.close()
	
	for line in fileinput.FileInput('data/links_sorted-%s.txt' %file_append, inplace=1):
		line = line.replace(":","-")
		print line,