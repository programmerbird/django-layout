// ==UserScript==
// @name Hibird Logger
// @namespace http://hibird.net/
// @description Load Hibird Logger
// @include http://localhost:8000/*
// ==/UserScript==

(function(){
	var scripts = [
		'/media/hibird/log.min.js',
	];
	for (i in scripts){
		var script = document.createElement('script');
		script.type = 'text/javascript';
		script.src = scripts[i];
		document.getElementsByTagName('head')[0].appendChild(script);
	}
	
})();

