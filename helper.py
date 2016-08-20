def get_repo_status(json_content):
	content_names = ['created_at','updated_at','size','stargazers_count','watchers_count','forks','watchers']
	contents = {}
	for ct in content_names:
		contents[ct] = json_content[ct]
	return contents
