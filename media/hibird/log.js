
var log = { 
	form: null,
	container: null,

	scroll: function (container, element) {
		container = $(container);
		element = $(element);
		var x = element.x ? element.x : element.offsetLeft,
		y = element.y ? element.y : element.offsetTop;
		container.scrollLeft=x-(document.all?0:container.offsetLeft );
		container.scrollTop=y-(document.all?0:container.offsetTop);
		return element;
	},
	
	load: function () {
		var div = document.createElement('div');
		div.id = 'logger';
		div.innerHTML = '<span id="btn_clear_log"><a href="#" onclick="javascript:log.clear()"><img src="/media/icons/delete.png" alt="Clear" title="Clear" align="absmiddle" /></a> | <a href="#" onclick="javascript:log.hide()">hide</a></span><ul id="container"></ul>';
		document.getElementsByTagName('body')[0].appendChild(div);
		log.form = div;
		log.container = document.getElementById('container');
	},
	
	write: function (msg, options) {
		var li = document.createElement('li');
		li.innerHTML = msg;
		Object.extend(li, options);
		log.container.appendChild(li);
		log.scroll(log.form, li);
		return li;
	},
	
	clear: function () {
		log.container.innerHTML = '';
	},
	
	hide: function () { log.form.hide(); },

	show: function () { log.form.show(); },
		
	popup: function (msg) {
		var div = document.createElement('div');
		Object.extend(div.style, {
			top: '5px', 
			left: '5px',
			position: 'fixed',
			width: '620px',
			height: '420px',
			padding: '10px'
		});
		
		var btnClose = document.createElement('a');
		Object.extend(btnClose, {
			href: '#',
			innerHTML: '[close]',
			onclick: function (div){
				div.parentNode.removeChild(div);
			}.bind(div, div)
		});
		div.appendChild(btnClose);
		
		var textarea = document.createElement('textarea');
		textarea.value = msg;
		Object.extend(textarea.style, {
			width: '600px',
			height: '400px'
		});
		div.appendChild(textarea);
		$$('body')[0].appendChild(div);
	},
	
	warn: function (msg) { log.write(msg, {className: 'warn', title: 'Warning'}); },
	info: function (msg) { log.write(msg, {className: 'info', title: 'information'}); },
	debug: function (msg) { log.write(msg, {className: 'debug', title: 'debug'}); },
	error: function (msg) {
		if ( msg.message ) {
			var li = log.write(msg.message + ' ', {
				className: 'error', title: 'Error', Exception: msg
			});
			var a = document.createElement('a');
			Object.extend(a, {
				href: '#',
				innerHTML: '#',
				title: 'exception',
				onclick: function(msg){
					log.popup(msg.stack.escapeHTML());
				}.bind(msg,msg)
			});
			li.appendChild(a);
		}else{
			log.write(msg, {className: 'error', title: 'Error'});
		}
	},
	
	profilers: $H({}),
	profile: function (label) {
		var begin = log.profilers.get(label);
		if( !begin ){
			log.profilers.set(label, new Date());
			log.write(label + ' <small>start</small>', {className: 'profile begin'});
		}else{
			log.profilers.unset(label);
			var end = new Date();
			log.write(label + '  <small>end (' + (end-begin) + 'ms)</small>', {className: 'profile end'});
		}
	}
};

log.load();

