# sigul

Forked version of sigul with ClearOS changes applied

## Update usage
  Add __#kojibuild__ to commit message to automatically build

* git clone git+ssh://git@github.com/clearos/sigul.git
* cd sigul
* git checkout master
* git remote add upstream git://pkgs.fedoraproject.org/sigul.git
* git pull upstream master
* git checkout clear7
* git merge --no-commit master
* git commit
