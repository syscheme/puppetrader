#!/usr/bin/env python
import sys
import optparse
import tornado.httpclient
import simplejson, json
import urllib

"""
Get result string from tesseract API
https://github.com/guitarmind/tesseract-web-service/blob/master/tesseractclient.py
sample command line usage:
    python /opt/ocr/tesseractclient.py -a "http://localhost:1688/fetchurl" -i "http://www.greatdreams.com/666-magicsquare.gif"

"""
def ocrAPI(apiUrl, imageUrl):
    request = { 'url': imageUrl }
    post_data = json.dumps(request)

    headers = { 'Content-Type': 'application/json; charset=UTF-8' }
    http_client = tornado.httpclient.AsyncHTTPClient()
    http_client.fetch(apiUrl, handle_request, method = 'POST', headers = headers, body = post_data)
    print "Sending request: " + post_data
    tornado.ioloop.IOLoop.instance().start()

def handle_request(response):
    if response.error:
        print "Error: ", response.error
    else:
        print "Got response: " + response.body
    tornado.ioloop.IOLoop.instance().stop()

def main():
    parser = optparse.OptionParser()
    parser.add_option('-a', '--api-url', dest='apiUrl', help='the URL of RESTful tesseract web service.')
    parser.add_option('-i', '--image-url', dest='imageUrl', help='the URL of image to do OCR.')
    (options, args) = parser.parse_args()

    if not options.apiUrl:   # if apiUrl is not given
        parser.error('api-url not given')
    if not options.imageUrl:   # if imageUrl is not given
        parser.error('image-url not given')

    # call tesseract API
    ocrAPI(options.apiUrl, options.imageUrl)
 
if __name__ == '__main__':
    main()

