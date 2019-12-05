#!/bin/bash

PACKAGE_ROOT=ozpricechecker
SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJ_MAIN_DIR=$SCRIPT_PATH/../..

echo SCRIPT_PATH: $SCRIPT_PATH
echo PROJ_MAIN_DIR: $PROJ_MAIN_DIR

pushd "$PROJ_MAIN_DIR/$PACKAGE_ROOT"
# Test directories are specified in Pytest.ini
python manage.py test
return_code=$?

if [[ $return_code -eq  0 ]];
then
    echo "*** No Issues Found"
else
    echo "*** Some Issues Found"
fi

echo "exit $return_code"
popd
exit $return_code
