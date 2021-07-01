from py2neo import Graph


class GraphDatabase:
    def __init__(self, uri):
        self.graph = Graph(uri)

    def clear_database(self):
        self.graph.delete_all()

    def __generate_nodes(self, nodes_tsv_path):
        load_nodes_tsv_command = '''\
        USING PERIODIC COMMIT
        LOAD CSV WITH HEADERS FROM 'file:///{filePath}' AS row 
        FIELDTERMINATOR '\t'
        CALL apoc.create.node([row.kind], {{id: row.id, name: row.name}}) yield node
        return 0;\
        '''.format(filePath=nodes_tsv_path)
        self.graph.run(load_nodes_tsv_command)

    def __generate_edges(self, edges_tsv_path):
        load_edges_tsv_command = '''\
        USING PERIODIC COMMIT
        LOAD CSV WITH HEADERS FROM 'file:///{filePath}' AS row 
        FIELDTERMINATOR '\t'
        MATCH (source),(destination)
        WHERE source.id=row.source AND destination.id=row.target
        CALL apoc.create.relationship(source, row.metaedge, {{}}, destination) yield rel
        return 0;\
        '''.format(filePath=edges_tsv_path)
        self.graph.run(load_edges_tsv_command)

    def generate_database(self, nodes_tsv_path, edges_tsv_path):
        self.__generate_nodes(nodes_tsv_path)
        self.__generate_edges(edges_tsv_path)

    def get_treatments(self, disease):
        find_treatment_command = '''
        MATCH (disease: Disease {{name: "{disease}"}})-[:DdG]->(:Gene)<-[:CuG]-(compound0: Compound)
        WHERE NOT (compound0)-[:CtD]->(disease)
        RETURN compound0.name AS name
        UNION
        MATCH (disease: Disease {{name: "{disease}"}})-[:DuG]->(:Gene)<-[:CdG]-(compound1: Compound)
        WHERE NOT (compound1)-[:CtD]->(disease)
        RETURN compound1.name AS name
        '''.format(disease=disease)
        treatments = self.graph.run(find_treatment_command).data()
        return treatments

    def is_database_empty(self):
        result = self.graph.run('MATCH (n) RETURN count(n);')
        if result == 0:
            return True
        else:
            return False
