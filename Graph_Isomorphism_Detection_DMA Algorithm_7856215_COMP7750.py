import numpy as np
import pandas as pd
import itertools

def degreeDivision(graphA, graphB):
    cumSumA = np.sum(
        graphA, axis=0)
    cumSumB = np.sum(
        graphB, axis=0)
    matchResult = np.equal(np.sort(cumSumA), np.sort(cumSumB))
    return np.all(matchResult)


def checkEquality(graphA, graphB):
    matchResult = np.equal(graphA, graphB)
    return np.all(matchResult)


#this function assumes the last column has the cummulative sum
def getExpandedSquareList(graph):
    # print(graph)
    sumA = graph[:, len(graph)]
    unique, counts = np.unique(sumA, return_counts=True)
    freqCountDict = dict(zip(unique, counts))
    keysFreqCount = -np.sort(-np.array([int(i) for i in freqCountDict.keys()]))
    # print(freqCountDict)
    exSqDeg = {}
    for i in range(0, len(graph[0]) - 1):
        exSqDeg[i] = 0

    exSqDegDict = {}
    startIndex = 0
    endIndex = 0
    # print(graph)
    # print(keysFreqCount)
    for uniqueDegree in keysFreqCount:
        count = freqCountDict[uniqueDegree]
        exSqDegDict[uniqueDegree] = 0
        endIndex = startIndex + count
        for node in range(startIndex, endIndex):
            for edge in range(startIndex, endIndex):
                if (graph[node, edge] == 1):
                    # print(node)
                    # print(edge)
                    # print("found")
                    exSqDeg[node] += sumA[node]**2
                    exSqDegDict[uniqueDegree] += sumA[node]**2
                    # print(exSqDeg[node])
        startIndex = endIndex
    # print(exSqDeg)
    return exSqDegDict


def checkExpandedSquareList(graphA, graphB):
    exSqDegDictA = getExpandedSquareList(graphA)
    # print(exSqDegDictA)
    exSqDegDictB = getExpandedSquareList(graphB)
    # print(exSqDegDictB)
    flag = compareDict(exSqDegDictA, exSqDegDictB)
    # print(flag)
    return exSqDegDictA, exSqDegDictB, flag


def sortGraph(graphA, graphB):
    nodeNames = []
    nVertex = len(graphA[0])
    for i in range(0, int(nVertex)):
        nodeNames.append("node" + str(i))
    # sort graphA
    df = pd.DataFrame(graphA, columns=nodeNames, index=nodeNames)
    df['sum'] = np.sum(
        graphA, axis=0)
    # print(df)
    df = df.sort_values(by=['sum'], ascending=False)
    rowNames = df.index.tolist()
    rowNames.append("sum")
    df = df.reindex(columns=rowNames)
    # print(df)
    graphA = df.as_matrix()

    # sort graphB
    df = pd.DataFrame(graphB, columns=nodeNames, index=nodeNames)
    df['sum'] = np.sum(
        graphB, axis=0)
    # print(df)
    df = df.sort_values(by=['sum'], ascending=False)
    # print(df)
    rowNames = df.index.tolist()
    rowNames.append("sum")
    df = df.reindex(columns=rowNames)
    # print(df)
    graphB = df.as_matrix()
    return graphA, graphB


def compareDict(dictA, dictB):
    flag = True
    for key in dictA.keys():
        if (dictA[key] != dictB[key]):
            flag = False
            break
    return flag


def getCorrelationDegreeMat(graph, nNodes):
    sumA = graph[:, len(graph)]
    unique, counts = np.unique(sumA, return_counts=True)
    freqCountDict = dict(zip(unique, counts))
    keysFreqCount = -np.sort(-np.array([int(i) for i in freqCountDict.keys()]))
    # print(keysFreqCount)# this is sorted
    # print(freqCountDict)# this contains count
    nSubGraphs = len(keysFreqCount)  # get number of sub blocks
    subBlockGraph = np.zeros(
        shape=(nSubGraphs, nSubGraphs), dtype=np.int)  # subblock matrix
    startIndex = 0
    endIndex = 0
    tempCorrelationDegreeMat = np.zeros((nNodes, nSubGraphs), dtype=int)
    correlationDegreeMat = np.zeros((nSubGraphs, nSubGraphs), dtype=int)
    for nSubGraph in range(0, nSubGraphs):
        subGraph = keysFreqCount[nSubGraph]
        # print(subGraph)
        endIndex = startIndex + freqCountDict[subGraph]
        # print(startIndex)
        # print(endIndex)
        tempCorrelationDegreeMat[:, nSubGraph] = np.sum(
            graph[:, startIndex:endIndex], axis=1)
        startIndex = endIndex
    startIndex = 0
    # print(tempCorrelationDegreeMat)
    # print(tempCorrelationDegreeMat.shape)
    for nSubGraph in range(0, nSubGraphs):
        subGraph = keysFreqCount[nSubGraph]
        # print(subGraph)
        endIndex = startIndex + freqCountDict[subGraph]
        # print(startIndex)
        # print(endIndex)
        # print(np.sum(tempCorrelationDegreeMat[startIndex:endIndex, :], axis=0))
        correlationDegreeMat[nSubGraph, :] = np.sum(
            tempCorrelationDegreeMat[startIndex:endIndex, :], axis=0)
        startIndex = endIndex
    return correlationDegreeMat


def graphInput(fileName):
    inputFile = open(fileName)
    #get number of graphs`
    nGraphs = int(inputFile.readline().strip())
    #get number of nodes in the first graph
    nNodesA = int(inputFile.readline().strip())
    nEdges = int(inputFile.readline().strip())
    graphA = np.zeros(shape=(nNodesA, nNodesA), dtype=np.int)
    for i in range(0, nEdges):
        line = inputFile.readline().strip().split()
        graphA[int(line[0]) - 1, int(line[1]) - 1] = 1
    #get number of nodes in the first graph
    nNodesB = int(inputFile.readline().strip())
    nEdges = int(inputFile.readline().strip())
    graphB = np.zeros(shape=(nNodesB, nNodesB), dtype=np.int)
    for i in range(0, nEdges):
        line = inputFile.readline().strip().split()
        graphB[int(line[0]) - 1, int(line[1]) - 1] = 1
    return graphA, nNodesA, graphB, nNodesB


def getNodeNames(nNodes):
    nodeNames = []
    for i in range(0, nNodes):
        nodeNames.append("node" + str(i))
    return nodeNames


def main():
    # take input
    graphA, nNodesA, graphB, nNodesB = graphInput('input7.txt')
    print("The input graphs are given below as adjacency matrices:\n")
    print("Graph A is:\n" )
    print(graphA)
    print("\nGraph B is:\n" )
    print(graphB)
    #algo 1: check for degree division
    checkDegDivFlag = degreeDivision(graphA, graphB)
    if checkDegDivFlag:
        graphA, graphB = sortGraph(graphA,
                                   graphB)  # sum is added in last clumn
        exSqDegDictA, exSqDegDictB, expandedSquareFlag = checkExpandedSquareList(
            graphA, graphB)
        correlationDegreeMatA = getCorrelationDegreeMat(graphA, nNodesA)
        correlationDegreeMatB = getCorrelationDegreeMat(graphB, nNodesB)
        equality = checkEquality(correlationDegreeMatA, correlationDegreeMatB)
        if equality:
            print("The graphs are Isomorphic")
        else:
            #print("start 5")
            # create node names in a list
            nodeNames = getNodeNames(nNodesB)
            dfB = pd.DataFrame(graphB[:, 0:len(graphB[0])-1], columns=nodeNames, index=nodeNames)
            dfBSum = np.sum(dfB.as_matrix(), axis=0)
            # print(dfBSum)
            unique, counts = np.unique(dfBSum, return_counts=True)
            freqCountDict = dict(zip(unique, counts))
            keysFreqCount = -np.sort(
                -np.array([int(i) for i in freqCountDict.keys()]))
            # print(freqCountDict)
            # print(keysFreqCount)
            startIndex = 0
            # print(dfB)
            flag = False
            # we assume, the last column of graphA is the cummulative sum
            graphA = np.delete(graphA, len(graphA[0]) - 1, 1)
            for uniqueDegree in keysFreqCount:
                endIndex = startIndex + freqCountDict[uniqueDegree]
                # print(startIndex)
                # print(endIndex)
                changingNodeNames = list(
                    [nodeNames[i] for i in range(startIndex, endIndex)])
                # print(changingNodeNames)
                # print(fixedNodeNames)
                permutedList = list(itertools.permutations(changingNodeNames))

                for newNodeNames in permutedList:
                    permutedNames = nodeNames[0:startIndex] + list(
                        newNodeNames) + nodeNames[endIndex:]
                    newGraphB = dfB.reindex(
                        index=permutedNames, columns=permutedNames)
                    flag = checkEquality(graphA, newGraphB.as_matrix())
                    if flag == True:
                        break
                startIndex = endIndex
            if flag == True:
                print("The graphs are Isomorphic")
            else:
                print("The graphs are not Isomorphic")
    else:
        print("The graphs are not Isomorphic")
        return


if __name__ == '__main__':
    main()
