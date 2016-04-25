import getpass
import layers

def seed_device():
	
	seed_device = raw_input("\nEnter seed device hostname or IP address: ")
	device_type = seed_device[seed_device.find("-") + 1 : seed_device.find("-") + 3]
	layers_list = layers.layers_list()
	live_update = None
	
	if (len(seed_device) < 9) or (device_type not in layers_list):
		while (len(seed_device) < 9) or (device_type not in layers_list):
			seed_device = raw_input("Enter a valid seed device hostname or IP address: ")			
			device_type = seed_device[seed_device.find("-") + 1 : seed_device.find("-") + 3]
	return live_update, seed_device

def upper_limit():
	layers_list = layers.layers_list()
	
	print "\nEnter upper limit of device hierarchy. Valid inputs include:", ','.join(layers_list)
	upper_limit = raw_input("Upper limit: ")
	if (len(upper_limit) is 0) or (upper_limit not in layers_list):
		while (len(upper_limit) is 0) or (upper_limit not in layers_list):
			upper_limit = raw_input("Enter a valid upper limit: ")
	return upper_limit

def lower_limit(upper_lim):
	layers_list = layers.layers_list()
	
	print "\nEnter lower limit of device hierarchy. Valid inputs include:", ','.join(layers_list[int(layers.layers_dict(upper_lim)):len(layers_list)])
	lower_limit = raw_input("Lower limit: ")
	
	if ((len(lower_limit) is 0) or (lower_limit not in layers_list) or (layers.layers_dict(lower_limit) <= layers.layers_dict(upper_lim))):
		while (len(lower_limit) is 0) or (lower_limit not in layers_list) or (layers.layers_dict(lower_limit) <= layers.layers_dict(upper_lim)):
			lower_limit = raw_input("Enter a valid lower limit: ")
	return lower_limit

def location_code():	
	print "\nEnter location code, e.g. abcsite"
	location_code = raw_input("Location code: ")
	if (len(location_code) < 3):
		while (len(location_code) < 3):
			location_code = raw_input("Enter a valid location code: ")
	return location_code	
	
def username():
	username = raw_input("\nUsername: ")
	if len(username) is 0:
		while len(username) is 0:
			username = raw_input("Enter a valid username: ")
	return username
	
def password():
	password = getpass.getpass("Password: ")
	return password
	
def graph_type():
	print "Enter graph type desired. Valid inputs include:\n\t\t\t\t 'o'  = orthographic lines\n\t\t\t\t 'no' = non-overlapping lines\n\t\t\t\t 's'  = straight lines"

	graph_type_desired = raw_input("Enter graph type: ")
	if graph_type_desired not in ['o', 'no', 's']:
		while graph_type_desired not in ['o', 'no', 's']:
			graph_type_desired = raw_input("Enter valid graph type: ")
	
	if graph_type_desired is 'o':
		graph_type_desired = 'ortho'
	elif graph_type_desired is 'no':
		graph_type_desired = 'splines'
	elif graph_type_desired is 's':
		graph_type_desired = 'line'
	
	return graph_type_desired