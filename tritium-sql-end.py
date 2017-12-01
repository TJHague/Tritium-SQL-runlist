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

#Uncomment the current experiment so that the correct table is filled.
EXP = "TEST"
#EXP = "PRECOMMISSIONING"
#EXP = "COMMISSIONING"
#EXP = "MARATHON"
#EXP = "SRC"
#EXP = "EP"
#EXP = "EK"

if len(sys.argv)==2:
    if sys.argv[1]=='right':
        right_arm = True
    elif sys.argv[1]=='left':
        right_arm = False
    else:
        print 'The second argument must be \'right\' or \'left\''
        sys.exit(1)
else:
    print 'Please specify if the code is being run for \'right\' or \'left\''
    sys.exit(1)

#Read in the run number from the rcRunNumber file
try:
    if right_arm:
        runnum_file = open("/adaqfs/home/adaq/datafile/rcRunNumberR","r")
    else:
        runnum_file = open("/adaqfs/home/adaq/datafile/rcRunNumber","r")
    runnum = runnum_file.readline()
    runnum = runnum.rstrip() #Removes \n end of line character and any trailing whitespace. There shouldn't be any in this case, but just in case
    runnum_file.close()
except IOError:
    print 'Run Number not found by the MySQL script. Please email Tyler Hague (tjhague@jlab.org) and include what run number this message appeared on.'
    sys.exit(1) #Exit. Run number is the primary key, so an insert cannot be made without it

#######################################################
# Try connecting to the database. Exit if fail.
#######################################################

try:
  db = MySQLdb.connect(host='halladb.jlab.org', user='triton', passwd='FakePassword', db="triton")
except MySQLdb.Error:
  print 'Could not connect to database. Please ensure that the paper runlist is kept up-to-date. Please email Tyler Hague (tjhague@jlab.org) and include what run number this message appeared on.'
  sys.exit(1)

#######################################################
# Ensure that the run number exists in the table
#   We are updating the entry.
#######################################################

cursor = db.cursor()

unique_test = "SELECT run_number FROM " + EXP + "runlist where run_number=" + runnum

#Get number of entries with the current run number as a uniqueness test
#Exit if not unique

cursor.execute(unique_test)
Evts = cursor.fetchall()
evtAll = [Evt[0] for Evt in Evts]
nEvtAll = len(evtAll)

if nEvtAll==0:
  print 'This run number is already in existence in the run_list. Please email Tyler Hague (tjhague@jlab.org) and include what run number this message appeared on.'
  sys.exit(1)

#######################################################
# Create and execute update statement
#######################################################

update_query = "UPDATE " + EXP + "runlist SET end_time=NOW() WHERE run_number=" + runnum

cursor.execute(update_query)

#print insert_query
print 'Successfully inserted into the MySQL run list! Have an awesome shift!'
