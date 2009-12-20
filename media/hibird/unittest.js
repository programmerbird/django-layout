hibird.unittest = {
	testCases: $A([]),
	
	testContainer: null,
	testContainerBody: null,
	logContainer: null,
	
	load: function (options){
		var obj = hibird.unittest;
		var initial = {};
		$H(initial).each(function (pair){
			obj[pair.key] = pair.value;
		});
		if(options){
			$H(options).each(function (pair){
				obj[pair.key] = pair.value;
			});
		}
		
		var ele = function (tagName, innerHTML, className){
			var n = document.createElement(tagName);
			if(innerHTML) n.innerHTML = innerHTML;
			if(className) n.className = className;
			return n;
			
		};
		if (obj.testContainer){
			var t = ele('table');
			var h = ele('thead');
			t.appendChild(h);
			h.appendChild(ele('th', 'Test Case', 'testCase'));
			h.appendChild(ele('th', 'Success', 'success'));
			h.appendChild(ele('th', 'Fails', 'fails'));
			h.appendChild(ele('th', 'Errors', 'errors'));
			
			var b = ele('tbody');
			t.appendChild(b); 
			b.appendChild(ele('tr'));
			
			obj.testContainer.appendChild(t);
			obj.testContainerBody = b;
		}
	},
	run: function (){
		hibird.unittest.testCases.each(function (testCase){
			testCase.run();
		});
	},
	
	add: function (options){
		var unit = {};
		hibird.extend(unit, hibird.unittest.TestCase);
		unit.load(options);
		
		unit.log = hibird.unittest.log.bind(unit, unit);
		unit.appendResult = hibird.unittest.appendResult.bind(unit, unit);
		
		hibird.unittest.testCases.push(unit);
	},
	
	appendResult: function (testCase, methodName){
		if(hibird.unittest.testContainerBody){
			var td = function (className, innerHTML){
				var d = document.createElement('td');
				d.className = className;
				d.innerHTML = innerHTML;
				return d;
			};
			var tr = document.createElement('tr');
			if(testCase.fails > 0 || testCase.errors > 0){
				tr.className = 'fail';
			}else{
				tr.className = 'success';
			}

			tr.appendChild(td('testCase', methodName));
			tr.appendChild(td('success', testCase.success));
			tr.appendChild(td('fails', testCase.fails));
			tr.appendChild(td('errors', testCase.errors));
			
			hibird.unittest.testContainerBody.appendChild(tr);
			
		}
	},
	
	log: function (unit, msg){
		if(hibird.unittest.logContainer){
			var li = document.createElement('li');
			li.innerHTML = msg;
			hibird.unittest.logContainer.appendChild(li);
		}
	},
	
	getFunctionName: function (theFunction){
		// mozilla makes it easy. I love mozilla.
		if(theFunction.name && theFunction.name != ""){
			return theFunction.name;
		}
		
		// try to parse the function name from the defintion
		var definition = theFunction.toString();
		var name = definition.substring(definition.indexOf('function') + 8,definition.indexOf('('));
		if(name && !name.match(/^\s*$/))
			return name;

		return definition;
		
		// sometimes there won't be a function name 
		// like for dynamic functions
		return "anonymous";
	},

	getSignature: function (theFunction) { 
		var signature = hibird.unittest.getFunctionName(theFunction); 
		signature += "("; 
		
		for(var x=0; x<theFunction.arguments.length; x++) { 
			// trim long arguments 
			try{
				var nextArgument = theFunction.arguments[x]; 
				if(nextArgument && nextArgument.length > 30) 
					nextArgument = nextArgument.substring(0, 30) + "..."; 
				// apend the next argument to the signature 
				signature += "'" + nextArgument + "'"; 
				// comma separator 
				if(x < theFunction.arguments.length - 1) signature += ", "; 
			}catch(e){}
		} 
		signature += ")"; 
		return signature; 
	}, 
	
	stackTrace: function (startingPoint) { 
		var stackTraceMessage = "<ul title='Stack trace'>\n"; 
		var nextCaller = startingPoint; 
		var limit = 10;
		while(nextCaller && limit >=0 ) { 
			stackTraceMessage += '<li>' + hibird.unittest.getSignature(nextCaller) + "</li>\n"; 
			nextCaller = nextCaller.caller; 
			limit--;
		} 
		if(!limit){
			stackTraceMessage += "<li>...</li>\n"; 
		}
		stackTraceMessage += "</ul>\n\n"; // display message 
		return stackTraceMessage;
	} 
};

hibird.unittest.TestCase = {
	fails: 0,
	errors: 0,
	success: 0,
	
	description: null,
	
	run: function (unit){
		for (var definition in unit){
			if(Object.isFunction( unit[definition] )){
				if (definition.match(/^test/)){
					try{
					
						if(unit.setUp){
							unit.setUp();
						}
						
						unit.fails = 0;
						unit.errors = 0;
						unit.success = 0;
						
						unit[definition]();						
						unit.appendResult(definition);
						
						if(unit.tearDown){
							unit.tearDown();
						}

					}catch(e){
						unit.log(e.message);
						unit.log(hibird.unittest.stackTrace(e.callee));
						unit.fails++;
					}
				}
			}
		}
	},
	
	log: function (unit, msg){
		alert(msg);
	},
	
	appendResult: function (unit, methodName){
		alert(methodName);
	},
	
	assert: function (unit, object, msg){
		if(object){
			unit.success++;
		}else{
			unit.fails++;
			unit.log(msg);
			unit.log(hibird.unittest.stackTrace(arguments.callee));
		}
	},
	
	assertEqual: function (unit, object, value, msg){
		if(!msg){
			msg = 'expect: ' + object + ' == ' + value;
		}
		unit.assert(object==value, msg);
	},
	
	assertNotEqual: function (unit, object, value, msg){
		if(!msg){
			msg = 'expect: ' + object + ' <> ' + value;
		}
		unit.assert(object!=value, msg);
	},
	
	assertContains: function (unit, haysack, needle, msg){
		if(!msg){
			msg = 'expect: ' + needle + ' in '+ haysack;
		}
		unit.assert(haysack.indexOf(needle) > 0	, msg);
	},
	
	load: function (unit, options) {
		var obj = unit;
		var initial = {};
		$H(initial).each(function (pair){
			obj[pair.key] = pair.value;
		});
		if(options){
			$H(options).each(function (pair){
				obj[pair.key] = pair.value;
			});
		}
	}
}
