# HETIONET

# Design Diagrams:

![image](/src/diagrams/mongo_diagram.png)

**Why MongoDB?**

I preprocessed the tsv in python and added all relevant information in a
document before inserting it to the database. This should be really fast retrieval
since we just need to find by id and all the data needed such as treatments,
palliates, genes and anatomy are all on the same document.

**Queries Used:**

For inserting into the database I just used collection.insert(document)
which is under the method generate_database() and for finding the item in the
database I used collection.find_one({‘_id’: disease_id}) which is under the method
get_disease().

![image](/src/diagrams/neo4j_diagram.png)

**Why Neo4j?**

I chose neo4j for question 2 because it it makes it easy and fast to search
for relationships between nodes whereas if I had used mongo for this task as well
I would have had to do much more pre-processing. Additionally, question 2 is
trying to find missing edges based on the already established relationships which
would also be another advantage for neo4j.

**Queries Used:**

For inserting nodes into the database I used:
```
'''
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///{filePath}' AS row
FIELDTERMINATO '\t'
CALL apoc.create.node([row.kind], {{id: row.id, name:
row.name}}) yield node
return 0;
'''.format(filePath=filePath)
```

For creating the relationships I used the following:
```
'''
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///{filePath}' AS row
FIELDTERMINATO '\t'
MATCH (source),(destination)
WHERE source.id=row.source AND destination.id=row.target
CALL apoc.create.node([row.kind], {{id: row.id, name:
row.name}}) yield node
return 0;
'''.format(filePath=filePath)
```

For getting the compounds to treat a disease given a name I used:

```
'''
MATCH (disease: Disease {{name: "{disease}"}})-[:DdG]->(:Gene)<-
[:CuG]-(compound0: Compound)
WHERE NOT (compound0)-[:CtD]->(disease)
RETURN compound0.name AS name
UNION
MATCH (disease: Disease {{name: "{disease}"}})-[:DuG]->(:Gene)<-
[:CdG]-(compound0: Compound)
WHERE NOT (compound1)-[:CtD]->(disease)
RETURN compound0.name AS name;
'''.format(disease=disease)
```

For all of these queries I was able to run them from python using py2neo

**Possible Optimizations:**

For Neo4j it was rather slow when creating the database. After some
research using periodic commit, editing configuration by adjusting max heap
usage as well as indexing in the beginning of db creation might help. Additionally,
since I’m working locally I saw that I could also use neo4j import and that might
perform faster, however that would require preprocessing and since I would need
to split tsv files and update headers.

For MongoDB optimization would be to insert the diseases in batches
instead of every loop insert a document since there could be the possibility of
running out of ram unlike when inserting into neo4j which I did in batches.
