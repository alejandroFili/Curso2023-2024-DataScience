#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[5]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# First let's read the RDF file

# In[22]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# In[16]:


# TO DO
from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

# with RDFlib
def subclases(x) -> None:
    a = g.triples((None, RDFS.subClassOf, x))
    if a is not None:
        for s, p, o in a:
          print(s)
          subclases(s)
subclases(ns.LivingThing)
    
# with SPARQL
q1 = prepareQuery('''
   SELECT ?Subject WHERE { 
      ?Subject rdfs:subClassOf* ns:LivingThing.
    } 
    ''',
    initNs={"rdfs": RDFS, "ns": ns}
)

# Visualize the SPARQL results
for r in g.query(q1):
  print(r.Subject)

# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[31]:


# TO DO
from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

# with RDFlib
def lista(x) -> None:
    a = g.triples((None, RDFS.type, x))
    if a is not None:
        for s, p, o in a:
            print(s)
    b = g.triples((None, RDFS.subClassOf, x))
    if b is not None:
        for s2, p2, o2 in b:
            lista(s2)
lista(ns.Person)
    
# with SPARQL
q2 = prepareQuery('''
   SELECT ?Subject WHERE { 
      ?Subject rdf:type ?person . 
      ?person rdfs:subClassOf* ns:Person .
    } 
    ''',
    initNs = {"rdfs": RDFS, "rdf": RDF, "ns": ns}
)

# Visualize the SPARQL results
for r in g.query(q2):
  print(r.Subject)


# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# In[36]:


# TO DO
from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

# with RDFlib
for s,p,o in g.triples((None, RDF.type, ns.Person or ns.Animal)):
  for s2,p2,o2 in g.triples((s, None, None)):
    print(s2,p2)

for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person or ns.Animal)):  
  for s2,p2,o2 in g.triples((None, RDF.type, s)):
    for s3,p3,o3 in g.triples((s2, None, None)):
      print(s2,p2)


# with SPARQL
q4 = prepareQuery('''
   SELECT ?Subject ?prop WHERE { 
      ?Subject rdf:type ns:Animal .
      ?Subject ?prop ?value .
    } 
    UNION
     { 
      ?Subject rdf:type ns:Person .
      ?Subject ?prop ?value .
    } 
    ''',
    initNs = {"rdf": RDF, "ns": ns}
)

q5 = prepareQuery('''
   SELECT ?Subject ?prop WHERE { 
      ?Subject rdf:type ?animal .
      ?animal rdfs:subClassOf* ns:Animal .
      ?Subject ?prop ?value .
    } 
    ''',
    initNs = {"rdfs": RDFS, "rdf": RDF, "ns": ns}
)

# Visualize the results
for r in g.query(q4):
  print(r.Subject)
for r in g.query(q5):
  print(r.Subject)


# **TASK 7.4:  List the name of the persons who know Rocky**

# In[32]:


# TO DO
from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

# with RDFlib
know_Rocky = []
for s, p, o in g.triples((None, FOAF.Knows, ns.Rocky)):
    print(s)
    know_Rocky += [s]

# with SPARQL
q6 = prepareQuery('''
    SELECT DISTINCT ?nombre
    WHERE{
            ?x FOAF:knows ns:RockySmith.
            ?x <http://www.w3.org/2001/vcard-rdf/3.0/Given> ?nombre
    }''', initNs = {"ns": ns, "FOAF":FOAF}
    )


# Visualize the results
for r in g.query(q6):
  print(r)


# **Task 7.5: List the entities who know at least two other entities in the graph**

# In[35]:


# TO DO
from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

# with RDFlib
from typing import Dict
dic:Dict[str, int]={}
resultado = []
for s,p,o in g.triples((None, FOAF.knows, None)):
  if s in dic:
    dic[s] +=1
  else:
    dic[s] = 0
for clave, cantidad in dic.items():
    if cantidad >= 2:
        lista.append(clave)
print(resultado)

# with SPARQL
q7 = prepareQuery('''
   SELECT ?entity ?knownEntities WHERE { 
        ?entity rdf:type ?class .
        ?entity ns:knows ?Entity1 .
        ?entity ns:knows ?Entity2 .
    FILTER(?Entity2 != ?Entity1)
    } 
    ''',
    initNs = {"rdfs": RDFS, "rdf": RDF, "ns": ns}
)

# Visualize the results
for r in g.query(q7):
    print(r)
