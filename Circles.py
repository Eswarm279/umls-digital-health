!pip install mysql.connector.python
import mysql.connector
import networkx as nw

# By using below the function to check the circles in between CUI1 and CUI2 
def sol_circles(cui, graph, vis, result):
    result.append(cui)# adding the neighbour node in the result
    vis.add(cui)# Attaching the CUI node to the visited
    #To verifying neighbour node in graph
    for nr in graph[cui]: 
        if nr in result:
                return True
        if nr not in vis:
            cir = sol_circles(nr, graph, vis, result)
            if cir:
                return True
    result.pop()
    return False

# Connecting to the database of umls by using host, port, user, password and database credentials
hostco = mysql.connector.connect(host='172.16.34.1', port='3307', user='umls', password='umls', database='umls2021')


# By using below query to get the relationships of CUI from the UMLS database 2021
Que = 'select CUI1, CUI2, RELA from MRREL limit 4100;'

# Creating a cursor below to run the queries in UMLS database
cur = hostco.cursor()

cur.execute(Que)#Executing the query

# By using DiGraph to add the edges and  the graph of CUIs and their relationships
Gra = nw.DiGraph()

for cui1, cui2, rela in cur:
    Gra.add_edge(cui1, cui2)

# By using below the function to check the circles in between CUI1 and CUI2 
for cui in Gra:
    vis = set()
    result = []
    sol=sol_circles(cui, Gra, vis, result)
    #cycles = nw.algorithms.cycles.cycle_basis(Gra)
    if sol:
        a=result[0]
        result.append(a) # add the first term to the end of the result 
    l=len(result)
    if l>3:
        print('Circles-Nodes:',result)

# Close the cursor and connection to the database
cur.close()
hostco.close()
