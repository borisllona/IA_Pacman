import plotly.graph_objects as go
from plotly.subplots import make_subplots

iterations = 5
modes = ['UCS','BFSH (manhattan)','BFSH (euclidian)','A* (manhattan)','A* (euclidian)']
files = ['resultsSmall.txt','resultsMedium.txt','resultsBig.txt']

def getResults(col):
    lista, alg = [],[]
    dictionary = {}
    algorithmsSmall = {}
    algorithmsMedium = {}
    algorithmsBig = {}
    algorithms = [algorithmsSmall,algorithmsMedium,algorithmsBig]

    for i in files:
        count,num,total = 0,0,0
        with open(i,'r') as fp:
            line = fp.readline()
            while(line):
                lline = line.split()
                if(lline and lline[0]!='@'):
                    if count == iterations:
                        count = 0
                    if len(alg)<iterations:
                        alg.append(float(lline[col]))
                        count+=1
                        total+=1
                    else:    
                        num = float(alg.pop(count))
                        num+=float(lline[col])
                        alg.insert(count,num)
                        count+=1
                        total+=1   
                line = fp.readline() 
        dictionary = algorithms.pop(0)
        total = total/iterations
        for j in modes:
            if col == 2: dictionary[j] = alg.pop(0)/total
            else: dictionary[j] = round(alg.pop(0)/total,2)

    return [algorithmsSmall,algorithmsMedium,algorithmsBig]

def showResults(size,name):

    yS = list(size[0].values())
    yM = list(size[1].values())
    yB = list(size[2].values())
    fig = make_subplots(rows=2, cols=2)

    fig.add_trace(go.Scatter(x=modes, y=yS,mode='lines+markers',name='Small Layout'),row=1, col=1)
    fig.add_trace(go.Scatter(x=modes, y=yM,mode='lines+markers',name='Medium Layout'),row=1, col=2)
    fig.add_trace(go.Scatter(x=modes, y=yB,mode='lines+markers',name='Big Layout'),row=2, col=1)

    fig.update_layout(title=name)

    fig.show()

if __name__ == "__main__":
    
    costPath = getResults(0)
    nodesExpanded = getResults(1)
    totalTime = getResults(2)

    showResults(costPath,'Path Cost')
    showResults(nodesExpanded,'Nodes Expanded')
    showResults(totalTime,'Execution Time')