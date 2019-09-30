#!/bin/bash

SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJ_MAIN_DIR=$SCRIPT_PATH/..
TEST_SERVER_DIR=$PROJ_MAIN_DIR/tests/TestServerContent

# --directory only available since Python 3.7 - So need to push to directory
pushd "$TEST_SERVER_DIR"

if [ "$1" != "" ]; then
    echo "Argument Found, run detached"
    python -m http.server --bind localhost 8000 &
else
    echo "No Argument Found, run attached"
    python -m http.server --bind localhost 8000
fi

popd
