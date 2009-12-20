
JSMIN=python ../../hibird/jsmin.py

CSSMIN=python ../../hibird/cssmin.py

all: scriptaculous-hibird.min.js jquery-hibird.min.js
	
scriptaculous-hibird.min.js: browser.js ../prototype/prototype.js ../scriptaculous/builder.js ../scriptaculous/effects.js ../scriptaculous/dragdrop.js ../scriptaculous/controls.js scriptaculous.hibird.js scriptaculous.notifier.js ../expandable-textarea/textarea.js scriptaculous.scripty.js
	cat $^ | ${JSMIN} > $@

jquery-hibird.min.js: browser.js ../jquery/jquery.js jquery.hibird.js jquery.notifier.js jquery.textarearesizer.js jquery.scripty.js
	cat $^ | ${JSMIN} > $@

