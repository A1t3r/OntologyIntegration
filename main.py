from SPARQ_proxy import SPARQLProxy

# sp = SPARQProxy("lte_v3.owl")
sp = SPARQLProxy('http://localhost:3030/lte/query')
# test queries
# res = sp.get_test_sparq_res()
# res = sp.get_subclasses('lte:UE')

# -A1.AB1.ABD1
# =H1.HA1.HAA1
# -D1-DA1-HSS400
# tag = '-A1.AB1.ABD1 =H1.HA1.HAA1 -D1-DA1-HSS400'
while 1:
    tag = input('Enter tag \n')
    if tag == 'exit':
        break
    sp.get_data_by_tag(tag, add_dbpedia=True)
