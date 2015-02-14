bashelp
=======

A tool for bookmarking and tagging your favourite (and impossible to remember) shell commands

Dependencies and Requirements
==============================
To install and run **bashelp** you need to have installed:
* nano 
* python3 (>=3.2)
* sqlite3 (>=3.6.19)

To build the docs for bashelp (not needed to install or run, as docs are 
already builded) you need:
* pandoc

It has been tested both on **bash** and **zsh** on the following linux distros: *Ubuntu*, *Debian*, *Fedora*, *Arch*.

Installation
============
1. Clone the repository or just download the whole content in a folder on your pc.
2. Execute in a shell 'sudo ./install.sh'.

Now you have installed bashelp.
To remove bashelp just execute 'uninstall.sh'.

Usage
=====
With
```bash
bashelp -a
```
you can interactively add a command to you shelf,
then get it with
```bash
bashelp CommandTag
```
and in the end you remove the command with
```bash
bashelp -remove CommandId
```

For further information you may use 
```bash
bashelp -h
```
or read the documentation in the manual
```bash
man bashelp
```
