import sys, re
import StringIO

PROP_RULES = (
    (re.compile(ur'\s*([\,\!])\s*'), ur'\1'),
)
ATTR_RULES = (
    (re.compile(ur'^0(\w+)$'), ur'0'),
    (re.compile(ur'^0\.(\d+)(\w*)$'), ur'.\1\2'),
    (re.compile(ur'^#([\d\w]{6})$'), lambda x : x.group(0).lower()),
    (re.compile(ur'^#([\d\w])\1([\d\w])\2([\d\w])\3$'), ur'#\1\2\3'),
)
def clean(value):
    for (pattern, replacement) in PROP_RULES:
        value = pattern.sub(replacement, value)
    values = value.split(' ')
    result = []
    for x in values:
        for (pattern, replacement) in ATTR_RULES:
            x = pattern.sub(replacement, x)
        result += x,
    return ' '.join(result)
    
css = '\n'.join(sys.stdin.readlines())

# remove comments - this will break a lot of hacks :-P
css = re.sub( r'\s*/\*\s*\*/', "$$HACK1$$", css ) # preserve IE<6 comment hack
css = re.sub( r'/\*[\s\S]*?\*/', "", css )
css = css.replace( "$$HACK1$$", '/**/' ) # preserve IE<6 comment hack

# url() doesn't need quotes
css = re.sub( r'url\((["\'])([^)]*)\1\)', r'url(\2)', css )

# spaces may be safely collapsed as generated content will collapse them anyway
css = re.sub( r'\s+', ' ', css )

w = StringIO.StringIO()
for rule in re.findall( r'([^{]+){([^}]*)}', css ):

    # we don't need spaces around decendant, and sibling indicators
    selectors = [selector.strip() for selector in rule[0].split( ',' )]

    # order is important, but we still want to discard repetitions
    properties = {}
    porder = []
    for prop in re.findall( '(.*?):(.*?)(;|$)', rule[1] ):
        key = prop[0].strip().lower()
        if key not in porder: porder.append( key )
        properties[ key ] = prop[1].strip()
        
    porder.sort()
    # output rule if it contains any declarations
    if properties:
        w.write( ','.join( selectors ) + '{' + \
              ';'.join(['%s:%s' % (key, clean(properties[key])) for key in porder]) + '}')
              
print w.getvalue(),
w.close()

