all:
	@find . -name "Makefile" | grep -v "\./Makefile" | sed "s/\.\//make -C /g" | sed "s/Makefile//g" | sh | grep -v "Leaving directory" | grep -v "is up to date"
