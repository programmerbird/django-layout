
(function() {var ua=navigator.userAgent.toLowerCase(),is=function(t){return ua.indexOf(t) != -1;},h=document.getElementsByTagName('html')[0],b=(!(/opera|webtv/i.test(ua))&&/msie\s(\d)/.test(ua))?('ie ie'+RegExp.$1):is('firefox/2')?'gecko ff2':is('firefox/3')?'gecko ff3':is('gecko/')?'gecko':is('opera/9')?'opera opera9':/opera\s(\d)/.test(ua)?'opera opera'+RegExp.$1:is('konqueror')?'konqueror':is('chrome')?'chrome webkit safari':is('applewebkit/')?'webkit safari':is('mozilla/')?'gecko':'',os=(is('x11')||is('linux'))?' linux':is('mac')?' mac':is('win')?' win':'';var c=b+os+' js'; h.className += h.className?' '+c:c;})();


