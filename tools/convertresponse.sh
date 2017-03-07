cat "$1" | sed -f convertobj.sed > /tmp/sed
grep -e 'function' -e 'const' /tmp/sed >/dev/null
if [ $? -ne 0 ]; then
    ./addimports.sh /tmp/sed
    cp /tmp/sed `echo "$1" | sed 's:../php:.:g;s:.php:.py:g;s:Instagram-API:InstagramAPI:g'`
fi
