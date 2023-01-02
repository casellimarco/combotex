install:
	pip install -e .

install-mac:
	pip3 install -e .

install-latex:
	sudo apt-get install texlive-pictures texlive-science texlive-latex-extra latexmk

install-latex-mac:
	brew install texlive