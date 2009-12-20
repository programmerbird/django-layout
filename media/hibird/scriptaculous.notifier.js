(function (){

	var notifier = {
		load: function () {
			$('info').observe('click', notifier.hide);
			var url = window.location.href.toString();
			if( url.indexOf('&info=')>=0 || url.indexOf('?info=')>=0 ){
				$('info').hide();
				hibird.notify( $('info').select('div').first().innerHTML );
			}
		},
			
		show: function ( msg ){
			$('info')
				.hide().update("<div>"+ msg +"</div>")
				.blindDown({duration: 0.3});
		},
	
		hide: function ( delay ) {
			var delay = (delay==null) ? 0 : delay;
			setTimeout("$('info').blindUp({duration: 0.3});", delay);
		},
	
		notify: function (msg, options) {
			options = Object.extend({
				delay : 10000,
				kind: null
			}, options || {});
			$('info').className = options.kind || '';
			notifier.show(msg);
			notifier.hide(options.delay);
		}
	};
	
	hibird.notify = notifier.notify;
	hibird.ready(function (){
		notifier.load();
	});
	
})();
