import sys, getopt

str_header = "library IEEE;\n\
use IEEE.STD_LOGIC_1164.ALL;\n\
use IEEE.NUMERIC_STD.ALL;\n\n\
-- Uncomment the following library declaration if instantiating\n\
-- any Xilinx primitives in this code.\n\
--library UNISIM;\n--use UNISIM.VComponents.all;\n\n"

todo_entity = '\n--TODO: complete entity parameters under this\n\n'
todo_signal = '\n--TODO: put your signal instances down here\n\n'
todo_output = '\n--TODO: place you final attributions to outputs here\n\n'

debug = False

def main(argv):
	if debug:
		print(str_header)
	
	str_entity = "entity " + argv[0] + " is \n\tPort (\n\n\t\t);\nend " + argv[0] + ";\n\narchitecture Behavioral of " + argv[0] + " is\n\n"
	if debug:
		print(str_entity)
	
	# initial body contains header, TODO_entity and entity frame
	body = str_header + todo_entity + str_entity
	
	# declare components
	for arg in argv[1:]:
		f = vhdFileAsString(arg)
		
		# find component name and attributes
		componentName = findName(f)
		str_attributes = findAttr(f, componentName)
		
		# generate component
		str_component = 'component ' + str_attributes + 'end component;\n\n'
		
		if debug:
			print(str_component)
		
		# add component to module's body
		body += str_component
		
	body += todo_signal + 'begin\n\n'
	
	# instanciate components
	for arg in argv[1:]:
		f = vhdFileAsString(arg)
		
		# generate instance header
		componentName = findName(f)
		instance = "inst_" + componentName + " : " + componentName + "\n\tPort map ("
		
		# find attributes
		str_attributes = findAttr(f, componentName)
		str_attributes = trim(str_attributes[str_attributes.find("(")+1 : -2])
		attributes = str_attributes.split(";")
		
		# find attributes names
		attributes_names = []
		for atr in attributes:
			attributes_names.append(atr.split(':')[0])
		
		# generate instance body
		for name in attributes_names:
			instance += "\n\t\t\t" + name + "\t=>\t,"
			
		# remove last comma
		instance = instance[:-1]
		
		# add instance final header
		instance += "\n\t\t\t);\n\n"
		
		if debug:
			print(instance)
			
		body += instance
	
	body += todo_output + "end Behavioral;\n"
	
	f = open(argv[0] + ".vhd", "w")
	f.write(body)
	
	if debug:
		print(body)
		
	
# open .vhd file
def vhdFileAsString(filename):
	if ".vhd" not in filename:
		filename += ".vhd"
	return open(filename, 'r').read()
	
# remove spaces, tabs and line jumps
def trim(str):
	return str.replace(" ", "").replace("\t", "").replace("\n", "")
	
# find component name
def findName(f):
	firstIndex = f.find("entity") +7
	lastIndex = firstIndex + f[firstIndex:].find(" is")
	return f[firstIndex:lastIndex]

# find component attributes
def findAttr(f, componentName):
	if debug:
		print(componentName)
	f = f[f.index(componentName + ' is') :]
	f = f[:f.index('end ' + componentName)]
	return f

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("usage: python " + sys.argv[0] + " <entity_name> " + "<component_1> " + "<component_2> " + "<component_n>")
		exit(2)
	main(sys.argv[1:])