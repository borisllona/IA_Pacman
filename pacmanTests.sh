#!/bin/bash

testUCS(){
    echo ""
    echo "--- Testeando UCS ---"
    echo ""
    timeout 5 python2.7 pacman.py -l ./test.lay -p SearchAgent -a fn=ucs -q
    echo "                ******"
}
testBFSH(){
    echo "" 
    echo "--- Testeando BestFS con la heuristica ${1} ---" 
    echo ""
    timeout 5 python2.7 pacman.py -l test.lay -p SearchAgent -a fn=bfsh,heuristic=$1 -q
    echo "                ******"
}
testAStar(){
    echo ""
    echo "--- Testeando A* con la heuristica ${1} ---" 
    echo ""
    timeout 5 python2.7 pacman.py -l test.lay -p SearchAgent -a fn=astar,heuristic=$1 -q
    echo "                ******"
}

testBDS(){
    truncate -s 0 executionResults.txt #Clears the content of result.txt file
    
    #testNAMEALGORITHM [<heuristic>]

    #It generates a random map and its analyzed by each algorithm
    for i in {1..5}
    do
        r=$((1 + RANDOM % 4))
        python2.7 gmap.py 50 50 0.${r} $((RANDOM)) > ./layouts/test.lay
        timeout 5 python2.7 pacman.py -l test.lay -p SearchAgent -a fn=bfs,heuristic=$1 -q
        timeout 5 python2.7 pacman.py -l test.lay -p SearchAgent -a fn=bds,heuristic=$1 -q
        echo "***********"
        
    done     
}


#Tests control function
testDiferentAlgorithms(){
    truncate -s 0 executionResults.txt #Clears the content of result.txt file
    
    #testNAMEALGORITHM [<heuristic>]

    #It generates a random map and its analyzed by each algorithm
    for i in $(seq 1 $3)
    do
        r=$((1 + RANDOM % 4))
        python2.7 gmap.py $1 $2 0.${r} $((RANDOM)) > ./layouts/test.lay
        testUCS 
        testBFSH manhattanHeuristic 
        testBFSH euclideanHeuristic 
        testAStar manhattanHeuristic 
        testAStar euclideanHeuristic 
        echo '' >> 'executionResults.txt'
        echo '@' >> 'executionResults.txt'
    done     
}

test(){
    touch executionResults.txt

    #testDiferentAlgorithms <Width> <Height> <Number of random maps>
    testDiferentAlgorithms 20 20 20
    cp executionResults.txt ./testResults/resultsSmall.txt
    testDiferentAlgorithms 100 100 10
    cp executionResults.txt ./testResults/resultsMedium.txt
    testDiferentAlgorithms 500 500 5
    cp executionResults.txt ./testResults/resultsBig.txt

    rm executionResults.txt
    cd testResults
    python analyzeResults.py
}

test
#testBDS

