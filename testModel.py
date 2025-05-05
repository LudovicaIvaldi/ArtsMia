from model.model import Model

myModel=Model()
myModel.buildGraph()
print("Il numero di nodi è:", myModel.getNumNodi(), "il numero di archi è:", myModel.getNumEdges())

myModel.getInfoConnessa(1234)