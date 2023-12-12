import pandas as pd
from ipywidgets import widgets
import random
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

def reset_cbox(button, cbox):
    cbox.value = ''

def get_barrio_names(graph, dict_namespaces):
    info = {
        "barrio_names" : [],
        "wiki_ids" : [],
        "barrio_ids" : []
    }
    q = prepareQuery(
    '''
    SELECT ?Neighborhood_names ?Neighborhood_id ?wiki_id
    WHERE {
        ?Neighborhood_id rdf:type dog-loc:Neighborhood .
        ?Neighborhood_id rdfs:label ?Neighborhood_names .
        ?Neighborhood_id owl:sameAs ?wiki_id .
    }
    ''',
    initNs=dict_namespaces
    )

    results = list(graph.query(q))
    
    if not results:
        print("No results found.")
    else:
        for r in results:
            # print(r.Neighborhood_names, r.wiki_id)
            info["barrio_names"].append(r.Neighborhood_names)
            info["wiki_ids"].append(r.wiki_id)
            info["barrio_ids"].append(r.Neighborhood_id)
    return info
    # print(user_choice.Neighborhood_names, user_choice.wiki_id)
