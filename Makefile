clean:
	find -type f -iname '*.pyc' -exec rm {} \;
	find -type f -iname '.*.swp' -exec rm {} \;
	find -type f -iname '*~' -exec rm {} \;
	-rm error.log
offline:
	-rm error.log
	python offline.py
