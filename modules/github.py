#!/usr/bin/env python
"""
github.py - Phenny Github Module
Author: Randy Nance, randynance.io
About: http://inamidst.com/phenny/
"""

import requests
import json

def github(phenny, input):
    """.issue <issue id> [owner/repo] [custom value] | .pr <pr id> [owner/repo] | repo defaults to hut/ranger | custom values: assignee, locked, milestone, created_at, updated_at, closed_at, closed_by, body; pr only values: merged_by, merged_at
    """
    req = str(input.split()[0])
    Id = str(input.split()[1])
    if len(input.split()) > 2:
        repo = str(input.split()[2])
    else:
        repo = 'hut/ranger'
    if req == '.issue':
        i = requests.get('https://api.github.com/repos/' + repo + '/issues/' + Id)
    elif req == '.pr':
        i = requests.get('https://api.github.com/repos/' + repo + '/pulls/' + Id)
    if i.ok:
        item = json.loads(i.text or i.content)
        if req == '.pr' and item['merged']:
            state = 'merged'
        else:
            state = str(item['state'])
        user = str(item['user']['login'])
        title = str(item['title'])
        url = str(item ['html_url'])
        comments = str(item['comments'])
        custom = {}
        if len(input.split()) > 3:
            for i in input.split()[3:]:
                try:
                    if isinstance(item[i], dict):
                        custom[str(i)] = item[str(i)]['login']
                    else:
                        custom[str(i)] = item[str(i)]
                except:
                    phenny.say('Could not find value for ' + str(i))
        string = "\x0305" +repo + '\x0355 #' + Id + '\x0399 |\x0309 by ' + user + '\x0399 | ' + title + ' | ' + url + '\x0307 (' + comments + ' comments)\x0310 [' + state + ']'
        for j in custom:
            string += '\x0399 | \x0306[' + str(j) + '] \x0312' + str(custom[j])
        phenny.say(string)
    else:
        phenny.say('#' + Id + ' not found for repo ' + repo)
github.commands = ['issue', 'pr']
if __name__ == '__main__': 
   print(__doc__.strip())
