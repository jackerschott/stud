BIN_PATH = $(HOME)/.local/bin
CONFIG_PATH = $(HOME)/.config/stud
STUD_PATH = $(HOME)/Documents/Studies

BIN = stud
CONFIG = studrc.json
MODULE_URLS = moduleUrls.json
CJAR = pt_cjar

first: stud

stud: src/$(BIN).py
	pyinstaller --onefile src/$(BIN).py --specpath tmp/spec --distpath bin --workpath tmp/build

clean:
	rm -r tmp/*


install: setup/studrc_gen.py setup/moduleFolders.py
	cp bin/$(BIN) $(BIN_PATH)/$(BIN)
	mkdir -p $(CONFIG_PATH)
	cp config/$(MODULE_URLS) $(CONFIG_PATH)/$(MODULE_URLS)

	@printf "\n"
	@python3 setup/studrc_gen.py -o $(CONFIG_PATH)/$(CONFIG)
	@printf "\n"

	mkdir -p $(STUD_PATH)
	@printf "\n"
	@python3 setup/moduleFolders.py $(CONFIG_PATH)/$(CONFIG) -o $(STUD_PATH)
	@printf "\n"

uninstall:
	rm -f $(CONFIG_PATH)/$(CONFIG)
	rm -f $(CONFIG_PATH)/$(MODULE_URLS)
	rm -f $(CONFIG_PATH)/$(CJAR)
	rmdir $(CONFIG_PATH)
	rm -f $(BIN_PATH)/$(BIN)
