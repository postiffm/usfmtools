#!/bin/bash

echo "Finding the top-level folder locations of all mp3 files in this"
echo "  folder and below recursively. This could take a few seconds."

find . -name *.mp3 | awk -F '/' '{print $2}' | sort | uniq
