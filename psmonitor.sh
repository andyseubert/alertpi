#!/bin/bash
PID=$(pgrep remoteListener)

if [[ -z "$PID" ]]; then
  /root/remoteListener.py & > /var/log/alert.log 2>&1
fi
unset PID
