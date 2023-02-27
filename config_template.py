import yaml, os, sys, csv, argparse, logging, time

# Path variables
cwd=os.curdir
data_rel_path=os.path.join(cwd, 'data')
templates_rel_path=os.path.join(cwd, 'templates')
output_rel_path=os.path.join(cwd, 'output')

# Logging settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.StreamHandler()
fh_formatter = logging.Formatter('%(asctime)s [%(levelname)s] : %(message)s', datefmt='%y%m%d %H:%M:%S')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('site', help='3 char Site Id')
	parser.add_argument('set', help='csv file with template-device association')
	args = parser.parse_args()
	data=os.path.join(data_rel_path,args.site+'.yaml')

	# get every set of template-device to create fragment
	fragments=get_list(os.path.join(data_rel_path,args.set))

	# Iteration for every SB
	for each_sb in sb_list(data):
		print ('\n### Creating files for ',each_sb.upper(),'###\n')
		for row in fragments:
			if (row[1]!='tbd' and row[0]!= 'tbd'):
				# Create MOP Procedure Fragments
				# from template list file:
				# row[0] jinja template; row[1] generic device (e.g.: drc_legacy_odd)
				config_template(data,each_sb,row[0],row[1])
		#config_template(data,each_sb,'dsc_pre_config','dsc_even')

def sb_list(data):

	# input parameters from yaml file
	try:
        # Catch yaml read error
		# logger.info("Accessing {}".format(data))
		with open(data, 'r') as stream:	
			CfgInput = yaml.safe_load(stream)
	except:
		# Exit script if unable to read yaml file
		logger.critical("Invalid file {}. Please check your input".format(data))
		sys.exit(1)

	# collects SB list from yaml file
	sb_list=[]
	for each_sb in CfgInput:
		sb_list.append(each_sb)
	return (sb_list)

def config_template(data,sb,template_file,device):
	# Jinja2 - Render using Template file
	# create and render the template (using input file and Template file)
	# YAML file, sb to migrate, Jinja template to use and device to operate

	from jinja2 import Environment, FileSystemLoader

	# input parameters from yaml file
	try:
		# Catch yaml read error
		# logger.info("Accessing {}".format(data))
		with open(data, 'r') as stream:	
			CfgInput = yaml.safe_load(stream)
	except:
		# Exit script if unable to read yaml file
		logger.critical("Invalid file {}. Please check your input".format(data))
		sys.exit(1)
	
	# find and load the template
	file_loader = FileSystemLoader(templates_rel_path)
	env = Environment(loader=file_loader)

	# get the Jinja2 template	
	template = env.get_template(template_file+'.j2')

	# Render the output from the template
	result = template.render(config=CfgInput[sb], device={'name':device})
	filename = CfgInput[sb][device]['hostname'].upper()+'_'+sb.upper()+'_'+template_file+'.txt'
	print (filename)
	
	try:
		# Catch txt write error
		# logger.info("Accessing {}".format(filename))
		with open(os.path.join(output_rel_path,filename), 'w') as document:
			document.write(result)
	except:
		# Exit script if unable to write txt file
		logger.critical("Invalid file {}. Please check your input".format(filename))
		sys.exit(1)
	
def get_list(input_file):
	"""
	Get lists from input file
	"""
	try:
		# Catch csv read error
		# logger.info("Accessing {}".format(input_file))
		with open (input_file,'r') as f:
			out_list=list(csv.reader(f, delimiter=';'))
		return out_list
	except:
		# Exit script if unable to read csv file
		logger.critical("Invalid file {}. Please check your input".format(input_file))
		sys.exit(1)

if __name__=='__main__':
	main()
