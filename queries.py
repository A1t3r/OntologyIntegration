PREFIX = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX lte:<http://www.semanticweb.org/anton/ontologies/2023/0/lte#>
        
        """

DBPEDIA_PREFIX = '''
        PREFIX dbo: <http://dbpedia.org/ontology/>
        '''

TEST_QUERY = PREFIX + """
        SELECT distinct ?type 
        	WHERE {  
        		{
        		lte:mme-enodeb-link1 lte:connectionProvidedWith ?obj .
        		?obj rdf:type ?type
        		}
        	FILTER ( ?type!=owl:NamedIndividual) 
        	}
        """

SUBCLASS_QUERY = PREFIX + '''
            SELECT ?type
            WHERE {{ ?type rdfs:subClassOf lte:LTEComponents}}
'''


def tag_individual_query_sample(tag: str, id: int, tag_type: str) -> str:
    tag_individual_query = PREFIX + f'' \
                                    f' SELECT distinct ?type ?description ?ind \n' \
                                    f' WHERE {{ \n' \
                                    f'        {{ \n' \
                                    f'          ?type  lte:{tag_type} "{tag}" . \n' \
                                    f'          ?type lte:rds_description ?description  . \n' \
                                    f'          ?ind rdf:type ?type . \n' \
                                    f'          ?ind lte:rds_id {id} . \n' \
                                    f'        }} \n' \
                                    f'      }} \n'
    return tag_individual_query


def tag_individuals_query_sample(tag: str, tag_type: str) -> str:
    tag_individual_query = PREFIX + f'' \
                                    f' SELECT distinct ?ind \n' \
                                    f' WHERE {{ \n' \
                                    f'        {{ \n' \
                                    f'          ?type  lte:{tag_type} "{tag}" . \n' \
                                    f'          ?ind rdf:type ?type . \n' \
                                    f'        }} \n' \
                                    f'      }} \n'
    return tag_individual_query


def dbpedia_service_query_sample(description: str) -> str:
    dbpedia_service_query = PREFIX + f'' \
                                     f'SELECT  ?wiki_obj \n' \
                                     f'WHERE {{ \n' \
                                     f'    SERVICE <http://dbpedia.org/sparql> {{ \n' \
                                     f'     ?wiki_obj rdfs:label "{description}"@en . \n' \
                                     f'      }} \n' \
                                     f'}} \n'
    return dbpedia_service_query


def tag_class_query_sample(tag: str, tag_type: str) -> str:
    tag_class_query = PREFIX + f'' \
                               f' SELECT distinct * \n' \
                               f' WHERE {{ \n' \
                               f'         {{ \n' \
                               f'           ?type  lte:{tag_type} "{tag}" . \n' \
                               f'           ?type lte:rds_description ?description  . \n' \
                               f'         }} \n' \
                               f'       }} \n'
    return tag_class_query


def ind_by_inner_id(tag: str, id: int, tag_type: str) -> str:
    tag = 'ABD'
    tag_individual_query = PREFIX + f'' \
                                    f' SELECT distinct ?type ?description ?ind \n' \
                                    f' WHERE {{ \n' \
                                    f'        {{ \n' \
                                    f'          ?type  lte:{tag_type} "{tag}" . \n' \
                                    f'          ?type lte:rds_description ?description  . \n' \
                                    f'          ?ind rdf:type ?type . \n' \
                                    f'        }} \n' \
                                    f' FILTER (?ind=lte:0002) ' \
                                    f'      }} \n'
    return tag_individual_query
