
(function ($){

	var notifier = {
		load: function () {
			$('#info').click(notifier.hide);
			var url = window.location.href.toString();
			if( url.indexOf('&info=')>=0 || url.indexOf('?info=')>=0 ){
				$('#info').hide();
				notifier.notify( $('#info').html() );
			}
		},
		show: function (msg){
			$('#info')
				.hide().html("<div>" + msg + "</div>")
				.fadeIn("fast");
		},
		hide: function (delay){
			delay = (delay==null) ? 0 : delay;
			setTimeout("$('#info').fadeOut('fast')", delay);
		},
		notify: function (msg, options){
			options = $.extend({
				delay: 10000,
				kind: null
			}, options || {});
			$('#info').attr('class', options.kind || '');
			notifier.show(msg);
			notifier.hide(options.delay);
		}
	};
	
	hibird.notify = notifier.notify;
	hibird.ready(function () {
		notifier.load();
	});
	
})(jQuery);

