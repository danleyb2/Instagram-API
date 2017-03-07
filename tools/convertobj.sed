#!/bin/sed

s/^ *<?php *$/from InstagramAPI.src.http.Response.Response import Response\n\n/g
/^ *namespace *.*$/d;
/^ *$/d;
s/^ *class *\([A-Za-z0-9_]*\).*/class \1(Response):/g;
/^class.*/ {
  N
  s/ *{.*/    def __init__(self):\n        self._types = {}\n/g
}
/^ *\/\*\** */d
/^ *\*\/ */d
s/^ *\* *@var \([]\[A-Za-z0-9_]*\).*/* @var \1/g;
s/^ *\* *@var \([A-Za-z0-9_]*\)\[\].*/* @var [\1]/g;
/^ *\* *@var mixed.*/d
s/\([^A-Za-z0-9_]*\)null\([^A-Za-z0-9_]*\)/\1None\2/g;
s/\([^A-Za-z0-9_]*\)true\([^A-Za-z0-9_]*\)/\1True\2/g;
s/\([^A-Za-z0-9_]*\)false\([^A-Za-z0-9_]*\)/\1False\2/g;
s/\([^A-Za-z0-9_]*\)string\([^A-Za-z0-9_]*\)/\1str\2/g;
s:\(//.*\):# \1:g
s/^ *public *\$in\([ =;][ =;]*\)/public $__dict__["in"]\1/g
s/^ *public *\$\(.*=.*\);\(.*\)$/        self.\1\2/g
s/^ *public *\$\(.*\);\(.*\)$/        self.\1 = None\2/g
/^ *\* *@var \([]\[A-Za-z0-9_]*\).*/ {
:newline
  N
  s/\n *\*\/ *//g
  t newline
  s/^ *\* *@var \([]\[A-Za-z0-9_]*\).*\n\( *public *\$\([A-Za-z0-9_]*\).*\)/        self._types["\3"] = \1\n\2/g
  s:\(//.*\):# \1:g
  s/\([^A-Za-z0-9_]*\)null\([^A-Za-z0-9_]*\)/\1None\2/g;
  s/\([^A-Za-z0-9_]*\)true\([^A-Za-z0-9_]*\)/\1True\2/g;
  s/\([^A-Za-z0-9_]*\)false\([^A-Za-z0-9_]*\)/\1False\2/g;
  s/\([^A-Za-z0-9_]*\)string\([^A-Za-z0-9_]*\)/\1str\2/g;
  s/ *public *\$in\([ =;][ =;]*\)/public $__dict__["in"]\1/g
  s/ *public *\$\(.*=.*\);\(.*\)$/        self.\1\2/g
  s/ *public *\$\(.*\);\(.*\)$/        self.\1 = None\2/g
}
/^ *}.*/d