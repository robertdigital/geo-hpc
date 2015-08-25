# prep queue requests

# need better error handling /notification for
# what are currently "fatal" errors
# at minimum: update request status so 
# we are aware and can check it or restart it

import os
import sys
import time

sys.stdout = sys.stderr = open(os.path.dirname(os.path.abspath(__file__)) +'/processing.log', 'a')

from queue import queue
from cache import cache
from documentation import doc

queue = queue()
cache = cache()
doc = doc()

queue.cache = cache
queue.doc = doc

request_id = 0

print '\n------------------------------------------------'
print 'Prep Script'
print time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())

# get next request in queue based on priority and submit time
# returns status of search, request id if search succeeds, and request data
gn_status, request_id, request_obj = queue.get_next(-1)

if not gn_status:
   sys.exit("Error while searching for next request in queue")
elif request_id == None:
   sys.exit("Prep queue is empty")


print 'Request id: ' + request_id


# update status to being processed 
# (without running extracts: 2, with runnning extracts: 3)
us = queue.update_status(request_id, 2)


# send initial email
p_message = "Your data extraction request (" + request_id + ") has been received. You can check on the status of the request via devlabs.aiddata.wm.edu/DET/status/#"+request_id +". Results can be downloaded from the same page when they are ready."
queue.send_email("aiddatatest2@gmail.com", request_obj["email"], "AidData Data Extraction Tool Request Received ("+request_id+")", p_message)

# check results for cached data
# run missing extracts if run_extract is True
cr_status, cr_count = cache.check_request(request_obj, False)

if not cr_status:
    queue.quit("Error while checking request cache")


# if extracts are cached then build output
if cr_count == 0:
    print "finishing request"

    queue.build_output(request_id, False)

else:
    print "finishing prep"
    # add cr_count to request so number of needed extracts 
    # can be factored into queue order (?)
    # 

    # update status 1 (ready for processing)
    us = queue.update_status(request_id, 1)

