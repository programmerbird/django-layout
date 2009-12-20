#-*- coding:utf-8 -*-

from django.conf import settings
import re 

VIDEO_WIDTH = getattr(settings, 'VIDEO_WIDTH', 560)
VIDEO_HEIGHT = getattr(settings, 'VIDEO_HEIGHT', 340)

def vimeo_pre(matches):
	video = matches.group(1)
	return "[vimeo:%s]" % video
	
def vimeo(matches):
	video = matches.group(1)
	width = VIDEO_WIDTH
	height = VIDEO_HEIGHT
	return """<object class="vimeo video" width="%(width)d" height="%(height)d"><param name="allowfullscreen" value="true" />
<param name="allowscriptaccess" value="always" /><param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=%(video)s&server=vimeo.com&show_title=1&show_byline=1&show_portrait=0&color=&fullscreen=1" />
<embed src="http://vimeo.com/moogaloop.swf?clip_id=%(video)s&server=vimeo.com&show_title=1&show_byline=1&show_portrait=0&color=&fullscreen=1" 
type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="always" width="%(width)d" height="%(height)d"></embed></object>""" % locals()
	
VIDEO_LINKS = (
	(re.compile(r'\&lt\;object.*?vimeo.com\/.*?clip_id\=(\d+)\&.*?\&lt\;\/object\&gt\;.*?Vimeo\&lt\;\/a\&gt\;\.\&lt\;\/p\&gt\;', re.DOTALL), vimeo_pre),
	(re.compile(r'\&lt\;object.*?vimeo.com\/.*?clip_id\=(\d+)\&.*?\&lt\;\/object\&gt\;', re.DOTALL), vimeo_pre),
	(re.compile(r'\<object.*?vimeo.com\/.*?clip_id\=(\d+)\&.*?\<\/object\>.*?Vimeo\<\/a\>\.\<\/p\>', re.DOTALL), vimeo_pre),
	(re.compile(r'\<object.*?vimeo.com\/.*?clip_id\=(\d+)\&.*?\<\/object\>', re.DOTALL), vimeo_pre),
	(re.compile(r'http\:\/\/[^\s]*?vimeo.com\/[^\s]*?clip_id\=(\d{5,})([^\d][^\s]*|)'), vimeo_pre),
	(re.compile(r'http\:\/\/[^\s]*?vimeo.com\/(\d{5,})([\?\&\#][^\s\n]*|)'), vimeo_pre),
	
	(re.compile(r'\<a href=\"\[vimeo:([^\]]+)\]\"\>\[vimeo\:([^\]]+)\]\<\/a\>'), r'[vimeo:\1]'),
	(re.compile(r'\[vimeo:([^\]]+)\]'), vimeo),	
)

def parse(txt):
	for pattern, replacement in VIDEO_LINKS:
		txt = pattern.sub(replacement, txt)
	return txt 
	
def main():
	testcases = """
	hello world 
	sdadasd

	ss
	<object width="400" height="225"><param name="allowfullscreen" value="true" /><param name="allowscriptaccess" value="always" /><param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=8115840&server=vimeo.com&show_title=1&show_byline=1&show_portrait=0&color=&fullscreen=1" /><embed src="http://vimeo.com/moogaloop.swf?clip_id=8115840&server=vimeo.com&show_title=1&show_byline=1&show_portrait=0&color=&fullscreen=1" type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="always" width="400" height="225"></embed></object>
	<p><a href="http://vimeo.com/8115840">Pony Pony Run Run - Walking on a line</a> from <a href="http://vimeo.com/user2072431">SoLab</a> on <a href="http://vimeo.com">Vimeo</a>.</p>
	ss

	vimeohh:
	<object width="400" height="225"><param name="allowfullscreen" value="true" /><param name="allowscriptaccess" value="always" /><param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=8115840&server=vimeo.com&show_title=1&show_byline=1&show_portrait=0&color=&fullscreen=1" /><embed src="http://vimeo.com/moogaloop.swf?clip_id=8115840&server=vimeo.com&show_title=1&show_byline=1&show_portrait=0&color=&fullscreen=1" type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="always" width="400" height="225"></embed></object>


	<object width="400" height="225"><param name="allowfullscreen" value="true" /><param name="allowscriptaccess" value="always" /><param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=8115840&server=vimeo.com&show_title=1&show_byline=1&show_portrait=0&color=&fullscreen=1" /><embed src="http://vimeo.com/moogaloop.swf?clip_id=8115840&server=vimeo.com&show_title=1&show_byline=1&show_portrait=0&color=&fullscreen=1" type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="always" width="400" height="225"></embed></object>

	""".split('\n\n\n')
	for x in testcases:
		for pattern, replacement in VIDEO_LINKS:
			x = pattern.sub(replacement, x)
		print "---"
		print x 

	print "MARKDOWN"
	import markdown
	for x in testcases:
		x = markdown.markdown(x, safe_mode="escape")
		for pattern, replacement in VIDEO_LINKS:
			x = pattern.sub(replacement, x)
		print "---"
		print x 

if __name__ == '__main__':
	import sys
	sys.exit(main())


