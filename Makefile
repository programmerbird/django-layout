all:
	make -C media

messages:
	find . -name "locale" | sed 's/^/cd /g' | sed 's@locale@ \&\& django-admin.py makemessages -l th \&\& cd ../@g' | sh
	find . -name "locale" | sed 's/^/cd /g' | sed 's@locale@ \&\& django-admin.py makemessages -l en \&\& cd ../@g' | sh

compilemessages:
	find . -name "locale" | sed 's/^/cd /g' | sed 's@locale@ \&\& django-admin.py compilemessages \&\& cd ../@g' | sh

                                                                                                                                         
