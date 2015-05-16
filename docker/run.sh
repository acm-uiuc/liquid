#! /bin/bash -e

cd /liquid

if [ -n "$LOCAL_SETTINGS" ]; then
    cp "$LOCAL_SETTINGS" app/local_settings.py
fi

if [ -n "$RUN_SETUP" ]; then
    python setup.py
fi

exec supervisord -n
