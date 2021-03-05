###############################################################################
# Make/Upload Rithm lectures
#
# This is a "Makefile"; it contains REAL TAB CHARACTERS and they MUST STAY
# as tabs. Your editor may (stupidly) try to convert these to spaces. That will
# break everything.


ifeq ($(origin RITHM_COHORT), undefined)
  $(info )
  $(info PANIC: don't know which cohort this is for. You must have an)
  $(info   environmental variable RITHM_COHORT)
  $(info )
  $(info You can do this in your .bashrc or .zshrc with a line like:)
  $(info )
  $(info export RITHM_COHORT=r8)
  $(info )
  $(error )
endif

SPHINXOPTS	= -n

NAME          = $(shell basename $(shell pwd))

# old way
SSH_HOST      = rithm@curric.rithmschool.com
SSH_DIR       = /var/www/html/$(RITHM_COHORT)/lectures/
SSH_URL	      = http://curric.rithmschool.com/$(RITHM_COHORT)/lectures/
SSH_DIR_SLIDE = /var/www/html/$(RITHM_COHORT)/slides/
SSH_URL_SLIDE = http://curric.rithmschool.com/$(RITHM_COHORT)/slides/

# new way
S3_BUCKET     = rithm-students-assets
URL_HANDOUT   = s3://$(S3_BUCKET)/$(RITHM_COHORT)/lectures/$(NAME)/handout
URL_REVEALJS  = s3://$(S3_BUCKET)/$(RITHM_COHORT)/lectures/$(NAME)/slides
URL_DEMO      = s3://$(S3_BUCKET)/$(RITHM_COHORT)/lectures/$(NAME)/demo.zip
URL_PDF       = s3://$(S3_BUCKET)/$(RITHM_COHORT)/lectures/$(NAME)/handout.pdf

export CURRIC_NAME=$(NAME)
ifneq ($(wildcard demo),)
	export DEMO_PATH=../$(NAME)-demo.zip
endif

# These things will never get zipped up, no matter how deep they
# may be in the tree of things that we may try to zip up
#
# For safety, we ignore all files starting with a dot. Note
# that this will prevent us from giving students demos or solutions
# with '.gitignore' or '.env' or such.

NEVER_ZIP = --exclude '*.rst' \
			--exclude '.[a-zA-Z0-9_]*' \
			--exclude 'venv' \
			--exclude '__pycache__' \
			--exclude 'node_modules' \
			--exclude 'meta' \
			--exclude 'rubric' \
			--exclude 'Makefile' \
			--exclude 'Untitled*.ipynb' \
			--exclude 'build' \
			--exclude '_build'

#NEVER_ZIP2 = -x\
# '.[a-zA-Z0-9_]*'\
# '*/venv'\
# '*/__pycache__'\
# '*/node_modules'\
# 'Untitled*.ipynb'\
# '*/build'



################################################################################
# You should probably not touch anything below here


SPHINXBUILD = sphinx-build
SOURCEDIR	= .
BUILDDIR    = _build

# Keep this first
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


################################################################################
# Glide-specific actions


# Make slides & open in browser (convenience)

revealjs-open: revealjs
	@open $(BUILDDIR)/revealjs/index.html

WATCHMEDO = watchmedo

# Make handouts & open in browser, then watch the filesystem for changes

watch-revealjs: revealjs-open
	@$(WATCHMEDO) shell-command \
			--patterns="*.rst;./demo/*" \
			--ignore-pattern='_build/*' \
			--recursive \
			--command='make revealjs-open; echo "waiting for changes"'


# Make handouts & open in browser (convenience)

handouts-open: handouts
	@open $(BUILDDIR)/handouts/index.html

# Make handouts & open in browser, then watch the filesystem for changes

watch-handouts: handouts-open
	@$(WATCHMEDO) shell-command \
			--patterns="*.rst;./demo/*" \
			--ignore-pattern='_build/*' \
			--recursive \
			--command='make handouts-open; echo "waiting for changes"'


# Zip up demo folder, if present (warns if no demo present)

# ln -fs ../demo _build/react-intro-demo
# (cd _build; zip -FS $(NEVER_ZIP) -r react-intro-demo react-intro-demo/)
demozip:
ifneq ($(wildcard demo),)
	@rm -rf /tmp/demo /tmp/$(NAME)-demo
	@tar -cL $(NEVER_ZIP) demo | tar -xC /tmp
	@mv /tmp/demo /tmp/$(NAME)-demo
	cd /tmp && zip -r $(NAME)-demo.zip $(NAME)-demo
else
	@echo "\n\nWARNING: no demo folder found; most lectures should have one\n\n"
endif


# Uploads slides --- see "upload", below

revealjs-upload: revealjs
	ssh $(SSH_HOST) rm -rf $(SSH_DIR_SLIDE)$(NAME)
	scp -r _build/revealjs $(SSH_HOST):$(SSH_DIR_SLIDE)$(NAME)
	open $(SSH_URL_SLIDE)$(NAME)


# Uploads handouts --- see "upload", below

handouts-upload: handouts demozip
	ssh $(SSH_HOST) rm -rf $(SSH_DIR)$(NAME)
	scp -r _build/handouts $(SSH_HOST):$(SSH_DIR)$(NAME)
	if [ -d demo ]; then scp /tmp/$(NAME)-demo.zip $(SSH_HOST):$(SSH_DIR); fi
	open $(SSH_URL)$(NAME)

handouts-s3: handouts demozip
	aws s3 sync _build/handouts $(URL_HANDOUT) --acl public-read --exclude .buildinfo --exclude objects.inv
	#aws s3api put-object-acl --bucket $(S3_BUCKET) --key $(RITHM_COHORT)/handout/$(NAME)/index.html --acl authenticated-read
	http https://$(RITHM_COHORT).students.rithmschool.com/api-glide/lecture/$(NAME)/upload/handout/ url=$(URL_HANDOUT)/index.html --ignore-stdin
	if [ -d demo ]; then aws s3 mv /tmp/$(NAME)-demo.zip $(URL_DEMO) --acl public-read --content-disposition='attachment;filename=$(NAME)-demo.zip'; fi
	if [ -d demo ]; then  http https://$(RITHM_COHORT).students.rithmschool.com/api-glide/lecture/$(NAME)/upload/code/ url=$(URL_DEMO) title=Demo --ignore-stdin; fi
	if [ -f /usr/local/bin/prince ]; then make prince; fi
	if [ -f /usr/local/bin/prince ]; then aws s3 mv _build/handouts/index.pdf $(URL_PDF) --acl public-read; fi
	if [ -f /usr/local/bin/prince ]; then http https://$(RITHM_COHORT).students.rithmschool.com/api-glide/lecture/$(NAME)/upload/handout-pdf/ url=$(URL_PDF) --ignore-stdin; fi
	open `aws s3 presign $(URL_HANDOUT)/index.html`

revealjs-s3: revealjs demozip
	aws s3 sync _build/revealjs $(URL_REVEALJS) --acl public-read --exclude .buildinfo --exclude objects.inv
	#aws s3api put-object-acl --bucket $(S3_BUCKET) --key $(RITHM_COHORT)/handout/$(NAME)/index.html --acl authenticated-read
	http https://$(RITHM_COHORT).students.rithmschool.com/api-glide/lecture/$(NAME)/upload/slides/ url=$(URL_REVEALJS)/index.html status=private is_logged=0 --ignore-stdin
	open `aws s3 presign $(URL_REVEALJS)/index.html`

# Upload everything & tidy up temp files --- this is what you want for upload

upload: revealjs-upload handouts-upload
	rm -f /tmp/$(NAME).zip
	rm -rf $(BUILDDIR)/*

upload-s3: revealjs-s3 handouts-s3
	rm -f /tmp/$(NAME).zip
	rm -rf $(BUILDDIR)/*


# Make PDFs

prince:
	make clean && make handouts SPHINXOPTS="-c ../.. -D html_add_permalinks="
	prince -j _build/handouts/index.html
	#open _build/handouts/index.pdf

list:
	$(info upload		build and upload all lecture material to the production server)
	$(info handouts-open		build and open the index file locally)
	$(info watch-handouts		build and open the index every time there is a file change)
	$(info revealjs-open		build and open revealjs slides locally)
	$(info watch-revealjs		build and open the revealjs slides every time there is a file change)

