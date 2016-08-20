import requests
import json
import helper

class BaseRepoCrawler:
	def __init__(self):
		self.index = 1
		self.total_results = 0
		self.logfile = open("log.txt", "w")
	#args: langauge (required)
	#      keyword (default: '')
	#      sort (default: star)
	#      minstar (default: 10)
	#      maxsize (default: 50000)
	#      minsize (default: 100)
	# other params: to be added
	# Github API: "in" -> With this qualifier you can restrict the search to just the repository name, description, readme, or any combination of these
	def base_query(self, args):
		params = ['language', 'keyword', 'sort', 'minstar', 'maxsize', 'minsize']
		defaults = {}
		defaults['keyword'] = ''
		defaults['sort'] = 'stars'
		defaults['minstar'] = 10
		defaults['maxsize'] = 50000
		defaults['minsize'] = 100
		for p in params:
			if p not in args.keys():
				args[p] = defaults[p]
	
		if len(args['keyword']) > 0:
			q = "https://api.github.com/search/repositories?q=%s+language:%s&size:%d..%d&stars:>=%d&sort=%s&order=desc"%(args['keyword'], args['language'], args['minsize'], args['maxsize'], args['minstar'], args['sort'])
		else:
			q = "https://api.github.com/search/repositories?q=language:%s&size:%d..%d&stars:>=%d&sort=%s&order=desc"%(args['language'], args['minsize'], args['maxsize'], args['minstar'], args['sort'])
		return q
	
	def base_match_file_list(self, author, repo_name, f_list):
		for fpath in f_list:
			rq_url = "https://api.github.com/repos/%s/%s/contents/%s"%(author, repo_name, fpath)
			response = requests.get(rq_url, verify=False)
			data = json.loads(response.text)
			if 'message' in data.keys() and data['message'] == 'Not Found':
				return False
		return True

	def start_query(self):
		#1. generate query
		q = self.query()
		print "query = %s"%q
		response = requests.get(q, verify=False)
		data = json.loads(response.text)
		print "total_count = %d"%data["total_count"]
	
		#2. iterate over each repo
		for repo in data["items"]:
			repo_name = repo["name"]
			author = repo["owner"]["login"]
			if repo_name and author:
				if self.match_file_list(author, repo_name):
					status = helper.get_repo_status(repo)
					self.logfile.write("Repo %s, status = "%(repo_name))
					self.logfile.write(str(status))
					self.logfile.write("\n\n")

	def query(self):
		pass

	def match_file_list(self, author, repo_name):
		pass


class DjangoRepoCrawler(BaseRepoCrawler):
		
	def query(self):
		args = {}
		args['language'] = 'python'
		return self.base_query(args)

	def match_file_list(self, author, repo_name):
		f_lists = []
		f_lists.append("manage.py")
		return self.base_match_file_list(author, repo_name, f_lists)

	
class RailsRepoCrawler(BaseRepoCrawler):
		
	def query(self):
		args = {}
		args['language'] = 'ruby'
		return self.base_query(args)

	def match_file_list(self, author, repo_name):
		f_lists = []
		f_lists.append("config/routes.rb")
		return self.base_match_file_list(author, repo_name, f_lists)

		
	
	
