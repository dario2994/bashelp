#!/bin/bash

ronn -r docs/manpage.md
sudo cp bashelp.py /usr/local/bin/bashelp
sudo mkdir -p /usr/local/man/man1
sudo cp docs/bashelp.1 /usr/local/man/man1/bashelp.1.gz

echo 'bashelp has been succesfully installed'
