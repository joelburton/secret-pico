SPHINXBUILD = sphinx-build
SOURCEDIR	= .
BUILDDIR    = _build

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

upload: handouts
	surge _build/handouts secret-pico.surge.joelburton.com

