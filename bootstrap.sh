[ ! -f bin/pip ] && virtualenv .
bin/pip install --upgrade pip setuptools zc.buildout
bin/buildout -c $1 annotate | tee annotate.txt | grep -E 'setuptools *= *[0-9][^ ]*|zc.buildout *= *[0-9][^ ]*'| sed 's/= /==/' > requirements.txt
cat annotate.txt
cat requirements.txt
bin/pip install --upgrade -r requirements.txt