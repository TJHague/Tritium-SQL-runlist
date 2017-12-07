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
#EXP = "TEST"
EXP = "PRECOMMISSIONING"
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
  print 'This run number does not exist in the run_list. Please email Tyler Hague (tjhague@jlab.org) and include what run number this message appeared on.'
  sys.exit(1)

#######################################################
# Extract end of run info to update the database
#######################################################

#Extracting end of run comments
try:
    if right_arm:
        comment_file = open("/adaqfs/home/adaq/scripts/.runendR.comments","r")
    else:
        comment_file = open("/adaqfs/home/adaq/scripts/.runendL.comments","r")
    found = False
    end_comment = ''
    for line in comment_file:
        if not found:
            i = 0
            while i<(len(line)-13) and not found:
                if line[i:i+13]=="comment_text=":
                    found = True
                    end_comment = line[i+13:].rstrip() + ' '
                i += 1
        else:
            end_comment += line.rstrip() + ' '
    end_comment = end_comment.rstrip()
    comment_file.close()
except IOError:
    print 'The end of run comment file seems to be missing. Please email Tyler Hague (tjhague@jlab.org) and include what run number this message appeared on.'

#Extract time, events, trigger totals, and charge
try:
    halog_com = open("/adaqfs/home/adaq/epics/runfiles_ar40/halog_com_" + runnum + ".epics","r")
    for line in halog_com:
        if line.startswith("EVENTS   : "):
           events = line[11:]
        if line.startswith("TIME     : "):
            time = line[11:]
        if line.startswith("TRIGGER TOTALS:"):
            found_triggers = True
        if found_triggers:
            for c in line:
                i=-1
                if c==':':
                    triggers[i] = ''
                    i += 1
                if c.isdigit():
                    triggers[i] += c
            found_triggers = False
        if line.startswith("APPROXIMATE BCM CHARGES"):
            found_charge = True
        if found_charge:
            i = 0
            charge = ''
            if line[i:i+6] == 'Unser:':
                i=i+7
                if line[i].isdigit() or line[i]=='.' and not charge_done:
                    charge += line[i]
                else:
                    charge_done = True
            found_charge = False
    halog_com.close()
except IOError:
    print 'The halog comment file seems to be missing. Please email Tyler Hague (tjhague@jlab.org) and include what run number this message appeared on.'

#######################################################
# Create and execute update statement
#######################################################

update_query = "UPDATE " + EXP + "runlist SET end_time=NOW(), end_comment=\"" + end_comment + "\", "
update_query += "events=" + events + ", "
update_query += "time_mins=" + time + ", "
update_query += "charge=" + charge + ", "
update_query += "T1_count=" + triggers[1] + ", "
update_query += "T2_count=" + triggers[2] + ", "
update_query += "T3_count=" + triggers[3] + ", "
update_query += "T4_count=" + triggers[4] + ", "
update_query += "T5_count=" + triggers[5] + ", "
update_query += "T6_count=" + triggers[6] + ", "
update_query += "T7_count=" + triggers[7] + ", "
update_query += "T8_count=" + triggers[8] + " "
update_query += "WHERE run_number=" + runnum

cursor.execute(update_query)

#print insert_query
print 'Successfully updated the MySQL run list! Have an awesome shift!'
