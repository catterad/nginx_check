#!/usr/bin/python

import sys, getopt, time
import json
import urllib2
from array import *

#data = json.load(urllib2.urlopen('http://10.108.111.214:3333/status/server_zones/VOD'))
#print data

Four = array('i',[0,0])
Five = array('i',[0,0])
Three = array('i',[0,0])
Disc = array('i',[0,0])


def main(argv):
	zone = ''
	host = ''
	s = ""
	bad = 10
	error = 0
	try:
	  opts, args = getopt.getopt(argv,"hz:H:b:",["zone","host","bad"])
	except getopt.GetoptError:
	 print 'nginx_upstream.py -z <server zone> -H <host:port> -b <bad threshold>'
	 sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
		  print 'nginx_upstream.py -z <server zone> -H <host:port> -b <bad threshold>'
		  sys.exit()
                elif opt in ("-z", "--zone"):
		 zone = arg
		elif opt in ("-H", "--host"):
		 host = arg
		elif opt in ("-b", "--bad"):
		 bad = int(arg)
	#print "Upstream is ", upstream
	#print "Host is ", host
        seq = ("http://", host, "/status/server_zones/", zone);
	s = s.join(seq) 
	#print "trying ", s
	try:
	 data = json.load(urllib2.urlopen(s, timeout = 3))
	except getopt.GetoptError:
	 print "Connection Error"
	except ValueError:
	 print "Decoding JSON has failed"
	 sys.exit(2)
	except urllib2.URLError, e:
	 print "Warning - Unable to connect to host", host
	 sys.exit(1)
	except socket.timeout, e:
	 print "timeout"
	 sys.exit(2)

	Four[0] = int(data["responses"]["4xx"])
	Five[0] = int(data["responses"]["5xx"])
        Three[0] = int(data["responses"]["3xx"])
	Disc[0] = int(data["discarded"])

	time.sleep(2)

	try:
	 data = json.load(urllib2.urlopen(s))
	except getopt.GetoptError:
         print "Connection Error"

	Four[1] = int(data["responses"]["4xx"])
        Five[1] = int(data["responses"]["5xx"])
        Three[1] = int(data["responses"]["3xx"])
	Disc[1] = int(data["discarded"])


	AFour = Four[1] - Four[0]
	AFive = Five[1] - Five[0]
	AThree = Three[1] - Three[0]
	ADisc = Disc[1] - Disc[0]

	if AFour >= bad:
		print bad
		error = 1
	elif AFive >= bad:
		print bad
		error = 1
	elif AThree >= bad:
		print bad
		error = 1
	elif ADisc >= bad:
		print bad
		error = 1

	if error == 1:
	  print "ERROR LEVEL CRITICAL: / %d-4xx=%d, %d-5xx=%d, %d-3xx=%d, %d-Discards-%d|4xx=%da 3xx=%da 5xx=%da discard=%da" % (Four[0], Four[1], Five[0], Five[1], Three[0], Three[1], Disc[0], Disc[1], Four[0],Three[0],Five[0],Disc[0])
	  sys.exit(2)
	else:
	  print "ERROR LEVEL OK: / 4xx=%d, 5xx=%d, 3xx=%d, Discards=%d|4xx=%da 3xx=%da 5xx=%da discard=%da" % (AFour, AFive, AThree, ADisc, Four[0],Three[0],Five[0],Disc[0])
	  sys.exit(0)


if __name__ == "__main__":
	main(sys.argv[1:]) 

