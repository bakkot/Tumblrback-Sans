#! /usr/bin/env python

import os
import json
from urllib import urlopen # not python3 compatible
from datetime import datetime
import sys






apiKey = 'cSuR5kl06wv2WlrgOng6qbE9cr05bUkeS8EiTOUOZAcMn9P2mD'


domain = raw_input('Domain (THISPART.tumblr.com): ')
if(domain == ''):
	print 'Invalid url.'
	exit()

url = domain + '.tumblr.com'

outDir = url

pageSize = 500 # best be a multiple of 20, son

def filterBy(x):
	return not x.has_key('reblogged_from_name')  # ie, not a reblog





def progress(s):
	sys.stdout.write("\r")
	sys.stdout.write(s)
	sys.stdout.flush()

def ufix(s):
	return s.encode('ascii', 'xmlcharrefreplace')

def formatPost(post):
	outStr = ''
	type = post['type']
	
	if type == 'text':
		if post.has_key('title') and post['title']:
			outStr += '<h3 class="posttitle">' + ufix(post['title']) + '</h3>\n'
		outStr += '<p class="textbody">' + ufix(post['body']) + '</p>'
		
	elif type == 'answer':
		outStr += '<bockquote><div class="question">'
		if post['asking_url']:
			outStr += '<a href="' + ufix(post['asking_url']) + '"><b>' + ufix(post['asking_name']) + '</b></a>'
		else:
			outStr += '<b>' + ufix(post['asking_name']) + '</b>'
		outStr += ' asked: '
		outStr += ufix(post['question']) + '<br>\n'
		outStr += '</div><br></bockquote>'
		outStr += ufix(post['answer'])
		
	elif type == 'photo':
		for i in post['photos']:
			#outStr += '<img src="' + i['original_size']['url'] + '" /><br>\n'   # full images
			#outStr += '<a href="' + i['original_size']['url'] + '">img</a><br>\n' # just links
			outStr += '<a href="' + i['original_size']['url'] + '">' + '<img src="' + i['alt_sizes'][-1]['url'] + '" />' + '</a><br>\n' # thumbs linking to full
			if not i['caption'] == "":
				outStr += '<br>\n' + ufix(i['caption']) + '\n<br>'
		if post.has_key('caption'):
			outStr += '<br>\n' + ufix(post['caption'])
			
	elif type == 'quote':
		outStr += '<blockquote><h4>' + ufix(post['text']) + '</h4><br>\n'
		outStr += ' ~ ' + ufix(post['source']) + '</blockquote>'
		
	elif type == 'video':
		outStr += ufix(post['player'][0]['embed_code']) + '\n<br>\n'
		if post.has_key('caption'):
			outStr += ufix(post['caption'])		
			
	elif type == 'chat':
		if post.has_key('title') and post['title']:
			outStr += '<h3 class="posttitle">' + ufix(post['title']) + '</h3>\n'
		outStr += '<ul class="chat">\n'
		for i in post['dialogue']:
			outStr += '<li><b>' + ufix(i['name']) + '</b>: ' + ufix(i['phrase']) + '</li>\n'
		outStr += '</ul>'
		
	elif type == 'link':
		outStr += '<a href="' + post['url'] + '">'
		if post.has_key('title') and post['title']:
			outStr += '<h3 class="posttitle">' + ufix(post['title']) + '</h3>\n'
		else:
			outStr += '<h3 class="posttitle">' + post['url'] + '</h3>\n'
		outStr += '</a>'
		if post.has_key('description') and post['description']:
			outStr += '' + ufix(post['description']) + ''
			
	elif type == 'audio':
		outStr += ufix(post['player']) + '<br>\n'
		if post.has_key('caption') and post['caption']:
			outStr += ufix(post['caption'])
			
	else:
		outStr += '<b>unhandled type: ' + type + '</b>'
	
	if(len(post['tags']) > 0):
		outStr += '\n<br>\n'
		for tag in post['tags'][:-1]:
			outStr += '#<a href="http://' + domain + '.tumblr.com/tagged/' + ufix(tag) + '">' + ufix(tag) + '</a> '
		outStr += '#<a href="http://' + domain + '.tumblr.com/tagged/' + ufix(post['tags'][-1]) + '">' + ufix(post['tags'][-1]) + '</a>'
	
	return outStr	
			







def process(url):
	
	# fetch info
	
	infor = urlopen('http://api.tumblr.com/v2/blog/' + url + '/info?api_key=' + apiKey).read()
	info = json.loads(infor)['response']['blog']
	postCount = info['posts']
	# pageCount = int(ceil(float(postCount)/20))
	
	if not os.path.exists(outDir):
		os.makedirs(outDir)
	
	
	
	for i in range(0, postCount, pageSize):
		outFname = str(i).zfill(len(str(postCount))) + '.html'
		with open(outDir + '/' + outFname, 'w') as outf:
			
			# set up file
			
			outf.write('<html>\n<head><title>Tumblr: ' + ufix(info['name']) + ' (' + str(i) + '-' + str(min(i+pageSize, postCount)) + ')</title><style type="text/css">')
			outf.write('''
		.question {width:480px;  background-color:#a1c4e6; color:#0b0536;
		font-style:italic; padding:10px; -moz-border-radius:5px; border-radius:5px;}
		''')
			outf.write('</style></head></html>')
			outf.write('<body>\n\n')
			outf.write('<div class="infoblock"><h1 class="maintitle">' + ufix(info['name']) + ' (' + str(i) + '-' + str(min(i+pageSize, postCount)) + ')</h1>\n')
			outf.write('<h3 class="selftitle"><a href="' + ufix(info['url']) + '">' + ufix(info['title']) + '</a></h3>\n')
			outf.write('<p class="selfdescr">' + ufix(info['description']) + '</p>\n')
			outf.write('</div>\n<br>')
			if(i > 0):
				outf.write('<a href="' + str(i-pageSize).zfill(len(str(postCount))) + '.html">Previous</a> ')
			if(i + pageSize < postCount):
				outf.write('<a href="' + str(i+pageSize).zfill(len(str(postCount))) + '.html">Next</a> ')
			outf.write('<br><br><br>\n\n\n\n<hr>')
			
			
			
			
			# fetch and parse pages
			
			baseurl = 'http://api.tumblr.com/v2/blog/' + url + '/posts?api_key=' + apiKey + '&reblog_info=true&offset='
			for p in range(i, min(i+pageSize, postCount), 20):
				progStr = 'Fetching posts {0}-{1} of {2} to \'{3}\'.'.format(p, min(p+20, postCount), postCount, outFname)
				progress(progStr)
				
				pgurl = baseurl + str(p)
				pgr = urlopen(pgurl).read()
				
				posts = json.loads(pgr)['response']['posts']
						
				filtered = [x for x in posts if filterBy(x)]
				
				for post in filtered:
					posttime = datetime.fromtimestamp(post['timestamp']).ctime()
					
					outf.write('<div class="post">\n<div class="content">\n\n')
					outf.write(formatPost(post))
					outf.write('\n\n</div>\n\n\n')
					
					outf.write('<p class="posturl">\n')
					outf.write('<a href="' + post['post_url'] + '">' + posttime + '</a>\n')
					outf.write('</p>')
					
					outf.write('\n\n</div><hr><br><br>\n\n\n')
			
			
			
			# finish
			
			if(i > 0):
				outf.write('<a href="' + str(i-pageSize).zfill(len(str(postCount))) + '.html">Previous</a> ')
			if(i + pageSize < postCount):
				outf.write('<a href="' + str(i+pageSize).zfill(len(str(postCount))) + '.html">Next</a>')
			
			outf.write('<br><br>')
			outf.write('\n\n</body></html>')
	
	print 'Done!'
	
process(url)