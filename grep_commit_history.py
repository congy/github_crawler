import requests
import json
import helper

owner = "diaspora"
repo = "diaspora"
prefix="https://api.github.com"

all_commits_query = "%s/repos/%s/%s/commits"%(prefix, owner, repo)
single_commit_prefix = "%s/repos/%s/%s/commits"%(prefix, owner, repo)

dump_file = open("commit_history/%s.txt"%repo, "w")

#grep most recent 200 commits that involve rb files
MAX_COUNT=200

login_info_file = open("login.txt")
lines = login_info_file.readlines()
login_name = lines[0].replace("\n", "")
login_password = lines[1].replace("\n", "")

count = 0
page = 0

while count < MAX_COUNT:
	rq_url = "%s"%all_commits_query
	if page > 0:
		rq_url += "?page=%d"%page
	page += 1
	print rq_url
	response = requests.get(rq_url, auth=(login_name, login_password))
	data = json.loads(response.text)
	if len(data) == 0:
		break
	for single_commit in data:
		commit_sha = single_commit["sha"]
		dump_file.write("\n\n========commit %s========\n"%str(commit_sha))
		dump_file.write("          (Time:  %s)\n"%single_commit["commit"]["author"]["date"])
		single_commit_url = "%s/%s"%(single_commit_prefix, commit_sha)
		print single_commit_url 
		resp = requests.get(single_commit_url, auth=(login_name, login_password))
		d = json.loads(resp.text)
		if "files" not in d.keys():
			break
		files = d["files"]
		modify_rb = False
		for f in files:	
			if f["filename"].endswith(".rb"):
				modify_rb = True
				dump_file.write("File %s\n"%f["filename"])
				if "patch" in f.keys():
					dump_file.write("%s\n"%(f["patch"].replace("\\n","\n").encode('utf-8')))
		if modify_rb:
			count += 1
