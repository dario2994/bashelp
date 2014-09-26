% BASHELP(1) User Manual
% 
% September 26, 2014

#NAME

**bashelp** -- bookmark, tag and search shell commands

# SYNOPSIS

**bashelp** *tag*\
**bashelp** -a|--add\
**bashelp**  -r|--remove, -m|--modify *tagId*\
**bashelp** --import, --export *fileName*\
**bashelp** -s|--show\
**bashelp** -v|--version, -h|--help

# DESCRIPTION

**bashelp** is a shell tool for bookmarking, tagging and searching shell 
commands you often use and often forget.

All the commands saved are stored in a sqlite database, and each command has an 
id, a short description and as many tags as needed to search for it afterward. 
When adding a command a unique id will be assigned to it, and showed always near
the command. When refering to the command, for example modifying and removing
it, his id should be used.

It is possible, through --import and --export options, to save in a simple
txt file all those commands that were previously added to **bashelp** database and
to load them again on a different **bashelp** installation.

**bashelp** should work on any modern shell (bash and zsh).

# OPTIONS

Just one option per time is accepted. This reflects the fact that any option 
directly relates to an action of the **bashelp**.

When passing *tag* (**bashelp** *tag*) all commands which have the corresponding, 
or a similar one, tag will be showed.
If *tag* is passed, no other option should be passed.

-a|--add
:   Add a command. It will open a nano instance on a template file to be filled 
    with details about the command to be added. When the file is filled with 
    information, just close nano using ctrl+x and the command will be added.

-r|--remove *tagId*
:   Remove the command with id=tagId. 

-m|--modify *tagId*
:   Modify the command with id tagId. It will open a nano instance on a file
    already filled with the details of the command, change what you want and
    then close nano using ctrl+x.

--import *fileName*
:   Import commands, saved in a specific format, from the file identified by
    fileName.
    
    The standard format used is:
        
        number of commands
        
        previous commands...
        last tag of command(N-1)

        commandN
        description of commandN
        number of tags of commandN
        1st tag of commandN
        2nd tag of commandN
        other tags...
        last tag of commandN

        command(N+1)
        following commands...
		
--export *fileName*
:   Export all commands saved in the database in the file identified by 
    fileName. It will use the same format as --import.
    
-s|--show
:   Shows all commands saved in the database, with their ids and descriptions
    and tags.
  
-v|--version
:   Prints the version of **bashelp** installed.
    
-h|--help
:   Prints the synopsis and a short explanation of various options.

# FILES

The database used to store commands is a sqlite3 database (using foreign keys, 
so sqlite version >= 3.6.19) saved in *~/.bashelp/CommandsDatabase.md*.

**bashelp** internally, when adding or changing a command, creates, and 
subsequently deletes, the file */tmp/bashelp_TempCommandFile.txt*.

# AUTHOR
**bashelp** was written by Federico Glaudo `<dario2994@gmail.com>`.

# THANKS
Special thanks go to: Giada Franz, William Di Luigi.

# BUGS

No bugs are known.

# REPORTING BUGS

For any issues please visit https://github.com/dario2994/bashelp/issues.

# COPYRIGHT

Copyright  ©  2012  Free Software Foundation, Inc.  License GPLv3+: GNU
GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software: you are free  to  change  and  redistribute  it.
There is NO WARRANTY, to the extent permitted by law.


# SEE ALSO

sqlite3(1)
