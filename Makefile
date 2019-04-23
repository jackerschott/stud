first: target

target: src/stud.py
	pyinstaller --onefile src/stud.py --specpath tmp/spec --distpath bin --workpath tmp/build

install: setup/install.py
	@python3 setup/install.py

uninstall: setup/uninstall.py
	@python3 setup/uninstall.py

clean:
	rm -r tmp/*
