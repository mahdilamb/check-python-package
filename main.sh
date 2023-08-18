#!/bin/bash
pip install pyyaml
SCRIPT_PATH="$(dirname "$(readlink -fm "$0")")"

VERSION_PATH=$1
VERSION_VARIABLE=$2
DEFAULT_BRANCH=$3
CURRENT_BRANCH=$4


git fetch
git checkout $DEFAULT_BRANCH
git checkout $CURRENT_BRANCH

REQUIRES_CHANGE=$(python $SCRIPT_PATH/scripts/check_version.py $VERSION_PATH $VERSION_VARIABLE $DEFAULT_BRANCH)
if [ $? ]; then
    echo "Updating version number"
    python $SCRIPT_PATH/scripts/next_version.py $VERSION_PATH $VERSION_VARIABLE $DEFAULT_BRANCH
    git config user.name github-actions
    git config user.email github-actions@github.com
    git add $VERSION_PATH
    git commit -m "Update micro version"
    git push --set-upstream origin $CURRENT_BRANCH

fi
