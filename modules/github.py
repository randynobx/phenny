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

def commits(phenny, input):
    """.commits [branch] [owner/repo] | defaults: branch=master, owner/repo=hut/ranger
    """
    # set default values
    branch = 'master'
    repo = 'hut/ranger'
    if len(input.split()) > 1:
        branch = str(input.split()[1])
    if len(input.split()) > 2:
        repo = input.split()[2]

    i = requests.get('https://api.github.com/repos/' + repo + '/git/refs/heads/' + branch)
    if i.ok:
        head = json.loads(i.text or i.content)
        commitHash = head['object']['sha']
        j = requests.get('https://api.github.com/repos/' + repo + '/git/commits/' + commitHash)
        if j.ok:
            commit = json.loads(j.text or j.content)
            author = commit['author']['name']
            msg = commit['message']
            date = commit['committer']['date']
            url = commit['html_url']

            string = "\x0305" +repo + '\x0355 ' + branch + '\x0399 | \x0307' + date + '\x0399 |\x0309 authored by ' + author + '\x0399 | ' + msg + ' | ' + url + '\x0307'
            phenny.say(string)
        else:
            phenny.say("issue fetching latest commit info")
    else:
        phenny.say("issue fetching branch info")
commits.commands = ['commits', 'lc']

if __name__ == '__main__': 
   print(__doc__.strip())
