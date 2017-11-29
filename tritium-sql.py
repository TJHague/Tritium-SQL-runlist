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
# Parse dump file from start of run script here
# Turn the raw info into an insert statement
#######################################################

runnum = #placeholder

insert_query = #placeholder

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
