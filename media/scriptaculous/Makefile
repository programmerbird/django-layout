
JSMIN=python ../../hibird/jsmin.py

CSSMIN=sed -e :a -e '$!N; s/\n/ /; ta' | sed 's/[ฟห]//g' | sed "s@\/\*@ฟ@g" | sed "s@\*\/@ห@g" | sed "s/ฟ[^ห]*ห//g" | sed 's/[ \t;]*\([\{\}]\)[ \t;]*/\1/g' | sed 's/;\s*/;/g' | sed 's/\([:;]\)\s*/\1/g' | sed 's/[;\s]+\}/}/g'

scriptaculous.min.js: ../prototype/prototype.js builder.js effects.js dragdrop.js controls.js
	cat $^ | ${JSMIN} > $@
