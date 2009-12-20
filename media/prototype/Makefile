
JSMIN=python ../../hibird/jsmin.py

CSSMIN=sed -e :a -e '$!N; s/\n/ /; ta' | sed 's/[ฟห]//g' | sed "s@\/\*@ฟ@g" | sed "s@\*\/@ห@g" | sed "s/ฟ[^ห]*ห//g" | sed 's/[ \t;]*\([\{\}]\)[ \t;]*/\1/g' | sed 's/;\s*/;/g' | sed 's/\([:;]\)\s*/\1/g' | sed 's/[;\s]+\}/}/g'

prototype.min.js: prototype.js
	cat $^ | ${JSMIN} > $@
