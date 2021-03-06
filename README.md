bashelp
=======

A tool for bookmarking and tagging your favourite (and impossible to remember) shell commands

Dependencies and Requirements
==============================
To install and run **bashelp** you need to have installed:
* nano 
* python3 (>=3.2)
* sqlite3 (>=3.6.19)

The docs for bashelp are written in Markdown and translated in the unix man language using pandoc. 
Pandoc is NOT a dependency as the manpage is already built and does not have to be built during the installation.

It has been tested both on **bash** and **zsh** on the following linux distros: *Ubuntu*, *Debian*, *Fedora*, *Arch*, *Gentoo*.

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
you can interactively add a command to your shelf,
then get it with
```bash
bashelp CommandTag
```
and in the end you remove the command with
```bash
bashelp --remove CommandId
```

For further information you may use 
```bash
bashelp -h
```
or read the documentation in the manual
```bash
man bashelp
```
