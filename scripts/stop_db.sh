#!/bin/bash
kill `ps -ef | grep 'mongod' | grep -v grep | awk '{print $2}'`