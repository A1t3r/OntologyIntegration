from rdflib import Graph
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
import rdflib.graph

from queries import *


class SPARQLProxy:
    _rds_tag_mapping = {
        '-': 'product_tag',
        '=': 'functional_tag',
        '+': 'location_aspect',
        '%': 'type_tag'
    }

    def __init__(self, path: str):
        # Connect to fuseki triplestore.
        store = SPARQLUpdateStore(context_aware=False)
        # store.open(path)
        # Open a graph in the open store and set identifier to default graph ID.
        self.graph = Graph(store, identifier=rdflib.graph.DATASET_DEFAULT_GRAPH_ID)
        self.graph.open(path)
        # self.graph = store
        # self.graph = Graph(identifier=URIRef('http://localhost:3030/dataset.html?tab=query&ds=/lte')).parse(path)

    def _format_query_results_to_list(self, query_result) -> list[str]:
        res_combined = []
        for r in query_result:
            for label in r.labels:
                res_combined.append(f'{label}: {str(r[label])}')

        return res_combined

    def _format_query_results_to_dict(self, query_result, dbpedia_specific=False) -> dict:
        res_combined = {}
        for r in query_result:
            for label in r.labels:
                value = str(r[label])
                if dbpedia_specific:
                    if 'resource' in value:
                        res_combined[str(label)] = value
                else:
                    res_combined[str(label)] = value

        return res_combined

    def _format_query_results_to_dict_list(self, query_result) -> dict:
        res_combined = {}
        for r in query_result:
            for label in r.labels:
                value = str(r[label])
                try:
                    res_combined[str(label)].append(value)
                except KeyError:
                    res_combined[str(label)] = list()
                    res_combined[str(label)].append(value)

        return res_combined

    def get_test_sparq_res(self) -> list[str]:
        q = TEST_QUERY
        res = self.graph.query(q)
        return self._format_query_results_to_list(res)

    def get_subclasses(self, provided_class: str):
        q = SUBCLASS_QUERY
        res = self.graph.query(q)
        return self._format_query_results_to_list(res)

    # TODO: find a better way
    @staticmethod
    def _get_number_pos(tag: str) -> int:
        for i in range(len(tag) - 1, -1, -1):
            if not tag[i].isnumeric():
                return i + 1

    def _exec_dbpedia(self, description: str) -> dict:
        q = dbpedia_service_query_sample(description)
        res = self.graph.query(q)
        return self._format_query_results_to_dict(res, dbpedia_specific=True)

    def _exec_ind(self, tag: str, id: int, tag_type: str) -> dict:
        q = tag_individual_query_sample(tag, id, tag_type)
        res = self.graph.query(q)
        return self._format_query_results_to_dict(res)

    def _exec_inds(self, tag: str, tag_type: str, id: str) -> dict:
        q = tag_individuals_query_sample(tag, tag_type)
        res = self.graph.query(q)
        inds = self._format_query_results_to_dict_list(res)
        if not inds:
            return {'ind': None}
        for ind in inds['ind']:
            id_pos = self._get_number_pos(ind)
            if id == ind[id_pos:]:
                return {'ind': ind}
        return {'ind': None}

    def _exec_class(self, tag: str, tag_type: str, id: str, add_dbpedia: bool = False) -> dict:
        q = tag_class_query_sample(tag, tag_type)
        res = self.graph.query(q)
        res = self._format_query_results_to_dict(res)
        ind_info = self._exec_inds(tag, tag_type, id)
        res.update(ind_info)
        if res is not None and add_dbpedia:
            if res.get('description') is not None:
                dbpedia_info = self._exec_dbpedia(res['description'])
                res.update(dbpedia_info)
        # print("res ", res)
        return res

    def test_by_id(self, tag: str, id: int, tag_type: str) -> list[str]:
        q = ind_by_inner_id(tag, id, tag_type)
        res = self.graph.query(q)
        return self._format_query_results_to_list(res)

    def get_data_by_tag(self, tags: str, add_dbpedia: bool = False):
        tags = tags.split()
        for tag in tags:
            print(tag)
            tag_type = tag[0]
            tag = tag.replace('.', tag_type)[1:]
            tag_by_levels = tag.split(tag_type)
            tag_type = self._rds_tag_mapping[tag_type]
            for tag in tag_by_levels:
                id_pos = self._get_number_pos(tag)
                tag, id = tag[:id_pos], tag[id_pos:]
                # ind_res = self._exec_ind(tag, int(id), tag_type)
                class_res = self._exec_class(tag, tag_type, id, add_dbpedia=add_dbpedia)

                # ind_res_id = self.test_by_id(tag, int(id), tag_type)
                # print(f'IND BY ID {ind_res_id}')

                # print(f'Info about individual with tag {tag} and id {id}: {ind_res if ind_res else "No data"}')
                print(f'Info about class with tag {tag}: {class_res if class_res else "No data"}')
                print()
