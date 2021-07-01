from document import DocumentDatabase
from graph import GraphDatabase
from pprint import pprint

neo4j_url = 'http://neo4j:thePassword@localhost:7474/db/data'

document = DocumentDatabase()

print("you can leave the nodes and edges empty if the database has been generated already")
nodes_tsv_path = input("please enter path of nodes tsv file: ")
edges_tsv_path = input("please enter path of edges tsv file: ")


if(document.is_database_empty()):
    document.generate_database(nodes_tsv_path,edges_tsv_path)
    print("mongoDB database generated!")
else:
    print("mongoDB database found!")


neo4j_url = input('enter uri for neo4j: ')

graph = GraphDatabase(neo4j_url)

if(graph.is_database_empty()):
    graph.generate_database(nodes_tsv_path, edges_tsv_path)
    print('neo4j databade generated!')
else:
    print('neo4j database found!')

while True:
    option = input('================================================================\nenter: \n [1] to search for a disease id and retrieve its data. \n [2] to search for a disease name and retrieve treatments \n press any other button to quit: \n')
    if option == "1":
        id = input("please enter a disease id: ")
        result = document.get_disease(id)
        print('These are the results: ')
        pprint(result)

    elif option == "2":
        name = input("please enter a disease name: ")
        result = graph.get_treatments(name)
        print('These are the results: ')
        pprint(result)
    else:
        break

print("exiting")