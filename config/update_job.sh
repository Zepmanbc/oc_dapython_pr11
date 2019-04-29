cd ~/oc_dapython_pr10/
echo $(date) >> ~/log.txt
~/.local/bin/pipenv run purbeurre/manage.py fillindb 0 >> ~/log.txt 2>&1