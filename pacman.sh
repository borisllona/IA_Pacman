#!/bin/bash
ulimit -t 5
python2.7 pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5