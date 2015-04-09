from instagram.client import InstagramAPI
from instagram.bind import InstagramAPIError
import sys
import pickle
import time

def get_recent_media(user_id):
	all_media = []
	recent_media = []
	max_id = None
	counter = 0
	while (recent_media is not None):
		try:
			if (max_id is not None):
				recent_media, next_ = api.user_recent_media(user_id=user_id, max_id=max_id)
			else:
				recent_media, next_ = api.user_recent_media(user_id=user_id)
			for media in recent_media:
				print media
				all_media.append(media)
			if len(recent_media) > 19:
				max_id = recent_media[-1].id.split('_')[0]
			else:
				break
		except InstagramAPIError as e:
			print e
			if (e.status_code == 429):
				print "Rate limit reached"
				recent_media = []
				time.wait(60)
			elif (e.status_code == 502):
				"Unable to parse response"
				break
			else:
				break
	print "Found %d" %len(all_media)
	media_counts.append(len(all_media))
	pickle.dump(all_media, save_file)

if __name__ == '__main__':
	media_counts = []
	access_token = sys.argv[1]
	user_ids_file = sys.argv[2]
	output_file = sys.argv[3]
	api = InstagramAPI(access_token=access_token)
	save_file = open(output_file, 'wb')

	#get_recent_media("47791647")

	user_ids = []
	with open(user_ids_file, 'r') as id_file:
		for line in id_file.readlines():
			user_ids.append(line.rstrip('\n'))
	print user_ids

	# stopped at 10051934
	# media counts [2944, 4328, 279, 1501, 1282, 765, 2445, 886, 1798, 234, 2058, 1168,
	# 64, 2375, 1388, 852, 1142, 1039, 449, 771, 977, 2910, 442, 1228, 591, 4820, 4963, 14073, 4280]
	for user_id in user_ids:
		print "Crawling %s" %user_id
		get_recent_media(user_id)
		print "Rate limit %s" %api.x_ratelimit_remaining
		print media_counts

