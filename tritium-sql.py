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

#define variables needed to go in database
runnum = 0
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

with open("sql.dat","r") as file:
    data = file.readlines()

#Loop over the lines looking for keywords to denote which variable is listed
for line in data:
    words = line.split()
    if words[0]=="runnum":
        runnum = words[1]
    elif words[0]=="start_time":
        start_time = words[1]
    elif words[0]=="end_time":
        end_time = words[1]
    elif words[0]=="target":
        target = words[1]
    elif words[0]=="sieve":
        sieve = words[1]
    elif words[0]=="raster":
        raster = words[1]
    elif words[0]=="beam_energy":
        beam_energy = words[1]
    elif words[0]=="momentum":
        momentum = words[1]
    elif words[0]=="angle":
        angle = words[1]
    elif words[0]=="off_x":
        off_x = words[1]
    elif words[0]=="off_y":
        off_y = words[1]
    elif words[0]=="off_z":
        off_z = words[1]
    elif words[0]=="comment"
        for com in words:
            comment = comment + com


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
