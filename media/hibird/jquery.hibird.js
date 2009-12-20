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

(function ($){

	Function.prototype.bind = function () {
		var _$A = function (a){ return Array.prototype.slice.call(a); }
		if (arguments.length < 2 && (typeof arguments[0] == "undefined")) return this;
		var __method = this, args = _$A(arguments), object = args.shift();
		return function (){
			return __method.apply(object, args.concat(_$A(arguments)));
		}
	};
	
	hibird.ready = $(document).ready;
	hibird.ready(function () {
		$('html').addClass('has-js');
		$('.js').removeClass('js');
	});
})(jQuery);

