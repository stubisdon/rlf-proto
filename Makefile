-include Makefile.def

TEST_APP=core test_pep8

runserver:
	@echo Starting $(PROJECT_NAME) ...
	IS_DEV=1 $(MANAGE) runserver $(BIND_TO):$(RUNSERVER_PORT)

run:
	@echo Starting $(PROJECT_NAME) ...
	IS_DEV=1 $(MANAGE) run_collecting $(BIND_TO):$(RUNSERVER_PORT)

mailserver:
	python -m smtpd -n -c DebuggingServer $(BIND_TO):$(MAILSERVER_PORT)

syncdb:
	@echo Syncing...
	$(MANAGE) makemigrations
	$(MANAGE) syncdb
	$(MANAGE) migrate
	@echo loading initial data
	$(MANAGE) loaddata $(PROJECT_NAME).json
	@echo Done

shell:
	@echo Starting shell...
	$(MANAGE) shell

testcoverage:
	mkdir -p tests/coverage/modules
	TESTING=1 $(MANAGE) test_coverage $(TEST_OPTIONS) $(TEST_APP)

test:
	TESTING=1 $(MANAGE) test $(TEST_OPTIONS) $(TEST_APP)

fast_test:
	TESTING=1 FAST_TESTING=1 $(MANAGE) test $(TEST_OPTIONS) $(TEST_APP)

static:
	@echo Collecting static
	$(MANAGE) collectstatic --noinput
	@echo Done

compress: static
	@echo Compressing css and js
	-rm -rf ./$(PROJECT_NAME)/static_media/static_root/CACHE/*
	$(MANAGE) compress --force 
	@echo Done

clean:
	@echo Cleaning up...
	find ./$(PROJECT_NAME) | grep '\.pyc$$' | xargs -I {} rm {}
	@echo Done

manage:
ifndef CMD
	@echo Please, spceify -e CMD=command argument to execute
else
	$(MANAGE) $(CMD)
endif

only_migrate:
ifndef APP_NAME
	@echo Please, specify -e APP_NAME=appname argument
else
	@echo Starting of migration of $(APP_NAME)
	$(MANAGE) migrate $(APP_NAME)
	@echo Done
endif

migrate:
ifndef APP_NAME
	@echo "You can also specify -e APP_NAME='app' to check if new migrations needed for some app"
	$(MANAGE) migrate
else
	@echo Starting of migration of $(APP_NAME)
	$(MANAGE) schemamigration $(APP_NAME) --auto
	$(MANAGE) migrate $(APP_NAME)
	@echo Done
endif

init_migrate:
ifndef APP_NAME
	@echo Please, specify -e APP_NAME=appname argument
else
	@echo Starting init migration of $(APP_NAME)
	$(MANAGE) schemamigration $(APP_NAME) --initial
	$(MANAGE) migrate $(APP_NAME)
	@echo Done
endif

requirements:
	pip install -r requirements.txt
