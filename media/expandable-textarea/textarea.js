/*
 *	textarearesizer.js
 *	
 *	Prototype port of the jQuery TextAreaResizer 
 *	Created on 14th November 2008 by Sam Burney <sburney@sifnt.net.au>
 *	Version 0.1
 *
 *	More info: http://samburney.com/blog/text-area-resizer-prototype-port
 *	Demo: http://stmarys.sifnt.net.au/~sam/textarearesizer/
 *	Original version: http://plugins.jquery.com/project/TextAreaResizer
 */
function TextAreaResizer(id, options){
	this.textarea = id;
	this.staticOffset;
	this.iLastMousePos = 0;
	this.iMin = 32;
	this.grip;
	this.options = options;
	
	this.init();
};

TextAreaResizer.prototype.init = function(){
		this.textarea.addClassName('processed')
		this.staticOffset = null;

		var span = new Element('span');
		Element.wrap(this.textarea, span);
		span.wrap(new Element('div', {'class': 'resizable-textarea'}));
		
		var grippie = new Element('div', {'class': 'grippie'});
		span.parentNode.insert(grippie);
		// grippie.style.marginRight = (grippie.getWidth() - this.textarea.getWidth()) +'px';
		
		Event.observe(grippie, 'mousedown', this.startDrag.bindAsEventListener(this));
};

TextAreaResizer.prototype.startDrag = function(event){
	var data = $A(arguments);
	data.shift();
	
	this.textarea = $(Event.element(event)).previous().firstDescendant();
	
	this.iLastMousePos = event.pointerY();
	this.staticOffset = this.textarea.getHeight() - this.iLastMousePos;
	this.textarea.setStyle({'opacity': 0.25});
	
	Event.observe(document, 'mousemove', this.performDrag.bindAsEventListener(this));
	Event.observe(document, 'mouseup', this.endDrag.bindAsEventListener(this));
	
	return false;
};

TextAreaResizer.prototype.performDrag = function(event){
	var data = $A(arguments);
	data.shift();

	var iThisMousePos = event.pointerY();
	var iMousePos = this.staticOffset + iThisMousePos;
	if(this.iLastMousePos >= (iThisMousePos)){
		iMousePos -= 5;
	}
	this.iLastMousePos = iThisMousePos;
	iMousePos = Math.max(this.iMin, iMousePos);
	this.textarea.setStyle({height: iMousePos + 'px'});
	if(iMousePos < this.iMin){
		this.endDrag(event);
	}

	return false;
};

TextAreaResizer.prototype.endDrag = function(event){
	var data = $A(arguments);
	data.shift();

	Event.stopObserving(document, 'mousemove');
	Event.stopObserving(document, 'mouseup');
	
	this.textarea.setStyle({'opacity': 1});
	this.textarea.focus();
	this.staticOffset = null;
	this.textarea = null;
	this.iLastMousePos = 0;

	if(this.options){
		if(this.options.afterDrag){
			this.options.afterDrag();
		}
	}
};

