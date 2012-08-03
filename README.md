Tumblrback-Sans
===============

Scrape tumblrs, without all the reblogs.

Consists of a single Python script, which will only run on Python 2.x. (Porting to 3.x should be straightforward.)

Usage: Run it as `python tumblrback.py`, then enter the domain you wish to scrape. A folder will be created in the current directory, into which HTML files with scraped posts will be generated. The script will report its progress as it goes.

By default, each HTML file will contain those non-reblog posts among 500 posts on the blog. To raise or lower that number, edit the variable 'pageSize' in the script.

