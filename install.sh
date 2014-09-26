#!/bin/bash

cp bashelp.py /usr/local/bin/bashelp

pandoc -s -w man docs/manpage.md -o docs/bashelp.1
mkdir -p /usr/local/man/man1
mv docs/bashelp.1 /usr/local/man/man1/bashelp.1.gz

echo 'bashelp has been succesfully installed'
