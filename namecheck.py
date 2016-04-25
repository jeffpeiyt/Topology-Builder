import layers

names = layers.layers_list()
valid = False

def namecheck (hostname):	
	for j in range (0,len(names)):
		if ("-" + names[j]) in hostname:
			valid = True
			break
		else:
			valid = False
	return valid