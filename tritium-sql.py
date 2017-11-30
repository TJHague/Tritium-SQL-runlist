#!/usr/bin/python

#######################################################
# A python script to insert run information into the
#   tritium MySQL run list.
# Author: Tyler Hague
# Created: 28 Nov 2017
#######################################################

import sys
import os
import string
import MySQLdb

serverAddress = 'halladb.jlab.org'

#######################################################
# Try connecting to the database. Exit if fail.
#######################################################

try:
  db = MySQLdb.connect(host=serverAddress, user='triton', passwd='FakePassword', db=triton)
except MySQLdb.Error:
  print 'Could not connect to database. Please ensure that the paper runlist is kept up-to-date. Please email Tyler Hague (tjhague@jlab.org) and include what run number this message appeared on.'
  sys.exit(1)

#######################################################
# Interact with the caget script to access
#   epics variables
#######################################################

#Read in the run number from the rcRunNumber file
runnum_file = open("/adaqfs/home/adaq/datafile/rcRunNumber","r")
runnum = runnum_file.readline()
runnum = runnum.rstrip() #Removes \n end of line character and any trailing whitespace. There shouldn't be any in this case, but just in case
runnum_file.close()

#prep a query to request EPICS variables. Change the third value for a new request
caget_query = ['/adaqfs/home/adaq/scrips/caget','-t','']

start_time = ""
end_time = ""
target = ""
sieve = 0
raster = ""
beam_energy = 0.0
momentum = 0.0
angle = 0.0
off_x = 0.0
off_y = 0.0
off_z = 0.0
comment = ""
insert_query = ""

#######################################################
# Execute the insert statment
# Ensure that the run number does not exist in the
#   table already. Runnum is a unique key.
#######################################################

cursor = db.cursor()

unique_test = "SELECT run_number FROM run_list where run_number="
unique_test = unique_test + runnum

#Get number of entries with the current run number as a uniqueness test
#Exit if not unique

cursor.execute(unique_test)
Evts = cursor.fetchall()
evtAll = [Evt[0] for Evt in Evts]
nEvtAll = len(evtAll)

if nEvtAll>0:
  print 'This run number is already in existence in the run_list. Please email Tyler Hague (tjhague@jlab.org) and include what run nimber this message appeared on.'
  sys.exit(1)

cursor.execute(insert_query)

print insert_query
print 'Successfully inserted into the MySQL run list! Have an awesome shift!'
