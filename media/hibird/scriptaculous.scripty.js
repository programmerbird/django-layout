(function () {

var effect = function (options, self,o,next){
	var effectName = this;
	o.each(function (i) {
		if(i.visible() == options.whenVisible){
			i[effectName]({
				duration: 0.3,
				afterFinish: function () {
					do_next(self,o,next);
				}
			})
		}else{
			do_next(self,o,next);
		}
	});
};

var toggle = function (showAction, self,o,next){
	var hideAction = this;
	if(o && o[0].visible()){
		var action = hideAction;
	}else{
		var action = showAction;
	}
	o.invoke(action, {
		duration: 0.3,
		afterFinish: function () {
			do_next(self,o,next);
		}
	});
};

var toggleSelected = function (self,o,next){
	if(o && o[0].hasClassName('selected')){
		var action = 'removeClassName';
	}else{
		var action = 'addClassName';
	}
	o.invoke(action, 'selected');
	do_next(self, o, next);
};

var do_next = function (self,o,next){
	if(next){
		var action = next.substring(0, (next + '|').indexOf('|'));
		next = next.substring(action.length+1);
		if(action.include(':')){
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
	var label = $(t.select('label[for='+input.name+']').first());
	Object.extend(label.style, {
		zIndex: 10,
		position: 'absolute',
		fontSize: input.getStyle('fontSize'),
		paddingTop: input.getStyle('paddingTop'),
		paddingLeft: input.getStyle('paddingLeft'),
		marginTop: input.getStyle('marginTop'),
		marginLeft: input.getStyle('marginLeft')
	});
	Object.extend(input.style, {
		zIndex: 100
	});
	label.onclick = function (input) {
		input.focus();
	}.bind(label,input);
	input.makePositioned();
	if(input.value.empty()){
		input.addClassName('empty');
	}
};

var manage_inline_form = function (dom){
	dom.select('.inline input').each(function (i){
	try{
		if(i.type != 'text' && i.type != 'password') return;
		init_hint(i);
		i.observe('focus', function (e) {
			var m = e.element();
			$(m).addClassName('focus');
		});
		i.observe('keypress', function (e){
			var m = e.element();
			$(m).removeClassName('empty');
		});
		i.observe('blur', function (e){
			var m = e.element();
			$(m).removeClassName('focus');
			if(m.value.empty()){
				$(m).addClassName('empty');
			}
		});
	}catch(e){ }
	});
};

var manage_textarea = function (dom){
	dom.select('textarea').each(function(tb){
		new TextAreaResizer(tb);
	});
};	

var scripty = {

	actions: {
		show: function (self,o,next){ o.invoke('show'); do_next(self,o,next); },
		hide: function (self,o,next){ o.invoke('hide'); do_next(self,o,next); },
		clear: function (self,o,next){ o.invoke('update'); do_next(self,o,next); },
		reset: function (self,o,next){ 
			o.invoke('reset'); do_next(self,o,next);
			o.each(function (f){
				f.select('input').each(function (m) {
					$(m).removeClassName('focus');
					if(!$(m).value) $(m).addClassName('empty');
				});
			});
		},
		makeajax: function (self, o, next) {
			o.each(function (f){
				f.select('form').each(function (form){
					if (form.hasClassName('ajax')) return;
					$(form).observe('submit', function (self, o, next, ev){
						scripty.actions.submit.bind(self)(self, o, next);
						ev.stop();
						return false;
					}.bind(self, self, o, next));
				});
			});
		},
		
		focus: function (self, o, next) {  },
		highlight: function (self,o,next) { o.invoke('highlight'); do_next(self,o,next); },
		save_ok: function (self,o,next) { hibird.notify('Saved successfully'); do_next(self,o,next); },
		
		appear: effect.bind('appear', {whenVisible: false}),
		fade: effect.bind('fade', {whenVisible: true}),
		blindUp: effect.bind('blindUp', {whenVisible: true}),
		blindDown: effect.bind('blindDown', {whenVisible: false}),
		blind: toggle.bind('blindUp', 'blindDown'),
		toggleSelected: toggleSelected,
		
		reload: function (self,o,next){
			var x = o; 
			x.each(function (item){
				
				if(item.className.include('PARTIAL')){
					if(item.title){
						var target = item.title;
						$(target).store('target', target);
						this.title = '';
					}else{
						var target = $(item).retrieve('target');
					}
					if(target){
						var chunks = target.split('#', 2);
						var url = chunks[0];
						var partName = chunks[1];
					}else{
						var url = window.location.href.toString().split('#',1)[0];
						var partName = item.className.split('PARTIAL ',2)[1].split(' ',2)[0];
					}
					if(url.include('?')){
						url += '&PARTIAL=';
					}else{
						url += '?PARTIAL=';
					}
					new Ajax.Request(url+partName, {
						method: 'get',
						evalScripts: false,
						evalJS: false,
						onSuccess: function (self, o, next, trans){
							this.update(trans.responseText);
							scripty.hook(this);
							do_next(self,o,next);
						}.bind(item, self, o, next)
					});
				}
			});
			
		},	
		submit: function (self,o,next){
		
			o.each(function(item){
				var t = item;
				var obj = $(t).select('form').first();
				if(obj){
					t = obj;
				}else{
					while(t && t.tagName != 'FORM') {t = t.parentNode }
				}
				if(t){
					if (!t.action.include('__hibird_ajax')){
						if(t.action.include('?')){
							t.action = t.action + '&__hibird_ajax=1';
						}else{
							t.action = t.action + '?__hibird_ajax=1';
						}
					}
					var methodName = t.method || "post";
					var params = {};
					if(item.name && item.value){
						params[item.name] = item.value;
					}
					$(t).request({
						parameters: params,
						method: methodName.toLowerCase(),
						onSuccess: function (trans){
							do_next(self,o,next);
						},
						onFailure: function(trans){
							if(trans.responseText.length < 300){
								hibird.notify(trans.responseText);
							}else{
								hibird.notify("Sorry, something went wrong", {kind:'error'});
							}
						},
						onComplete: function (trans){
							$(this).enable();
							$(this).select('button').each(function (b){ b.disabled=false; });
						}.bind(t)
					});
					$(t).disable();
					$(t).select('button').each(function (b){ b.disabled=true; });
				}
			});
		},
		propagate: function(o,next){}
	},
	
	select: function (self, filter) {
	
		if(filter=='') return $A([self]); 
		if(filter.include('+')) {
			var result = [];
			$A(filter.split('+')).each(function (e){
				result = result.concat(scripty.select(self, e));
			});
			return $A(result);
		}
		
		filter = filter.replace(/\!/g, '#');
		filter = filter.replace(/\*/g, ':');
		filter = filter.replace(/\~/g, '.PARTIAL.');
		filter = filter.replace(/\%20/g, ' ');
		
		var only_visible = false;
		if(filter.endsWith(':visible')){
			only_visible = true;
			filter = filter.substring(0,filter.length-8);
		}
		var only_hidden = false;
		var result = null;
		if(filter.endsWith(':hidden')){
			only_hidden = true;
			filter = filter.substring(0,filter.length-7);
		}
		var is_closest = false;
		if(filter.startsWith('^')){
			is_closest = true;
			filter = filter.substring(1);
		}
		if(is_closest){
			var cur = self;
			result = $A([]);
			while(cur && !result.any()){
				cur = cur.parentNode;
				result = $(cur).select(closest);
			}
			return result;
		}else{
			result = $$(filter);
		}
		
		if(only_visible){
			result = result.collect(function (item) { if($(item).visible()) return item });
		}
		if(only_hidden){
			result = result.findAll(function (a) { return !a.visible() });
		}
		
		return result;
	},

	operate: function (self, url, ev){
		if(!url.include('#do=')) return;
		var expr = url.split('#do=',2)[1];
		$A(expr.split(',')).each(function (stat){
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
		var partials = dom.select('.PARTIAL');
		for(var i=0,len=partials.length; i<len; i++){
			var t = partials[i];
			if(t.title){
				var target = t.title;
				$(t).store('target', target);
				t.title = '';
			}
		}	
		
		var objs = dom.select('.ajax');
		for(var i=0, len=objs.length; i<len; i++){
			var obj = objs[i];
			var actions = obj.className.split(' ');
			$A(actions).each(function (action){
				if(action.startsWith('on-')){
					var chunks = action.split('-',3);
					var event = chunks[1];
					var param = chunks[2];
					var url = obj[param];

					if(!obj.retrieve('ajax-'+event)){
						obj.store('ajax-'+event, url);
						obj[param] = url.split('#do=',1)[0];
					}else{
						url = obj.retrieve('ajax-'+event);
					}
					obj.observe(event, function(obj,ev){
						var expr = obj.retrieve('ajax-'+this);
						scripty.operate(obj, expr, ev);
						if(!expr.include('propagate')) ev.stop();
					}.bind(event,obj));
				}
			});
		};
		
		manage_inline_form(dom);
		manage_textarea(dom);
		
	}
};

hibird.scripty = function (action) {
	if(!action.include('#do=')){
		action = '#do='+action;
	}
	scripty.operate(document, action, null);
};

hibird.ready(function () {
	var url = window.location.href.toString();
	if(url.include('#do=')){
		window.location.href = url.split('#do=',1)[0];
	}
	scripty.hook($$('body')[0]);
});

})();
