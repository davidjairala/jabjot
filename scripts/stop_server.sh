#!/bin/bash
kill `ps -ef | grep 'nginx' | grep -v grep | awk '{print $2}'`