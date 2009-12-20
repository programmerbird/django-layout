(function ($) {

var effect = function (self,o,next){
	$(o)[this]('fast', function () {
		do_next(self, o, next);
	});
};


var toggle = function (showAction, self,o,next){
	var hideAction = this;
	if($(o).is(':visible')){
		var action = hideAction;
	}else{
		var action = showAction;
	}
	$(o)[action]('fast', function () {
		do_next(self,o,next);
	});
};


var toggleSelected = function (self,o,next){
	if(o && $(o).is('.selected')){
		var action = 'removeClass';
	}else{
		var action = 'addClass';
	}
	$(o)[action]('selected');
	do_next(self, o, next);
};

var do_next = function (self,o,next){
	if(next){
		var action = next.substring(0, (next + '|').indexOf('|'));
		next = next.substring(action.length+1);
		if(action.indexOf(':') >= 0){
			var filter = action.substring(0, action.indexOf(':'));
			var action = action.substring(filter.length+1);
			
			o = scripty.select(self, filter);
		}
		scripty.actions[action](self,o,next);
	}
};


	
var init_hint = function (input){
	var t = input;
	while(t && t.tagName != 'FORM') {t = t.parentNode }
	var labels = $(t).find('label[for='+input.name+']');
	var $input = $(input);
	labels.css({
		zIndex: 10,
		position: 'absolute',
		fontSize: $input.css('fontSize'),
		paddingTop: $input.css('paddingTop'),
		paddingLeft: $input.css('paddingLeft'),
		marginTop: $input.css('marginTop'),
		marginLeft: $input.css('marginLeft')
	});
	$(input).css({
		zIndex: 100,
		position: 'relative'
	});
	labels.click(function (input) {
		this.focus();
	}.bind(input));
	if(!$(input).val()){
		$(input).addClass('empty');
	}
};

var manage_inline_form = function (dom){
	$.each($(dom).find('.inline input'), function (){
	try{
		var i = this;
		if(i.type != 'text' && i.type != 'password') return;
		init_hint(i);
		$(i).bind('focus', function(e){
			var m = this;
			$(m).addClass('focus');
		});
		$(i).bind('keypress', function(e){
			var m = this;
			$(m).removeClass('empty');
		});
		$(i).bind('blur', function (e){
			var m = this;
			$(m).removeClass('focus');
			if(!m.value){
				$(m).addClass('empty');
			}
		});
	}catch(e){ }
	});
};

var manage_textarea = function (dom){
	$(dom).find('textarea').TextAreaResizer();
};	

var scripty = {

	actions: {
		show: function (self,o,next){ $(o).show(); do_next(self,o,next); },
		hide: function (self,o,next){ $(o).hide(); do_next(self,o,next); },
		clear: function (self,o,next){ $(o).html(''); do_next(self,o,next); },
		reset: function (self,o,next){ 
			$(o)
			 .find(':input')
			 .not(':button, :submit, :reset, :hidden')
			 .val('')
			 .removeAttr('checked')
			 .removeAttr('selected');
			do_next(self,o,next);
			$.each($(o).find('input'), function (){
				var m = this;
				$(m).removeClass('focus');
				if(!$(m).value) $(m).addClass('empty');
			});
		},
		makeajax: function (self,o,next) {
			$.each($(o).find('form').not('.ajax'), function (){
				$(this).submit(function (self, o, next) {
				 	scripty.actions.submit.bind(self)(self, o, next)
				 	return false;
				}.bind(self, self, o, next));
			});
		},
		focus: function (self, o, next) { $(o).select(); do_next(self,o,next); },
		highlight: function (self,o,next) { do_next(self,o,next); },
		save_ok: function (self,o,next) { hibird.notify('Saved successfully'); do_next(self,o,next); },
		
		appear: effect.bind('fadeIn'),
		fade: effect.bind('fadeOut'),
		blindUp: effect.bind('slideUp'),
		blindDown: effect.bind('slideDown'),
		blind: toggle.bind('slideUp', 'slideDown'),
		toggleSelected: toggleSelected,
		
		reload: function (self,o,next){
			var x = o; 
			$.each($(x), function () {
				if(this.className.indexOf('PARTIAL')>=0){
					if(this.title){
						var target = this.title;
						$(this).data('target', target);
						this.title = '';
					}else{
						var target = $(this).data('target');
					}
					if(target){
						var chunks = target.split('#', 2);
						var url = chunks[0];
						var partName = chunks[1];
					}else{
						var url = window.location.href.toString().split('#',1)[0];
						var partName = this.className.split('PARTIAL ',2)[1].split(' ',2)[0];
					}
					if(url.indexOf('?')>=0){
						url += '&PARTIAL=';
					}else{
						url += '?PARTIAL=';
					}
					$.ajax({
						"url": url+partName,
						"type": "GET",
						success: function (self, o, next, html){
							$(this).html(html);
							scripty.hook(this);
							do_next(self, o, next);
						}.bind(this, self, o, next)
					});
				}
			});
		},	
		submit: function (self,o,next){
			$.each($(o), function(){
				var t = this;
				var objs = $(t).find('form');
				if(objs.length){
					t = objs[0];
				}else{
					while(t && t.tagName != 'FORM') {t = t.parentNode }
				}
				if(t){
					if($(t).find('input[type=file]').length > 0 && !this.name){
						t.action = t.action.replace('__hibird_ajax=1', '');
						t.submit();
						return;
					}
					if (t.action.indexOf('__hibird_ajax')==-1){
						if(t.action.indexOf('?')>=0){
							t.action += '&__hibird_ajax=1';
						}else{
							t.action += '?__hibird_ajax=1';
						}
					}
					var serializedData = $(t).serialize();
					if(this.name && this.value){
						var params = {};
						params[this.name] = this.value;
						serializedData += '&'+ $.param(params);
					}
					var methodName = t.method || "POST";
					$.ajax({
						"url": t.action,
						"type": methodName.toUpperCase(),
						data: serializedData,
						success: do_next.bind(self, self, o, next),
						error: function (transport){
							var html = transport.responseText;
							if(html.length < 300){
								hibird.notify(html);
							}else{
								hibird.notify("Sorry, something went wrong", {kind:'error'});
							}
						}, 
						complete: function(transport){
							var t = t;
							$(t).find(':input')
								.removeAttr('disabled');
						}.bind(t)
					});
					$(t).find(':input')
						.attr('disabled', true);					
				}
			});
		},
		propagate: function(o,next){}
	},
	
	select: function (self, filter) {
		if(filter=='') return [self]; 
		if(filter.indexOf('+')>=0) {
			var result = [];
			$(filter.split('+'), function (){
				result = result.concat(scripty.select(self, e));
			});
			return result;
		}
		
		filter = filter.replace(/\!/g, '#');
		filter = filter.replace(/\*/g, ':');
		filter = filter.replace(/\~/g, '.PARTIAL.');
		filter = filter.replace(/\%20/g, ' ');
		var is_closest = false;
		if(filter.indexOf('^')==0){
			is_closest = true;
			filter = filter.substring(1);
		}
		if(is_closest){
			var cur = self;
			var result = [];
			while(cur && result.length==0){
				cur = cur.parentNode;
				result = $(cur).find(closest);
			}
			return result;
		}else{
			return $(filter);
		}
	},

	operate: function (self, url, ev){
		if(url.indexOf('#do=')==-1) return;
		var expr = url.split('#do=',2)[1];
		$.each(expr.split(','), function (){
			var stat = this;
			var filter = stat.substring(0, stat.indexOf(':'));
			var action = stat.substring(filter.length+1);
			var objs = scripty.select(self, filter);
			try{
			do_next(self,objs,action);
			}catch(e){}
		});
		
		return false;
	},
	
	hook: function (dom){
		$.each($(dom).find('.PARTIAL'), function (){
			var t = this;
			if(this.title){
				var target = this.title;
				$(this).data('target', target);
				this.title = '';
			}
		});
		
		var objs = $(dom).find('.ajax');
		$.each(objs, function (){
			var obj = this;
			var actions = obj.className.split(' ');
			$.each(actions, function (){
				var action = this;
				if(action.indexOf('on-')==0){
					var chunks = action.split('-',3);
					var event = chunks[1];
					var param = chunks[2];
					var url = obj[param];

					if(!$(obj).data('ajax-'+event)){
						$(obj).data('ajax-'+event, url);
						obj[param] = url.split('#do=',1)[0];
					}else{
						url = $(obj).data('ajax-'+event);
					}
					$(obj).bind(event, function(eventName, ev){
						var expr = $(this).data('ajax-'+eventName);
						scripty.operate(obj, expr, ev);
						if(!expr.indexOf('propagate')>=0) {
							ev.stopPropagation();
							ev.preventDefault();
						}
					}.bind(obj, event));
				}
			});
		});
		
		manage_inline_form(dom);
		manage_textarea(dom);
		
	}
};

hibird.scripty = function (action) {
	if(action.indexOf('#do=') > 0){
		action = '#do='+action;
	}
	scripty.operate(document, action, null);
};

hibird.ready(function () {
	var url = window.location.href.toString();
	if(url.indexOf('#do=') > 0){
		window.location.href = url.split('#do=',1)[0];
	}
	scripty.hook($('body'));
});

})(jQuery);
