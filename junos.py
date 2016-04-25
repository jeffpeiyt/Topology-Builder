import namecheck

def parser (data, current_node, nodes, accessed, file_append):
	
	lines = data.splitlines()
	first_line = 0
	
	for y in range (0,len(lines)):
		if "Local" in lines[y]:
			first_line = y
			break

	nodes_file = open ('data/nodes-%s.txt' %file_append, 'a')
	links_file = open ('data/links-%s.txt' %file_append, 'a')

	lengths = []
	final1 = []
	unique = []
	y = first_line + 1

	while y < len(lines)-1:
		delimited_line = lines[y].split()
		final1 = delimited_line
		
		if len(final1) >= 5:					
			if "." in final1[4]:
				final1[4] = final1[4][0:(final1[4].index("."))]

			final2 = final1[:1] + final1[-2:]		
			final3 = current_node + "\t" + final2[2].lower() + "\t" + final2[0] + "\t" + final2[1] + "\n"
		elif len(final1) < 5:
			y+=1
			continue

		if namecheck.namecheck(str(final2[2].lower())) is False:
			y+=1
			continue
			
		if (final2[2].lower() != current_node.lower()) and (final2[2].lower() not in nodes):
			unique.append (final2[2].lower())		
			nodes.append (final2[2].lower())		
		
		if (final2[2].lower() not in accessed):
			links_file.write(final3)
		
		y+=1

	return unique