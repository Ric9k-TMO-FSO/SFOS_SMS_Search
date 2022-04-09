#!/usr/bin/env python3

#Search for text into SFOS messages.

#Script from
#https://github.com/Ric9k-TMO-FSO/SFOS_SMS_Search

import sqlite3
import sys # For variables passed to the script
from os.path import exists # To verify if the file exists
import os #Launch shell commands, to check if we are root or user
#import subprocess #Launch shell commands, to check if we are root or user
import datetime #To convert epoch in a readable date/time format
#args = ['a', 'a']
args = sys.argv


debug = 0
firstNameString = ''
lastNameString = ''

#Check if executed as root
command = ("whoami")
whoAmI = os.popen(command).read()

print('  ')
print('Sailfish Messages Search')
print('-----------------------------')
print('  ')
print('-t     display text found into messages')
print('  ')
print('Accents sensitive search.')
print('  Wildcards:')
print('  Use "_" for single character')
print('  Use "%" for multiple characters')
print('  ')

if debug == 1:
    searchTerms = ['Hello', '', '']
    searchNames = ''
elif debug == 0:
    #Ask user to enter the terms he want to search
    searchTerms = ['']
    newTerm = 'a'
    i = 0
    while (newTerm != ""):
        i += 1
        if i == 1:
            newTerm =  input("Search for: ")
            if newTerm == '':
                print('Nothing to search, aborting.')
                exit()
        elif i > 1:
            print('Add a search term,')
            newTerm =  input("or leave empty if done: ")
        searchTerms.append(newTerm)
        #We allow a max of 3 terms
        if len(searchTerms) == 4:
            break

    #Filter by name
    print('')
    print('This works only if the script is')
    print('ran as root. Leave empty otherways')
    searchName =  input('''Contact's name: ''')



msgDb = '/home/defaultuser/.local/share/commhistory/commhistory.db' #Real
#msgDb = './commhistory.db' #Test
contactsDb = '/home/defaultuser/.local/share/system/privileged/Contacts/qtcontacts-sqlite/contacts.db' #Real
#contactsDb = './contacts.db' #Test

#Verify if needed files exist, try with nemo username (Not sure this works, actually!)
if not exists(msgDb) and not exists(contactsDb):
    print('No defaultuser db. Trying nemo')
    msgDb = '/home/nemo/.local/share/commhistory/commhistory.db' #Real
    contactsDb = '/home/nemo/.local/share/system/Contacts/qtcontacts-sqlite/contacts.db'
    if not exists(msgDb) and (contactsDb):
        print('Messages database cannot be found. Aborting')

#Open databases
msgConnection = sqlite3.connect(msgDb)
msgCursor = msgConnection.cursor()

if 'root' in whoAmI:
    print('hello root')
    contactConnection = sqlite3.connect(contactsDb)
    contactCursor = contactConnection.cursor()

#Remove empty entries and make all lowercase
searchTermsCleaned = []
for element in searchTerms:
    if element != '':
        searchTermsCleaned.append(element)

if len(searchTermsCleaned) == 1:
    #print(1)
    msgCursor.execute("""SELECT remoteUid, endTime, freeText FROM Events WHERE (freeText LIKE '%'||?||'%')""", [searchTermsCleaned[0]])
    foundTextTable = msgCursor.fetchall()
elif len(searchTermsCleaned) == 2:
    #print(2)
    msgCursor.execute("""SELECT remoteUid, endTime, freeText FROM Events WHERE (freeText LIKE '%'||?||'%' AND freeText LIKE '%'||?||'%')""", [searchTermsCleaned[0], searchTermsCleaned[1]])
    foundTextTable = msgCursor.fetchall()
elif len(searchTermsCleaned) == 3:
    #print(3)
    msgCursor.execute("""SELECT remoteUid, endTime, freeText FROM Events WHERE (freeText LIKE '%'||?||'%' AND freeText LIKE '%'||?||'%' AND freeText LIKE '%'||?||'%')""", [searchTermsCleaned[0], searchTermsCleaned[1], searchTermsCleaned[2]])
    foundTextTable = msgCursor.fetchall()

#Search for correspondant's name, message date, text

numbersTable = []
numbersTable.append(0)
resultCount = -1
for textSearchLine in foundTextTable:
    
    if 'root' in whoAmI:
        contactCursor.execute("SELECT firstName, lastName FROM 'Names' WHERE (contactID = (SELECT contactId FROM phoneNumbers WHERE normalizedNumber = ?)) ",[  textSearchLine[0][-8:] ])    
        foundNames = contactCursor.fetchall()
        #Display names correctly
        firstNameString = str(','.join([str(i[0]) for i in foundNames]))
        lastNameString = str(','.join([str(i[1]) for i in foundNames]))
        if lastNameString == 'None':
            lastNameString = ''
    #Convert epoch time to a more readable time format
    msgTime = datetime.datetime.fromtimestamp(textSearchLine[1])
    #Empty lastName if None
    #Display the found message only if the given name is contained to either the first name or the last name.
    if ( (searchName).lower() in (firstNameString).lower() or (searchName).lower() in (lastNameString).lower() ) or 'root' not in whoAmI:
        resultCount += 1
        print('Result #',resultCount,'---------')
        print(msgTime)
        print(firstNameString+' '+lastNameString)
        print(textSearchLine[0])# Phone Number
        if len(args) > 1 and args[1] == '-t':
            print(textSearchLine[2]) #Text
            
    #Launch jolla-messages into the chosen conversation - Not always working        
    #Temporarly store the search number aside phone number
    #numbersTable.append(textSearchLine[0])
#print('Go to conversation?')
#print('This will create a new message.')
#print('''Don't press send!''')
#wantedNumber = int(input('Enter result #:'))
#command = ('dbus-send --type=method_call --dest=org.nemomobile.qmlmessages / org.nemomobile.qmlmessages.startSMS array:string:"'+numbersTable[wantedNumber]+'" string:" "')
#os.system(command)

if msgConnection:
    msgConnection.close()
if 'root' in whoAmI and contactConnection:
    contactConnection.close()
