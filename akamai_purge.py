#!/usr/bin/python
#Version:  1.0                                                                    
#Info: Script to Purge the urls from Akamai CDN using akamai API's and this script use Jenkins as it's frontend.
#	   /var/tmp/jenkins/workspace/Akamai_Purge/purge file contains the URLs to purge.
#Author : Saurav Yadav 

import os
import subprocess
import urllib2, base64, json, time, sys
sys.stdout.flush()

proc = subprocess.Popen(["/usr/local/python/bin/ccu_purge --domain=production --urls=/var/tmp/jenkins/workspace/Akamai_Purge/purge --email=email-id@gmail.com --type=arl --username=akamaipurge@gmail.com --password=abcd1234"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
prog = out.split('progress_uri=')[1]
print "progressUri = https://api.ccu.akamai.com" + prog + "\n"

while True:
    req2 = urllib2.Request("https://api.ccu.akamai.com" + prog)
    base64string = base64.encodestring('%s:%s' % ("akamaipurge@gmail.com","abcd1234")).replace('\n', '')
    req2.add_header("Authorization", "Basic %s" % base64string)
    tmp = urllib2.urlopen(req2).read()
    status = eval(tmp.replace("null","None"))
    if status["purgeStatus"] == "Done":
      print "purge complete"
      sys.exit(0)
    else:
      print time.ctime() + '\tpurge still running...'
      #sys.stdout.write(time.ctime() + '\tpurge still running...')
      sys.stdout.flush()
      time.sleep(30)
