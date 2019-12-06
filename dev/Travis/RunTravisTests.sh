#!/bin/bash

# From https://graysonkoonce.com/getting-the-current-branch-name-during-a-pull-request-in-travis-ci/
export FROM_BRANCH=$(if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then echo $TRAVIS_BRANCH; else echo $TRAVIS_PULL_REQUEST_BRANCH; fi)

echo "TRAVIS_BRANCH=$TRAVIS_BRANCH, PR=$PR, FROM_BRANCH=$FROM_BRANCH"

if [[ ($TRAVIS_BRANCH != $FROM_BRANCH) && ($TRAVIS_BRANCH == 'master') && ($FROM_BRANCH != 'development') ]];
then
    echo "*** Cannot Merge Branch '$FROM_BRANCH' into '$TRAVIS_BRANCH'"
    exit 1
else
    echo "No Merging Issue"
    exit 0
fi
