

(function () {
	var definitions = {};
	var wid = 0;
	
	var loadForm = function (widget_name, callback){
		try{
		if(!definitions[widget_name]){
			new Ajax.Request(publisher.views.api_widget_form, {
				method: 'get', 
				parameters: {'name': widget_name},
				onSuccess: function (transport){
					definitions[widget_name] = transport.responseText;
					callback(definitions[widget_name]);
				}
			});
		}else{
			callback(definitions[widget_name]);
		}
		}catch(e){}
	};
	
	var getInputs = function (e){
		return $(e).select('input, textarea, select, radio, textarea');
	};
	
	var resetInputs = function (e){
		getInputs(e).each(function (i){
			i.value = i.retrieve('default');
		});
	};
	
	var getContext = function (form){
		result = {}; 
		getInputs(form).each(function (input){
			if(input.type=='checkbox'){
				result[input.name] = input.checked;
			}else{
				result[input.name] = input.value;
			}
		});
		return result; 
	};
	
	var setContext = function (form, context){
		$H(context).each(function (pair){
			var input = $(form).select('[name='+pair.key+']').first();
			if(input && input.type=='checkbox'){
				input.checked = pair.value;
			}else{
				input.value = pair.value;
			}
			if(input.hook_change){
				input.hook_change.bind(input)();
			}
		});
	};
		
	var updateContext = function (form){
		var context = getContext(form); 
		var widget = form.retrieve('widget');
		widget.store('context', context);
	};
	
	var showWidgetProperty = function (widget){
		try{
		var widget_name = widget.retrieve('widget_name');
		loadForm(widget_name, function (html) {
			var selectedWidget = $$('.selected.widget').first();
			if(selectedWidget == null || selectedWidget.id!=widget.id) return;
			
			var form = $('widget-properties');
			form.update(html);
			form.highlight({duration: 0.3});
			form.store('widget', widget);
			getInputs(form).each(function (i){
				i.onchange = i.onkeyup = function () {
					updateContext(form);
				};
			});
			var context = widget.retrieve('context');
			if(context){
				setContext(form, context);
			}
			
		});
		}catch(e){}
	};
	
	var widgetDidSelect = function () {
		$$('li.widget').invoke('removeClassName', 'selected');
		$(this).addClassName('selected');
		
		showWidgetProperty(this);
	};
	
	var removeWidget = function (widget){
		widget.slideUp({duration: 0.3, afterFinish: function () { widget.remove() }.bind(widget)});
		return false;
	};
	var addWidget = function (widget_name, destination, context){
		if (!context) context = {};
		var li = new Element('li', {'class':'widget'});
		var h4 = new Element('h4');
		var a = new Element('a', {'href': '#'});
		a.update('remove');
		
		li.id = 'widget-'+(wid++);
		h4.update(widget_name);
		li.insert({bottom: h4});
		li.insert({bottom: a});
		$(destination).appendChild(li);
		
		li.store('widget_name', widget_name);
		li.store('context', context);
		li.onclick = widgetDidSelect;
		a.onclick = removeWidget.bind(li, li);
		return li;
	};
	
	var updateContainers = function () {
		var uls = $$('#layout-containers ul');
		var ids = [];
		for(var i=0, len=uls.length; i<len; ++i){
			var ul = uls[i];
			ids.push(ul.id);
		}
		
		ids.push('widgets');
		
		for(var i=0, len=uls.length; i<len; ++i){
			var ul=uls[i];
			Sortable.destroy(ul.id);
			Sortable.create(ul.id, {
				tag: 'li', 
				only: 'widget',
				hoverclass: 'hover',
				constraint: null,
				dropOnEmpty: true,
				containment: ids
			});
		}
	};
	
	var getContainersJSON = function () {
		result = {};
		$$('#layout-containers ul').each(function (container){
			var container_name = container.id.replace('layout-', '');
			var widgets = [];
			var hasChild = false;
			container.select('li.widget').each(function (widget){
				hasChild = true;
				widgets.push([
					widget.retrieve('widget_name'),
					widget.retrieve('context')
				]);
			});
			if(hasChild){
				result[container_name] = widgets;
			}else{
				result[container_name] = [];
			}
		});
		return Object.toJSON(result);
	};
	
	var setContainersByJSON = function (json){
		var containers = json.evalJSON();
		try{
		$H(containers).each(function (pair){
			var container_name = pair.key;
			var widgets = pair.value;
			$A(widgets).each(function (widget){
				addWidget(widget[0], 'layout-' + container_name, widget[1]);
			});
		});
		}catch(e){alert("a"+e)}
		updateContainers();
	};

	var submitButtonDidClick = function (ev) {
		try{
		$('id_containers').value = getContainersJSON();
		$('main-form').submit();
		ev.preventDefault();
		}catch(e){}
	};
	
	document.observe("dom:loaded", function () {
		try{
		setContainersByJSON( $('id_containers').value);
		}catch(e){}
		updateContainers();
		$('btn-submit').observe('click', submitButtonDidClick);
		
		var lis = $$('#widgets li');
		for(var i=0, len=lis.length; i<len; ++i){
			var li = lis[i];
			li.observe('click', function (ev) {
			try{
				widget_name = $(this).select('h4').first().innerHTML;
				var widget = addWidget(widget_name, 'layout-article');
				widget.highlight({afterFinish: function () {
					widget.style.backgroundColor = '';
				}});
				widgetDidSelect.bind(widget)();
				updateContainers();
				
				ev.preventDefault();
			}catch(e){}
			});
		}
		
	});

	
})();