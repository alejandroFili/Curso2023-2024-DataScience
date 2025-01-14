# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yPniC8cCIRK0ofpUQK_h0bcNOa4CroCF

**Task 07: Querying RDF(s)**
"""

# !pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

ns = Namespace("http://somewhere#")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# TO DO
from rdflib.plugins.sparql import prepareQuery

livingThing_query = prepareQuery('''
SELECT ?subClase
WHERE {
    ?subClase rdfs:subClassOf ns:LivingThing
}                      
''',
initNs = { "rdfs": RDFS, "ns": ns}
)
# Visualize the results
print("7.1")
for r in g.query(livingThing_query):
  print(r.subClase)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
# from rdflib.plugins.sparql import prepareQuery

person_query = prepareQuery('''
SELECT ?person
WHERE {
    ?person rdf:type ns:Person
}                      
''',
initNs = { "rdf": RDF, "rdfs": RDFS, "ns": ns}
)
# Visualize the results
print("7.2")
for r in g.query(person_query):
  print(r.person)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

# TO DO
# from rdflib.plugins.sparql import prepareQuery

query_3 = prepareQuery('''
SELECT ?subject ?predicate ?object
WHERE {
     ?subject ?predicate ?object .
     ?subject rdf:type ?type .
FILTER (
     ?type = ns:Animal || ?type = ns:Person
)
}
''',
initNs = { "rdf": RDF, "rdfs": RDFS, "ns": ns}
)

# Visualize the results
print("7.3")
for r in g.query(query_3):
  print(r.subject, r.predicate, r.object)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

# TO DO
# from rdflib.plugins.sparql import prepareQuery
from rdflib import FOAF
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0")

query_4 = prepareQuery('''
SELECT ?Rocky_URI  ?amigo_URI ?amigo_name
WHERE {
     ?Rocky_URI <http://www.w3.org/2001/vcard-rdf/3.0/Given>  ?given_name . 
     ?amigo_URI foaf:knows ?Rocky_URI .
     ?amigo_URI <http://www.w3.org/2001/vcard-rdf/3.0/Given>  ?amigo_name . 
                                   

     FILTER(?given_name = "Rocky")
}
''',
initNs = { "foaf": FOAF , "ns" : ns, "vcard": VCARD}
)

# Visualize the results
print("7.4")
for r in g.query(query_4):
     print(r.amigo_name)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

# TO DO

# from rdflib.plugins.sparql import prepareQuery
# from rdflib import FOAF
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0")

query_5 = prepareQuery('''
SELECT ?entity ?relatedEntity
WHERE {
      ?entity foaf:knows ?relatedEntity .

}
GROUP BY ?entity 
HAVING (COUNT(DISTINCT ?relatedEntity) >= 2)
    
''',
initNs = { "foaf": FOAF , "ns" : ns, "vcard": VCARD}
)

# Visualize the results
print("7.5")
for r in g.query(query_5):
     print(r.entity)