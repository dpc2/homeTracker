#!/bin/bash

cd /home/danny/scripts/venv/plantFlask/
git add static/images/
git status |
if grep -q "new file:" $1; then
        git add database.db
        git commit -m "Db + picture update"
        git push
else
	:
fi

