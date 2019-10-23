import plotly.graph_objects as go

def getResults(lista,results):
    TotalCost = 0
    NodesExpanded = 0
    TotalTime = 0
    cont = 0
    row = []
    a = []
    with open(results) as fp:
        line = fp.readline()
        while(line):
            if line != '\n':
                row = line.split()
                if row[0]=='@':
                    a.append(TotalCost/cont)
                    a.append(NodesExpanded/cont)
                    a.append(TotalTime/cont)
                    TotalCost = 0
                    NodesExpanded = 0
                    TotalTime = 0
                    cont = 0
                    lista.append(a)
                    a = []
                else:
                    TotalCost+=int(row[0])
                    NodesExpanded+=int(row[1])
                    TotalTime+=float(row[2])
                    cont+=1
            line = fp.readline()
    return lista

if __name__ == "__main__":
    algorithms = getResults([],'resultsSmall.txt')
    print(algorithms)