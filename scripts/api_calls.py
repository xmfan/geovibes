# -*- coding: utf-8 -*-

import requests
import json

from collections import namedtuple
'''
NEWS
====
value: [
{
name: string
url: string
image: { thumbnail: 
            { contentUrl: string
              width: int
              height: int
            }
       }
description: string
about: [ { readLink: string
           name: string
         }
       ]
mentions: [{ name: string }]
provider: [ {_type: string, name: string} ]
datePublished: date %Y-%m%dT%hh:mm:ss
category: string
}
]

SAMPLE:
{"name": "Snap Is Using Vending Machines for Its New Camera Glasses", 
"url": "http:\/\/www.bing.com\/cr?IG=EFB171B8ABC94328B7EE4689A0BB20D9&CID=3F96AB4DDC906F9A3574A286DDA16EAF&rd=1&h=acQNdE7k_qK5fn0QyKfaDgISEoU4tCoAUSGF_bG8KrA&v=1&r=http%3a%2f%2fwww.nbcnews.com%2ftech%2ftech-news%2fsnap-using-vending-machines-its-new-camera-glasses-n682696&p=DevEx,5210.1", 
"image": {"thumbnail": {"contentUrl": "https:\/\/www.bing.com\/th?id=ON.01B69C301515AEFBF1DD7823834D5DEE&pid=News", "width": 320, "height": 210}}, 
"description": "What do a sandwich, soda and Spectacles have in common? You can buy all three from vending machines. Spectacles - the camera glasses from the company formerly known as Snapchat — went up for sale in a bright yellow vending machine on Thursday.",
"about": [{"readLink": "https:\/\/api.cognitive.microsoft.com\/api\/v5\/entities\/90fd2ef2-8123-de59-2b1f-ccd033454a4a", "name": "NBC News"}, {"readLink": "https:\/\/api.cognitive.microsoft.com\/api\/v5\/entities\/3df07628-b8da-2cb7-7d61-95c268a5d178", "name": "Camera"}, {"readLink": "https:\/\/api.cognitive.microsoft.com\/api\/v5\/entities\/97410ae3-4d3a-cf91-43d0-2ad5986953e4", "name": "Vending machine"}],
"mentions": [{"name": "NBC News"}, {"name": "Camera"}, {"name": "Vending machine"}], 
"provider": [{"_type": "Organization", "name": "NBC News"}],
"datePublished": "2016-11-12T12:42:00",
"category": "Products"},

SENTIMENT
=========
{
  "documents": [
    {
      "score": 0.0,
      "id": "string"
    }
  ]
}

SAMPLE:

{"documents":[{"score":0.9572602,"id":"1"}],"errors":[]}

KEY PHRASES:

[{u'keyPhrases': [u'Spectacles', u'bright yellow vending machine', u'sale', u'soda', u'Los Angeles', u'camera glasses', u'company', u'Thursday', u'vending machines', u'sandwich'], u'id': u'1'}]
'''

headers = {'Ocp-Apim-Subscription-Key':'782e68122d8742c091f6dee73fc2d270'}

r = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/news/', headers=headers)
print len(r.json()['value'])

#headers = {'Ocp-Apim-Subscription-Key':'7b20e9c1ffa8470cab2e3b6245148cf6',
#        'Content-Type': 'application/json',
#        'Accept': 'application/json'
#        }
#payload = {
#    "documents": [
#        {
#            "language": "en",
#            "id": "1",
#            "text": "What do a sandwich, soda and Spectacles have in common? Los Angeles You can buy all three from vending machines. Spectacles - the camera glasses from the company Okalitsa Balatniki formerly known as Snapchat — went up for sale in a bright yellow vending machine on Thursday"
#        }
#     ]
#}
#
#r = requests.post('https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases', json = payload, headers=headers)
#print r.json()['documents']
