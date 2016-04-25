import access
import catos
import ios_cdp
import ios_lldp
import iosxr_cdp
import iosxr_lldp
import nxos_cdp
import nxos_lldp
import eos
import junos
import time

def get_ndp_output (current_node,nodes,accessed,username,password,file_append):

	accessed_file = open ('data/accessed-%s.txt' %file_append, 'a')
	print "\nAccessing node:", current_node

	access_start_time = time.time()
	nos = access.ssh_ver (current_node,'show version',username,password)
	access_iteration = 0
	
	if (nos == 'ios') or (nos == 'Unknown NOS'):
		cdp_out = access.ssh_ndp (current_node,'show cdp neighbor',username,password)
		cdp_nodes, current_unique_neighbors = ios_cdp.parser(cdp_out, current_node, nodes, accessed, file_append)
		nodes = add_neighbors(current_node, current_unique_neighbors, nodes, accessed,access_iteration)
		access_iteration+=1

		lldp_out = access.ssh_ndp (current_node,'show lldp neighbor',username,password)
		if "enabled" not in lldp_out:
			current_unique_neighbors = ios_lldp.parser(lldp_out, current_node, nodes, cdp_nodes, accessed, file_append)
			nodes = add_neighbors(current_node, current_unique_neighbors, nodes, accessed,access_iteration)
	elif (nos == 'nxos'):
		cdp_out = access.ssh_ndp (current_node,'show cdp neighbor',username,password)
		cdp_nodes, current_unique_neighbors = nxos_cdp.parser(cdp_out, current_node, nodes, accessed, file_append)
		nodes = add_neighbors(current_node, current_unique_neighbors, nodes, accessed,access_iteration)
		access_iteration+=1

		lldp_out = access.ssh_ndp (current_node,'show lldp neighbor',username,password)
		current_unique_neighbors = nxos_lldp.parser(lldp_out, current_node, nodes, cdp_nodes, accessed, file_append)
		nodes = add_neighbors(current_node, current_unique_neighbors, nodes, accessed,access_iteration)
	elif (nos == 'iosxr'):
		cdp_out = access.ssh_ndp (current_node,'show cdp neighbor',username,password)
		cdp_nodes, current_unique_neighbors = iosxr_cdp.parser(cdp_out, current_node, nodes, accessed, file_append)
		nodes = add_neighbors(current_node, current_unique_neighbors, nodes, accessed,access_iteration)
		access_iteration+=1

		lldp_out = access.ssh_ndp (current_node,'show lldp neighbor',username,password)
		current_unique_neighbors = iosxr_lldp.parser(lldp_out, current_node, nodes, cdp_nodes, accessed, file_append)
		nodes = add_neighbors(current_node, current_unique_neighbors, nodes, accessed,access_iteration)
	elif (nos == 'catos'):
		cdp_out = access.ssh_ndp (current_node,'show cdp neighbor',username,password)
		current_unique_neighbors = catos.parser(cdp_out, current_node, nodes, accessed, file_append)
		nodes = add_neighbors(current_node, current_unique_neighbors, nodes, accessed,access_iteration)
	elif (nos == 'eos'):
		lldp_out = access.ssh_ndp (current_node,'show lldp neighbor',username,password)
		current_unique_neighbors = eos.parser(lldp_out, current_node, nodes, accessed, file_append)
		nodes = add_neighbors(current_node, current_unique_neighbors, nodes, accessed,access_iteration)
	elif (nos == 'junos'):
		lldp_out = access.ssh_ndp (current_node,'show lldp neighbor',username,password)
		current_unique_neighbors = junos.parser(lldp_out, current_node, nodes, accessed, file_append)
		nodes = add_neighbors(current_node, current_unique_neighbors, nodes, accessed,access_iteration)

	access_time = time.time() - access_start_time
	accessed_file.write (current_node + "\t" + nos + "\t" + str(round(access_time,2)) + "\n")
	return nodes, access_time


def add_neighbors (current_node, current_unique_neighbors, nodes, accessed, access_iteration):

	if current_node not in accessed:
		accessed.append (current_node)
		
		if len(current_unique_neighbors) > 0:
			print "Neighbors discovered:\t",  ','.join(current_unique_neighbors)
		else:
			print "No new nodes discovered"

		return nodes
	
	elif (current_node in accessed) and (access_iteration is 1):
	
		if len(current_unique_neighbors) > 0:
			print "Neighbors discovered (lldp):\t", ','.join(current_unique_neighbors)
		else:
			print "No new nodes discovered via LLDP"

		return nodes
		
	else:
		print "\nAccess loop detected, aborting"
