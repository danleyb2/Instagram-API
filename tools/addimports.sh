#!/bin/bash

cd `dirname "$0"`/..

cat "$1" |\
    grep "_types\[" | \
    sed 's:.*=[\[ ]*\([A-Za-z0-9_]*\).*:\1:g' > /tmp/sed_
cat /tmp/sed_ | while read line;
do
    PYMOD="`find ./InstagramAPI | grep "/$line.py\$" | sed 's:^\./::g;s:/:.:g;s:\.py$::g' | head -n1`"
    grep "$PYMOD" "$1" >/dev/null || echo "$PYMOD"
done > /tmp/sed1
cat /tmp/sed1 | sort | uniq | sed 's:\(.*\.\([^.]*\)\):from \1 import \2:g' | sed '/^ *$/d' > /tmp/sed_
cat /tmp/sed_
cat /tmp/sed_ "$1" > /tmp/sed1
cat /tmp/sed1 > "$1"
