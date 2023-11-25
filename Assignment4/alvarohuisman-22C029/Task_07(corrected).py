# %% [markdown]
# **Task 07: Querying RDF(s)**

# %%
!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

# %% [markdown]
# First let's read the RDF file

# %%
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")
for s, p, o in g:
  print(s,p,o)

# %% [markdown]
# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# %%
# TO DO
from rdflib.plugins.sparql import prepareQuery
import rdflib
print('SPARQL')
q1 = prepareQuery('''
  SELECT ?Subject WHERE { 
    ?Subject rdfs:subClassOf* ?LivingThing. 
  }
  ''',
  initNs = { "rdfs": RDFS}
)

living = rdflib.URIRef("http://somewhere#LivingThing")
# Visualize the results

for r in g.query(q1, initBindings={'LivingThing':living}):
  print(r.Subject)


print("RDFLIB")
def extract_subclasses(g,class_name):
  subclasses = set()
  for s,p,o in g.triples((None,RDF.type,RDFS.Class)):
    if (s,RDFS.subClassOf,class_name) in g:
      subclasses.add(s)
      subclasses.update(extract_subclasses(g,s))
  return subclasses
subclasses_lt = extract_subclasses(g,ns.LivingThing)
for subclass in subclasses_lt:
  print(subclass)


# %% [markdown]
# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# %%
# TO DO
print("SPARQL")
ns = Namespace("http://somewhere#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
q2 = prepareQuery('''
  SELECT DISTINCT ?Subject 
  WHERE { 
      {
        ?Subject rdf:type ns:Person. 
      } UNION { 
        ?x rdfs:subClassOf* ns:Person.
        ?Subject rdf:type ?x
      }
    }
    ''',
    initNs={"rdf": rdf, "rdfs": rdfs, "ns": ns}
)
# Visualize the results

for r in g.query(q2):
  print(r.Subject)

print("RDFLIB")
for s,p,o in g.triples((None, RDF.type, ns.Person)):
  print(s)
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s1,p1,o1 in g.triples((None, RDF.type, s)):
    print(s1)

# %% [markdown]
# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# %%
# TO DO
print("SPARQL")
q3 = prepareQuery('''
    SELECT distinct ?Subject ?properties ?x
    WHERE {
        {
          ?Subject a ns:Person.
        }
        UNION
        {
          ?individual a ns:Animal.
        }
        ?Subject ?properties ?x
    }
    ''',
    initNs = {"rdf": rdf, "rdfs": rdfs, "ns": ns}
)


# Visualize the results
for r in g.query(q3):
  print(r.Subject, r.properties, r.x)

print("RDFLIB")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
  for s1, p1, o1 in g.triples((s, None, None)) :
    print (s1, p1, o1)
for s, p, o in g.triples((None, RDF.type, ns.Animal)):
  for s1, p1, o1 in g.triples((s, None, None)) :
    print (s1, p1, o1)

# %% [markdown]
# **TASK 7.4:  List the name of the persons who know Rocky**

# %%
# TO DO
from rdflib import FOAF, RDF, RDFS, Namespace
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
print("SPARQL")
q4 = prepareQuery('''
  SELECT ?Subject ?Name WHERE {
    ?Subject foaf:knows ns:RockySmith.
    ?Subject rdf:type ns:Person.
    ?Subject <http://www.w3.org/2001/vcard-rdf/3.0/FN> ?Name.
  }
''',
initNs={"foaf": FOAF, "rdf": RDF, "rdfs": RDFS, "vcard": VCARD, "ns":ns})
# Visualize the results
for r in g.query(q4):
    print(r.Name)

print("RDFLIB")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
  for s1, p1, o1 in g.triples((s, FOAF.knows, ns.RockySmith)) :
     for s2, p2, o2 in g.triples((s1, VCARD.FN, None)) :
        print(o2)

# %% [markdown]
# **Task 7.5: List the entities who know at least two other entities in the graph**

# %%
# TO DO
print("SPARQL")
q5 = prepareQuery('''
  SELECT ?Subject (COUNT(?known) AS ?count) WHERE {
    ?Subject foaf:knows ?known.
  }
  GROUP BY ?Subject
  HAVING (COUNT(?known) >= 2)
''',
initNs={"foaf": FOAF})

# Visualize the results
for r in g.query(q5):
    print(r.Subject)

print("RDFLIB")
count = {}
for s, p, o in g.triples((None, FOAF.knows, None)):
  count[s] = count.get(s,0)+1
entities = []
for key, value in count.items():
  if value >= 2:
    entities.append(key)
print(entities)


