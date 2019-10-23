#!/bin/bash

testUCS(){
    echo ""
    echo "--- Testeando UCS ---"
    echo ""
    for i in $(seq 1 $3)
    do
        r=$((1 + RANDOM % 4))
        python2.7 gmap.py $1 $2 0.${r} $((RANDOM)) > ./layouts/test.lay
        timeout 3 python2.7 pacman.py -l ./test.lay -p SearchAgent -a fn=ucs -q
        echo "                ******"
    done
}
testAStar(){
    echo ""
    echo "--- Testeando A* con la heuristica ${1} ---" 
    echo ""
    for i in $(seq 1 $4)
    do
        r=$((1 + RANDOM % 4))
        python2.7 gmap.py $2 $3 0.${r} $((RANDOM)) > ./layouts/test.lay
        timeout 3 python2.7 pacman.py -l test.lay -p SearchAgent -a fn=astar,heuristic=$1 -q
        echo "                ******"
    done
}
testBFSH(){
    echo "" 
    echo "--- Testeando BestFS con la heuristica ${1} ---" 
    echo ""
    for i in $(seq 1 $4)
    do
        r=$((1 + RANDOM % 4))
        python2.7 gmap.py $2 $3 0.${r} $((RANDOM)) > ./layouts/test.lay
        timeout 3 python2.7 pacman.py -l test.lay -p SearchAgent -a fn=bfsh,heuristic=$1 -q
        echo "                ******"
    done
}

#Tests control function
testDiferentAlgorithms(){
    truncate -s 0 executionResults.txt #Clears the content of result.txt file
    
    #testNAMEALGORITHM [<heuristic>] <Width> <Height> <Number repetitions>

    #testUCS 40 50 50
    testBFSH manhattanHeuristic 300 200 5
    #testBFSH euclideanHeuristic 20 20 50 
    #testAStar manhattanHeuristic 20 30 50
    #testAStar euclideanHeuristic 20 15 50
}
#Average nodes expanded from diferent random medium layouts 

testDiferentAlgorithms