import time
import access
import info
import discover
import layers
import link_sort
import node_sort
import plot
import plot_small

print "-----------------------------------------------------------------------------------------\n"

live_update, seed_device = info.seed_device()
upper_limit = info.upper_limit()
lower_limit = info.lower_limit(upper_limit)
location_code = info.location_code()
username = info.username()
password = info.password()

script_start_time = time.time()
file_seed_time = (time.strftime("%Y%m%d-%H%M%S"))
file_append = username + "-" + file_seed_time

accessed = []
nodes = []
i = 0
exec_num = 0
total_access_time = 0
master_list = []

nodes.append (seed_device)

accessed_file = open ('data/accessed-%s.txt' %file_append, 'a')
accessed_file.seek(0)
accessed_file.truncate()

with open ('data/nodes-%s.txt' %file_append, 'a') as nodes_file:
	nodes_file.seek(0)
	nodes_file.truncate()

with open ('data/links-%s.txt' %file_append, 'a') as links_file:
	links_file.seek(0)
	links_file.truncate()

with open ('data/links_sorted-%s.txt' %file_append, 'a') as sorted_file:
	sorted_file.seek(0)	
	sorted_file.truncate()

while i != len(nodes):
	node_device_type = nodes[i][nodes[i].find("-") + 1 : nodes[i].find("-") + 3]
	node_location_code = nodes[i][0:len(location_code)]

	if i == 0:	
		nodes, access_time = discover.get_ndp_output(nodes[i],nodes,accessed,username,password, file_append)
		total_access_time = total_access_time + access_time

	if node_location_code != location_code:	
		i+=1
		continue
	
	elif (layers.layers_dict(node_device_type) >= layers.layers_dict(upper_limit) and layers.layers_dict(node_device_type) <= layers.layers_dict(lower_limit) and  i > 0):

		nodes, access_time = discover.get_ndp_output(nodes[i],nodes,accessed,username,password, file_append)
		total_access_time = total_access_time + access_time
	elif i > 0:

		accessed_file.write(nodes[i] + "\tskipped" + "\n")
		i+=1
		continue
	
	i+=1
	
	if live_update == 'y':
		node_sort.node_sort(upper_limit, lower_limit, location_code, file_append)
		link_sort.link_sort(upper_limit, lower_limit, location_code, file_append)
		plot.plot(upper_limit, lower_limit, location_code)

print "\n---------------------------------------------------------------------------------------------------------------\n"
				
with open ('data/nodes-%s.txt' %file_append, 'a') as nodes_file:
	for i in range (0, len(nodes)):
		nodes_file.write(nodes[i] + "\n")

nodes_dict = node_sort.node_sort(upper_limit,lower_limit, location_code, file_append)

lengths = [len(v) for v in nodes_dict.values()]
print "%d nodes discovered:" %sum(lengths),
for i in nodes_dict:
	for j in nodes_dict[i]:
		print j,",",


print "\n\nSorting links..."
link_sort.link_sort(upper_limit, lower_limit, location_code, file_append)

data_time = time.time() - script_start_time

print "Plotting...\n"
plot_time_start = time.time()
plot_small.plot(upper_limit, lower_limit, location_code, file_append)
plot_time = time.time() - plot_time_start

exec_time = time.time() - script_start_time

print ("Data Collection and Analysis time: \t%s seconds") % round(data_time,2), 
print (" (%s seconds Device Access Time)") % round(total_access_time,2)
print ("Plotting time: \t\t\t%s seconds") % round(plot_time,2)
print ("Total Execution time: \t\t%s seconds\n") % round(exec_time,2)

print "Topology generated at: \t img/topology-%s.svg\n\n" %file_append