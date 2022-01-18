all: clean_app app

run: clean_app app
	mkdir -p ./files
	./gen.py --type good

test: clean gen app
	./test.sh

app:
	gcc -O2 -g -Wall -Wpedantic -Wextra -Werror ./main.c -o ./app -lz

gen:
	mkdir -p ./files
	./gen.py --type bad
	./gen.py --type good
	./gen.py --type empty
	./gen.py --type size

clean_app:
	rm -vf ./app

clean_files:
	rm -rvf ./files

clean: clean_app clean_files
