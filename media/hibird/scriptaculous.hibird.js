
var hibird = {
	version: '1.2'
};


var log = { 
	clear: function () {},
	debug: function () {},
	warn: function () {},
	error: function () {},
	info: function () {},
	profile: function () {}
};

(function (){
	hibird.ready = function (f) {
		document.observe("dom:loaded", f);
	};
	hibird.ready(function (){
		$$('html').first().addClassName('has-js');
		$$('.js').invoke('removeClassName', 'js');
	});
	
})();

