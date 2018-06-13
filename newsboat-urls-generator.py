from xml.dom.minidom import parseString
import requests
import argparse
import json

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--channel-id", help="your youtube channel id")
    parser.add_argument("-u", "--channel-url", help="youtube url channel to convert. needs channel username.")
    parser.add_argument("-v", "--verbose", help="verbose mode", action="store_true")

    args = parser.parse_args()

    feed_url = 'https://www.youtube.com/feeds/videos.xml?channel_id='

    if args.channel_id:
        generate_list(feed_url, args)
    elif args.channel_url:
        generate_url(feed_url, args)



def generate_list(feed_url, args):

    i = 0
    f = open('newsboat_urls', 'w+')
    api_key = 'AIzaSyBu8YAifpfHVbBR2wSbZ5a0Dp6WGEshy88'
    page_token = 'CDIQAQ'

    while True:
        
        request_url = 'https://www.googleapis.com/youtube/v3/subscriptions?' + \
                'pageToken=' + page_token + \
                '&part=snippet%2CcontentDetails&channelId=' + args.channel_id + \
                '&maxResults=50&key=' + api_key

        r = requests.get(request_url)
        channel_list = json.loads(r.text)

        for channel in channel_list['items']:
            
            channel_id = channel['snippet']['resourceId']['channelId']
            channel_title = channel['snippet']['title']

            if args.verbose:
                print('Generating for ' + channel_title)

            f.write(feed_url + channel_id + ' "Youtube" ' + '"!' + channel_title + '"\n')
            i += 1

        try:
            page_token = channel_list['nextPageToken']
        except KeyError:
            break


    f.write('\n"query:Youtube:tags # \\"Youtube\\""')
    print('\nDone! A total of ' + str(i) + ' channels written in newsboat_urls file')
    f.close()


def generate_url(feed_url, args):

    yt_url = "https://www.youtube.com/feeds/videos.xml"

    if 'user' in args.channel_url:
            payload = {'user':args.channel_url.split('/').pop()}
    else:
            payload = {'channel_id':args.channel_url.split('/').pop()}

    r = requests.get(yt_url, payload)
    dom = parseString(r.text)
    element = dom.getElementsByTagName('entry')[0]

    channel_id = element.getElementsByTagName('yt:channelId').pop().firstChild.data
    channel_title = element.getElementsByTagName('name').pop().firstChild.data

    print(feed_url + channel_id + ' "Youtube" ' + '"!' + channel_title + '"\n')



if __name__ == "__main__":
    main()
