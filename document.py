from pymongo import MongoClient
import csv
import networkx as nx


class DocumentDatabase:
    def __init__(self):
        self.client = MongoClient()

    def clear_database(self):
        self.client['HETIONET']['Diseases'].drop()

    def __generate_nodes(self, file_path_nodes):
        self.graph = nx.Graph()
        self.diseaseIds = []
        file = open(file_path_nodes)
        read_file = csv.reader(file, delimiter="\t")
        first_line = True
        for row in read_file:
            if first_line:
                first_line = False
                continue
            else:
                if row[0].split('::')[0] == 'Disease' and row[0] not in self.diseaseIds:
                    self.diseaseIds.append(row[0])
                self.graph.add_node(row[0], value=row[1])

        file.close()

    def __generate_edges(self, file_path_edges):
        file = open(file_path_edges)
        read_file = csv.reader(file, delimiter="\t")
        first_line = True
        for row in read_file:
            if first_line:
                first_line = False
                continue
            else:
                self.graph.add_edge(row[0], row[2], value=row[1])

    def generate_database(self, file_path_nodes, file_path_edges):
        db = self.client['HETIONET']
        collection = db['Diseases']
        self.__generate_nodes(file_path_nodes)
        self.__generate_edges(file_path_edges)
        print('creating database....')
        for disease in self.diseaseIds:
            document = {
                '_id': None,
                'name': None,
                'treatments': [],
                'palliates': [],
                'genes': [],
                'anatomy': []
            }
            for a, b in list(self.graph.edges(disease)):
                document['name'] = self.graph.nodes[disease]['value']
                document['_id'] = disease
                if self.graph.edges[a,b]['value'] == 'CtD':
                    document['treatments'].append(self.graph.nodes[b]['value'])
                elif self.graph.edges[a,b]['value'] == 'DdG' or self.graph.edges[a,b]['value'] == 'DuG' or self.graph.edges[a,b]['value'] == 'DaG':
                    document['genes'].append(self.graph.nodes[b]['value'])
                elif self.graph.edges[a,b]['value'] == 'CpD':
                    document['treatments'].append(self.graph.nodes[b]['value'])
                elif self.graph.edges[a,b]['value'] == 'DlA':
                    document['anatomy'].append(self.graph.nodes[b]['value'])
            if(document['_id'] != None):
                collection.insert(document)

    def is_database_empty(self):
        db = self.client['HETIONET']
        collection = db['Diseases']
        if collection.count() == 0:
            return True
        else:
            return False

    def get_disease(self, disease_id):
        db = self.client['HETIONET']
        collection = db['Diseases']
        result = collection.find_one({'_id': disease_id})
        return result

