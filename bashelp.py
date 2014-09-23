#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
import argparse
import shutil
import subprocess
import textwrap

PROGRAM_NAME='bashelp'
PROGRAM_VERSION='1.0'
USER_DATA_FOLDER=os.path.expanduser("~")+'/.'+PROGRAM_NAME
DATABASE_PATH=USER_DATA_FOLDER+'/CommandsDatabase.db'
TMPFILE_PATH='/tmp/'+PROGRAM_NAME+'_TempCommandFile.txt'

#~ Costanti tutto maiuscolo+underscore
#~ Funzioni in maiuscolo, il resto in camelcase con l'iniziale minuscola 
#~ Tabelle in maiuscolo, colonne in camelcase con l'iniziale minuscola 

def OpenDatabase():
	dbConnection=sqlite3.connect(DATABASE_PATH)
	db=dbConnection.cursor()
	db.execute('PRAGMA foreign_keys=ON')
	return dbConnection

def DatabaseCommandExists(dbConnection, commandId):
	db=dbConnection.cursor()
	exists=db.execute('SELECT count(*) FROM Commands WHERE rowid=?',(commandId,)).fetchone()[0]
	return (False, True)[exists]
	
def DatabaseAddCommand(dbConnection, commandId, command, description):
	db=dbConnection.cursor()
	if commandId!=-1: 
		db.execute('INSERT INTO Commands (rowid,command,description) VALUES(?,?,?)', (commandId, command, description))
	else:
		db.execute('INSERT INTO Commands (command,description) VALUES(?,?)', (command, description))
	commandId=db.lastrowid
	return commandId
	
def DatabaseRemoveCommand(dbConnection, commandId): #non controlla che commandId esista
	db=dbConnection.cursor()
	db.execute('DELETE FROM Commands WHERE rowid=?',(commandId,)) #A cascata dovrebbe togliere tutti i tag corrispondenti
	return 0
	
def DatabaseAddTag(dbConnection, tag, commandId): #non controlla che commandId esista
	db=dbConnection.cursor()
	db.execute("INSERT INTO Tags (tag,commandId) VALUES(?,?)",(tag, commandId))
	return db.lastrowid

ISTTY=sys.stdout.isatty()
COLOR_BLUE='\033[94m' if ISTTY else ''
COLOR_GREEN='\033[92m' if ISTTY else ''
COLOR_RED='\033[91m' if ISTTY else ''
COLOR_DEFAULT='\033[0m' if ISTTY else ''
def ColorPrint( string , color, prefix='', suffix='' ): #Non è facile usarlo perchè spesso solo una parte va colorata!
	if color=='red':
		color=COLOR_RED
	elif color=='blue':
		color=COLOR_BLUE
	elif color=='green':
		color=COLOR_GREEN
	elif color=='default':
		color=COLOR_DEFAULT	
	print(prefix+color+string+COLOR_DEFAULT+suffix)	
	
def PrintCommand(dbConnection, commandId, ShowTags): #Non controlla che il comando esista
	db=dbConnection.cursor()
	(command,description)=db.execute('SELECT command, description FROM Commands WHERE rowid=?',(commandId,)).fetchone()
	ColorPrint( str(commandId), 'red', '', ': '+command )
	descriptionPrefix='\t'
	descriptionWrapper=textwrap.TextWrapper(initial_indent=descriptionPrefix, subsequent_indent=' '*(len(textwrap.fill(descriptionPrefix+'$',replace_whitespace=False))-1), width=70)
	ColorPrint( descriptionWrapper.fill( description ), 'blue' )
	if ShowTags:
		allTags=map(lambda x: COLOR_GREEN+x[0]+COLOR_DEFAULT,db.execute('SELECT tag FROM Tags WHERE commandId=?',(commandId,)).fetchall())
		tagsPrefix='\tTags: '
		tagsWrapper=textwrap.TextWrapper(initial_indent=tagsPrefix, subsequent_indent=' '*(len(textwrap.fill(tagsPrefix+'$',replace_whitespace=False))-1), width=90)
		print( tagsWrapper.fill(', '.join(allTags)) )
	print('')

COMMAND_TXT='Command: '
DESCRIPTION_TXT='Description: '
TAGS_TXT='Tags (each tag on a new line, starting from next line):\n'
def AddCommandFromFile( dbConnection, commandId, fileName ):
	inputFile=open(fileName)
	
	command=( inputFile.readline().rstrip() )[len(COMMAND_TXT)-1:].lstrip()
	description=( inputFile.readline().rstrip() )[len(DESCRIPTION_TXT)-1:].lstrip()
	if len(command)==0:
		ColorPrint( 'The command must contain at least 1 character.' , 'red')
		return -1
	if len(description)<5:
		ColorPrint( 'The description must contain at least 5 characters.' , 'red')
		return -1
	
	inputFile.readline()
	tags=[]
	for line in inputFile:
		tag=line.rstrip().lstrip()
		if len(tag)>0:
			tags.append( tag )
	inputFile.close()
	
	if not tags:
		ColorPrint( 'At least one tag must be specified.' , 'red')
		return -1
	
	commandId=DatabaseAddCommand(dbConnection, commandId, command, description)
	db=dbConnection.cursor()
	for tag in tags:
		DatabaseAddTag(dbConnection, tag, commandId)
	
	return commandId

def WriteCommandToFile( dbConnection, commandId, fileName): #Non controllo l'esistenza di commandId
	outputFile=open( fileName ,'w+')
	dbConnection=OpenDatabase()
	db=dbConnection.cursor()
	(command, description)=db.execute('SELECT command, description FROM Commands WHERE rowid=?',(commandId,)).fetchone() 
	outputFile.write(COMMAND_TXT+command+'\n')
	outputFile.write(DESCRIPTION_TXT+description+'\n')
	outputFile.write(TAGS_TXT)
	allTags=db.execute('SELECT tag FROM Tags WHERE commandId=?',(commandId,)).fetchall()
	for (tag,) in allTags:
		outputFile.write(tag+'\n')
	outputFile.close()
	
def Install(): #Da cancellare
	if os.path.exists(USER_DATA_FOLDER):
		ColorPrint( PROGRAM_NAME+' is already installed.', 'red')
		return
	
	os.makedirs(USER_DATA_FOLDER)
	print( 'The user folder has been created.' )
	
	dbConnection=OpenDatabase()
	db=dbConnection.cursor()
	db.execute('''
		CREATE TABLE IF NOT EXISTS Commands(
			rowid INTEGER PRIMARY KEY AUTOINCREMENT,
			command TEXT UNIQUE NOT NULL, 
			description TEXT
		)
	''')
	db.execute('''
		CREATE TABLE IF NOT EXISTS Tags(
			tag TEXT NOT NULL, 
			commandId INTEGER, 
			FOREIGN KEY(commandId)
				REFERENCES Commands(rowid)
				ON DELETE CASCADE
				ON UPDATE CASCADE
		)
	''')
	dbConnection.commit()
	dbConnection.close()
	print( 'Database has been successfully initialized.' )
	
	ColorPrint( 'Installation is complete.', 'green')

def Uninstall(): #Da cancellare
	if (not os.path.exists(USER_DATA_FOLDER)):
		ColorPrint( PROGRAM_NAME+' is not installed.', 'red' )
		return
	shutil.rmtree(USER_DATA_FOLDER)
	ColorPrint( PROGRAM_NAME+' has been uninstalled successfully.', 'green')
	
def QuietInstall():
	if os.path.exists(USER_DATA_FOLDER):
		return
	
	os.makedirs(USER_DATA_FOLDER)
	
	dbConnection=OpenDatabase()
	db=dbConnection.cursor()
	db.execute('''
		CREATE TABLE IF NOT EXISTS Commands(
			rowid INTEGER PRIMARY KEY AUTOINCREMENT,
			command TEXT UNIQUE NOT NULL, 
			description TEXT
		)
	''')
	db.execute('''
		CREATE TABLE IF NOT EXISTS Tags(
			tag TEXT NOT NULL, 
			commandId INTEGER, 
			FOREIGN KEY(commandId)
				REFERENCES Commands(rowid)
				ON DELETE CASCADE
				ON UPDATE CASCADE
		)
	''')
	dbConnection.commit()
	dbConnection.close()
	
#	Number of commands
#
#	command1
#	descrition1
#	number of tags
#	tag1
#	...
#	tagn
#
#	command2
#	...
def Import( fileName ): #Non controlla se sono già presenti i comandi
	inputFile=open( fileName )
	commandsNumber=int( inputFile.readline() )
	print( 'There are '+str(commandsNumber)+' commands to be imported:' )
	inputFile.readline()
	
	dbConnection=OpenDatabase()
	
	for i in range(commandsNumber):
		command=inputFile.readline().rstrip().lstrip()
		print( command )
		description=inputFile.readline().rstrip().lstrip()
		if not command:
			ColorPrint( "The "+str(i)+"-th command doesn't contain any characters, then the command is skipped." ,'red' )
			continue
		if len(description)<5:
			ColorPrint( "The description of the "+str(i)+"-th command is shorter than 5 characters, then the command is skipped." ,'red' )
			continue
		commandId=DatabaseAddCommand(dbConnection, -1, command, description)
		
		n=int(inputFile.readline())
		for j in range(n):
			tag=inputFile.readline().rstrip().lstrip()
			if not tag:
				ColorPrint( "The "+str(j)+"-th tag of the "+str(i)+"-th command doesn't contain any characters, then the tag is skipped." , 'red')
				continue
			DatabaseAddTag(dbConnection, tag, commandId)
		inputFile.readline()
	
	dbConnection.commit()
	dbConnection.close()
	inputFile.close();
	ColorPrint('The file '+fileName+' has been successfully imported.', 'green')

def Export( fileName ): 
	outputFile=open(fileName,'w+')
	dbConnection=OpenDatabase()
	db=dbConnection.cursor()
	allCommands=db.execute('SELECT rowid,command,description FROM Commands').fetchall()
	outputFile.write(str(len(allCommands))+'\n\n')
	for (commandId, command, description) in allCommands:
		outputFile.write(command+'\n')
		outputFile.write(description+'\n')
		allTags=db.execute('SELECT tag FROM Tags WHERE commandId=?',(commandId,)).fetchall()
		outputFile.write(str(len(allTags))+'\n')
		for (tag,) in allTags:
			outputFile.write(tag+'\n')
		outputFile.write('\n')
		print('Command '+str(commandId)+' has been written to the file.')
	ColorPrint('The whole database has been exported into '+fileName+'.', 'green')

def Add():
	tmpFile=open(TMPFILE_PATH,'w+')
	tmpFile.write(COMMAND_TXT+'\n'+DESCRIPTION_TXT+'\n'+TAGS_TXT)
	tmpFile.close()
	
	subprocess.check_call(['nano', '-t', '+1,'+str(len(COMMAND_TXT)+1), TMPFILE_PATH])
	
	dbConnection=OpenDatabase()
	commandId=AddCommandFromFile(dbConnection, -1, TMPFILE_PATH)
	if commandId!=-1:
		print( 'The following command has been added: ' )
		PrintCommand(dbConnection, commandId, 1)
	dbConnection.commit()
	dbConnection.close()
	os.remove(TMPFILE_PATH)

def Remove(commandId):
	dbConnection=OpenDatabase()
	if not DatabaseCommandExists(dbConnection, commandId):
		ColorPrint( "The command "+str(commandId)+" doesn't exist." , 'red')
		return 1
	DatabaseRemoveCommand(dbConnection, commandId)
	dbConnection.commit()
	dbConnection.close()
	ColorPrint( "The command "+str(commandId)+" has been successfully removed." , 'green')

def Modify(commandId):
	dbConnection=OpenDatabase()
	if not DatabaseCommandExists(dbConnection, commandId):
		ColorPrint( "The command "+str(commandId)+" doesn't exist." , 'red')
		return 1
	
	WriteCommandToFile(dbConnection, commandId, TMPFILE_PATH)
	DatabaseRemoveCommand(dbConnection, commandId)
	
	subprocess.check_call(['nano', '-t', '+1,'+str(len(COMMAND_TXT)+1), TMPFILE_PATH])
	commandId=AddCommandFromFile(dbConnection, commandId, TMPFILE_PATH)
	
	if commandId!=-1:
		print( 'The command has been modified successfully: ' )
		PrintCommand(dbConnection, commandId, 1)
	
	dbConnection.commit()
	dbConnection.close()
	os.remove(TMPFILE_PATH)

def Show():
	dbConnection=OpenDatabase()
	db=dbConnection.cursor()
	allCommands=db.execute('SELECT rowid FROM Commands').fetchall()
	
	for (commandId,) in allCommands:
		PrintCommand(dbConnection,commandId,1)
		
	if not allCommands:
		ColorPrint( "There aren't commands saved. To add a command use "+PROGRAM_NAME+" --add", 'red' )
	
	dbConnection.close()

def Search( commandTag ):
	dbConnection=OpenDatabase()
	db=dbConnection.cursor()
	db.execute("SELECT commandId FROM Tags WHERE tag LIKE ?", (commandTag+'%',) )
	commandIdList=set( db.fetchall() )
	
	for (commandId,) in commandIdList:
		PrintCommand(dbConnection, commandId, 0)
	
	if not commandIdList:
		ColorPrint( "No command matches the tag searched." , 'red' )
	
	dbConnection.close()

#Magari aggiungere un database reset? Bah
#Controllare la sicurezza del tutto e testare grandemente todos!
#Mettere a posto gli a capo generali!

if __name__=='__main__':
	QuietInstall()
	
	parser = argparse.ArgumentParser(description='Search all commands with the tag passed as an argument.')
	group = parser.add_mutually_exclusive_group(required=True)
	
	#~ group.add_argument('--install', action='store_true', default=False,
		#~ help='install '+PROGRAM_NAME)
	group.add_argument('--debugClean', action='store_true', default=False,
		help='uninstall '+PROGRAM_NAME)
	
	group.add_argument('--import', dest='fileImport', metavar='fileName', action='store', nargs=1, default='',
		help='import from a file')
	group.add_argument('--export', dest='fileExport', metavar='fileName', action='store', nargs=1, default='',
		help='export to a file')
		
	group.add_argument('--add','-a', action='store_true', default=False,
		help='add a new command')
	group.add_argument('--remove','-r','--delete','-d', metavar='commandId', nargs=1, type=int, action='store', default=-1,
		help='remove a command, passed its id')
	group.add_argument('--modify','-m','--change','-c', metavar='commandId', nargs=1, type=int, action='store', default=-1,
		help='modify a command, passed its id')
		
	group.add_argument('--show', action='store_true', default=False,
		help='show all commands saved, with descriptions and tags')
	
	group.add_argument('tag', metavar='TAG', action='store', nargs='?', default='', 
		help='tag to be searched')
		
	group.add_argument('--version', action='version', version=PROGRAM_NAME+' '+PROGRAM_VERSION)
	
	args=parser.parse_args()
	
	#~ if args.install:
		#~ Install()
	#~ elif args.uninstall:
		#~ Uninstall()
	if args.fileImport:
		Import(args.fileImport[0])
	elif args.fileExport:
		Export(args.fileExport[0])
	elif args.add:
		Add()
	elif args.remove != -1:
		Remove(args.remove[0])
	elif args.modify != -1:
		Modify(args.modify[0])
	elif args.show:
		Show()
	elif args.tag:
		Search(args.tag)
	elif args.debugClean:
		Uninstall()
