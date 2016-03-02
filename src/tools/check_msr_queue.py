
# --------------------------------------------------

import sys
import os

branch = sys.argv[1]

branch_dir = os.path.join(os.path.expanduser('~'), 'active', branch)

if not os.path.isdir(branch_dir):
    raise Exception('Branch directory does not exist')


config_dir = os.path.join(branch_dir, 'asdf', 'src', 'tools')
sys.path.insert(0, config_dir)

from config_utility import *

config = BranchConfig(branch=branch)


# --------------------------------------------------

import pymongo

client = pymongo.MongoClient(config.server)

msr = client[config.det_db].msr

request_count = msr.find({'status':0}).count()

# make sure request was found
if request_count > 0:
    print "ready"

else:
    print "empty"