# -*- coding: utf-8 -*-

import sys,getopt,datetime,codecs
import got3 as got
outputFile = open("output_got.txt", 'w+')

def main(argv):

	if len(argv) == 0:
		print('You must pass some parameters. Use \"-h\" to help.')
		return
		
	if len(argv) == 1 and argv[0] == '-h':
		print("""\nTo use this jar, you can pass the folowing attributes:
    username: Username of a specific twitter account (without @)
       since: The lower bound date (yyyy-mm-aa)
       until: The upper bound date (yyyy-mm-aa)
 querysearch: A query text to be matched
   maxtweets: The maximum number of tweets to retrieve

 \nExamples:
 # Example 1 - Get tweets by username [barackobama]
 python Exporter.py --username "barackobama" --maxtweets 1\n

 # Example 2 - Get tweets by query search [europe refugees]
 python Exporter.py --querysearch "europe refugees" --maxtweets 1\n

 # Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']
 python Exporter.py --username "barackobama" --since 2015-09-10 --until 2015-09-12 --maxtweets 1\n
 
 # Example 4 - Get the last 10 top tweets by username
 python Exporter.py --username "barackobama" --maxtweets 10 --toptweets\n""")
		return
 
	try:
		opts, args = getopt.getopt(argv, "", ("username=", "since=", "until=", "querysearch=", "toptweets", "maxtweets="))
		
		tweetCriteria = got.manager.TweetCriteria()
		
		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg
				
			elif opt == '--since':
				tweetCriteria.since = arg
				
			elif opt == '--until':
				tweetCriteria.until = arg
				
			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg
				
			elif opt == '--toptweets':
				tweetCriteria.topTweets = True
				
			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)

		
		print('Searching...\n')
		
		def receiveBuffer(tweets):
			for t in tweets:
				x={}
				x['text'] = t.text
				x['retweet_count'] = t.retweets
				x['favorite_count'] = t.favorites
				user={}
				user['id'] = t.id
				user['screen_name'] = t.username
				x['user'] = user
				x['geo'] = t.geo
				x['time'] = t.date				
				#print(t.date)
				try:
					outputFile.write(str(x))
					outputFile.write("\n")
				except:
					pass
				#outputFile.write(('\n%s;\n%s;\n%d;\n%d;\n"%s";\n%s;\n%s;\n%s;\n"%s";\n%s\n' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))
			outputFile.flush();
			print('More %d saved on file...\n' % len(tweets))
		
		got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
		
	except arg:
		print('Arguments parser error, try -h' + arg)
	finally:
		outputFile.close()
		print('Done. Output file generated "output_got.txt".')

if __name__ == '__main__':
	main(sys.argv[1:])