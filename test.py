import crawler
login_info_file = open("login.txt")
lines = login_info_file.readlines()
print "lines = "
print lines

login_info = {}
login_info['username'] = lines[0].replace("\n", "")
login_info['password'] = lines[1].replace("\n", "")

#rails_crawler = crawler.RailsRepoCrawler(login_info)
#rails_crawler.start_query()

django_crawler = crawler.DjangoRepoCrawler(login_info)
django_crawler.start_query()
