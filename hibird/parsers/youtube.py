#-*- coding:utf-8 -*-

import re 
from django.conf import settings

VIDEO_WIDTH = getattr(settings, 'VIDEO_WIDTH', 560)
VIDEO_HEIGHT = getattr(settings, 'VIDEO_HEIGHT', 340)

def youtube_pre(matches):
	video = matches.group(1)
	return "[youtube:%s]" % video

def youtube(matches):
	video = matches.group(1)
	width = VIDEO_WIDTH
	height = VIDEO_HEIGHT
	return """<object class="youtube video" width="%(width)d" height="%(height)d"><param name="movie" value="http://www.youtube.com/v/%(video)s&hl=en_US&fs=1&">
</param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param>
<embed src="http://www.youtube.com/v/%(video)s&hl=en_US&fs=1&" type="application/x-shockwave-flash" 
allowscriptaccess="always" allowfullscreen="true" width="%(width)d" height="%(height)d"></embed></object>""" % locals()

VIDEO_LINKS = (
	(re.compile(r'\&lt\;object.*?youtube.com\/v\/([^\&\"]*)[\&\"\n\s].*?\&lt\;\/object\&gt\;', re.DOTALL), youtube_pre),
	(re.compile(r'\<object.*?youtube.com\/v\/([^\&\"]*)[\&\"\n\s].*?\<\/object\>', re.DOTALL), youtube_pre),
	(re.compile(r'http\:\/\/[^\s]*?youtube.com\/watch\?v\=([\w\d]*)([\&\#][^\s\n]*|)'), youtube_pre),
	(re.compile(r'http\:\/\/[^\s]*?youtube.com\/v\/\=([^\&\"\s]*)([\&\#][^\s]*|)'), youtube_pre),
	
	(re.compile(r'\<a href=\"\[youtube:([^\]]+)\]\"\>\[youtube\:([^\]]+)\]\<\/a\>'), r'[youtube:\1]'),
	(re.compile(r'\[youtube:([^\]]+)\]'), youtube),
)

def parse(txt):
	for pattern, replacement in VIDEO_LINKS:
		txt = pattern.sub(replacement, txt)
	return txt 
	
def main():
	testcases = """
hello world 
http://www.youtube.com/watch?v=eIO5Qebk3dI
ss http://www.youtube.com/watch?v=eIO5Qebk3dI&feature=featured test
sdadasd

hello world 
http://www.youtube.com/watch?v=eIO5Qebk3dI


hello world youtube
<object width="560" height="340"><param name="movie" value="http://www.youtube.com/v/eIO5Qebk3dI&hl=en_US&fs=1&"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/eIO5Qebk3dI&hl=en_US&fs=1&" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="560" height="340"></embed></object>



hello world 
<object width="560" height="340"><param name="movie" value="http://www.youtube.com/v/eIO5Qebk3dI&hl=en_US&fs=1&">
</param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param>
<embed src="http://www.youtube.com/v/eIO5Qebk3dI&hl=en_US&fs=1&" type="application/x-shockwave-flash" 
allowscriptaccess="always" allowfullscreen="true" width="560" height="340"></embed></object>

hello world 
<object width="560" height="340">
<param name="movie" value="http://www.youtube.com/v/eIO5Qebk3dI&hl=en_US&fs=1&"></param>
<param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param>
<embed src="http://www.youtube.com/v/eIO5Qebk3dI&hl=en_US&fs=1&" type="application/x-shockwave-flash" 
allowscriptaccess="always" allowfullscreen="true" width="560" height="340"></embed>
</object>

http://www.youtube.com/watch?v=eIO5Qebk3dI
http://www.youtube.com/watch?v=eIO5Qebk3dI&feature=featured
http://www.youtube.com/watch?v=eIO5Qebk3dI

<object width="400" height="225"><param name="allowfullscreen" value="true" /><param name="allowscriptaccess" value="always" /><param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=8115840&server=vimeo.com&show_title=1&show_byline=1&show_portrait=0&color=&fullscreen=1" /><embed src="http://vimeo.com/moogaloop.swf?clip_id=8115840&server=vimeo.com&show_title=1&show_byline=1&show_portrait=0&color=&fullscreen=1" type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="always" width="400" height="225"></embed></object>


<http://www.youtube.com/watch?v=eIO5Qebk3dI>

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


