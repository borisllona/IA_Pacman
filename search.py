# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import sys
import node

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    n = node.Node(problem.getStartState(),None,None,0)
    if problem.isGoalState(n.state):
        return n.path()
    fringe = [n]    
    generated = {n.state:[n,'F']}
    while True:
        if len(fringe) == 0: 
            sys.stderr.write('No solution')
            sys.exit()
        n = fringe.pop() #Pila
        generated[n.state] = [n,'E']
        for state, action, cost in problem.getSuccessors(n.state):
            ns = node.Node(state,n,action,cost)
            if ns.state not in generated:
                if problem.isGoalState(ns.state): return ns.path()
                fringe.append(ns)
                generated[ns.state] = [ns,'F']

    util.raiseNotDefined()      

def breadthFirstSearch(problem):
    n = node.Node(problem.getStartState(),None,None,0)
    if problem.isGoalState(n.state):
        return n.path()
    fringe = [n]    
    generated = {n.state:[n,'F']}
    while True:
        if len(fringe) == 0: 
            sys.stderr.write('No solution')
            sys.exit()
        n = fringe.pop(0) #Queue
        generated[n.state] = [n,'E']
        for state, action, cost in problem.getSuccessors(n.state):
            ns = node.Node(state,n,action,cost)
            if ns.state not in generated:
                if problem.isGoalState(ns.state): return ns.path() #more eficient, we can also do it after extracting node from the fringe
                fringe.append(ns)                                               
                generated[ns.state] = [ns,'F']

    util.raiseNotDefined()        

def uniformCostSearch(problem):
    n = node.Node(problem.getStartState(),None,None,0)
    fringe = util.PriorityQueue()  #f(n) = g(n)
    fringe.push(n,n.cost)         
    generated = {n.state:[n,'F']} 
    while True:
        if fringe.isEmpty(): #No more paths to explore
            sys.stderr.write('No solution')
            sys.exit()
        n = fringe.pop()
        if problem.isGoalState(n.state): return n.path() #Its obligatory that has to be after extracting node from frindge.
        generated[n.state] = [n,'E']
        for state, action, cost in problem.getSuccessors(n.state): #Sucesors of the node
                ns = node.Node(state,n,action,cost)
                if ns.state not in generated:   #Add node to fringe if its not in fringe(to explore) and not in the expanded (explored) 
                    fringe.push(ns,ns.cost)
                    generated[ns.state] = [ns,'F']
                elif generated[ns.state][0].cost > ns.cost: #Update fringe if we can reach same state with less cost
                    fringe.push(ns,ns.cost)
                    generated[ns.state] = [ns,'F']
            
    util.raiseNotDefined()

def depthLimitedSearch(problem, k=5):
    while True:
        result = DLS(problem,k)
        if result[0] == 'Failure': #No result
            sys.exit()
        elif result[0] == 'True': #Result
            return result[1]    
        k+=1                   #Cutoff, we increase a k level

def DLS(problem=None,k=0):
    n = node.Node(problem.getStartState(),None,None,0)
    fringe = util.Stack()  #Same as pop
    fringe.push(n)         
    generated = {n.state:[n,'F']} 
    while True:
        if fringe.isEmpty(): #No more paths to explore
            return ('Failure',None)
        n = fringe.pop()
        if n.depth == k: return ("Cutoff",None) #We reached the max level, k is increased in main function.
        else:
            generated[n.state] = [n,'E']
            for state, action, cost in problem.getSuccessors(n.state): #Sucesors of the node
                    ns = node.Node(state,n,action,cost)
                    ns.depth = ns.parent.depth + 1
                    if ns.state not in generated:   #Add node to fringe if its not in fringe(to explore) and not in the expanded (explored) 
                        if problem.isGoalState(ns.state): return ('True',ns.path())
                        fringe.push(ns)
                        generated[ns.state] = [ns,'F']
            
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def bestFirstSearch(problem, heuristic=nullHeuristic):
    n = node.Node(problem.getStartState(),None,None,0)
    fringe = util.PriorityQueue()  #We have the data structure we need to push and pop elms
    fringe.push(n,heuristic(n.state,problem))   #f(n) = h(n) 
    generated = {n.state:[n,'F']} 
    while True:
        if fringe.isEmpty(): #No more paths to explore
            sys.stderr.write('No solution')
            sys.exit()
        n = fringe.pop()
        if problem.isGoalState(n.state): return n.path() #Goal state reached
        generated[n.state] = [n,'E']
        for state, action, cost in problem.getSuccessors(n.state): #Sucesors of the node
                ns = node.Node(state,n,action,cost)
                if ns.state not in generated:   #Add node to fringe if its not in fringe(to explore) and not in the expanded (explored) 
                    fringe.push(ns,heuristic(ns.state,problem))
                    generated[ns.state] = [ns,'F']
                elif generated[ns.state][0].cost > ns.cost: #Update fringe if we can reach same state with less cost
                    fringe.push(ns,heuristic(ns.state,problem))
                    generated[ns.state] = [ns,'F']
            
    util.raiseNotDefined()
    
def pathMax(father, son):
    if father > son: return father
    return son

def aStarSearch(problem, heuristic=nullHeuristic):
    n = node.Node(problem.getStartState(),None,None,0)
    fringe = util.PriorityQueue()  
    fringe.push(n,n.cost+heuristic(n.state,problem)) #f(n) = g(n) + h(n)      
    generated = {n.state:[n,'F']} 
    while True:
        if fringe.isEmpty(): #No more paths to explore
            sys.stderr.write('No solution')
            sys.exit()
        n = fringe.pop()
        if problem.isGoalState(n.state): return n.path() #Goal state reached
        generated[n.state] = [n,'E']
        for state, action, cost in problem.getSuccessors(n.state): #Sucesors of the node
                ns = node.Node(state,n,action,cost)
                if ns.state not in generated:   #Add node to fringe if its not in fringe(to explore) and not in the expanded (explored) 
                    f = pathMax(n.cost+heuristic(n.state,problem),ns.cost+heuristic(ns.state,problem))
                    fringe.push(ns,f)
                    generated[ns.state] = [ns,'F']
                elif generated[ns.state][0].cost > ns.cost: #Update fringe if we can reach same state with less cost
                    f = pathMax(n.cost+heuristic(n.state,problem),ns.cost+heuristic(ns.state,problem))
                    fringe.push(ns,f)
                    generated[ns.state] = [ns,'F']
            
    util.raiseNotDefined()

def bidirectionalSearch(problem):
    cont = 1
    ni = node.Node(problem.getStartState(),None,None,0)
    ng = node.Node(problem.goal,None,None,0)
    if ni.state == ng.state: return ni.path()
    fringeI = [ni]
    fringeG = [ng]    
    generatedI = {ni.state:[ni,'F']}
    generatedG = {ng.state:[ng,'F']}
    nsg = ng
    while True:
        if cont%2 != 0:
            if len(fringeI) == 0: 
                sys.stderr.write('No solution')
                sys.exit()
            ni = fringeI.pop(0) #Queue
            generatedI[ni.state] = [ni,'E']
            for state, action, cost in problem.getSuccessors(ni.state):
                nsi = node.Node(state,ni,action,cost)
                if nsi.state not in generatedI:
                    if nsi.state in generatedG.keys(): 
                        return nsi.path()+generatedG[nsi.state][0].invertedpath()
                        sys.exit(0)
                    fringeI.append(nsi)                                            
                    generatedI[nsi.state] = [nsi,'F']
        else:
            if len(fringeG) == 0: 
                sys.stderr.write('No solution')
                sys.exit()
            ng = fringeG.pop(0) #Queue
            generatedG[ng.state] = [ng,'E']
            for state, action, cost in problem.getSuccessors(ng.state):
                nsg = node.Node(state,ng,action,cost)
                if nsg.state not in generatedG:
                    if nsg.state in generatedI.keys(): 
                        return generatedI[nsg.state][0].path()+nsg.invertedpath()
                        sys.exit(0)    
                    fringeG.append(nsg)                                            
                    generatedG[nsg.state] = [nsg,'F']
        cont+=1
    util.raiseNotDefined() 


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
dls = depthLimitedSearch
bfsh = bestFirstSearch
bds = bidirectionalSearch

