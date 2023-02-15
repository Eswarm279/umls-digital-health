!pip install mysql.connector.python
import mysql.connector
import pprint

# Connecting to the database of umls by using host, port, user, password and database credentials
hostco = mysql.connector.connect(host='172.16.34.1', port='3307', user='umls', password='umls', database='umls2021')
# Creating a cursor below to run the queries in UMLS database
cur = hostco.cursor()
def run_query(cur, query):
    cur.execute(query)
    query_result = cur.fetchall()
    col_names = [ col[0] for col in cur.description]
    pprint.pprint(col_names)
    pprint.pprint(query_result)
# By using below query to get the circles of CUI from the UMLS database 2021
run_query(cur, """
with recursive cui_node (n, CUI1, CUI2, path_info) as (select 0 as n, CUI1 as CUI1, CUI2 as CUI2, cast(concat('C1254372,', CUI2) as char(2000)) as path_info from umls2020.MRREL where CUI1='C1254372' AND REL='PAR' AND CUI1<>CUI2 union all
   select n+1, p.CUI1, p.CUI2, concat(path_info, ',', p.CUI2) as path_info from umls2020.MRREL p inner join cui_node on p.CUI1=cui_node.CUI2
   where p.REL='PAR' AND p.CUI1<>p.CUI2 and n < 3)
   select path_info 
   FROM cui_node a 
   where a.path_info 
   like '%C1254372%'
""")
hostco.close()