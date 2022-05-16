import configparser
from bs4 import BeautifulSoup
import pymysql
import html2md
import requests

term_dic = {}

def get_data_in_db(sql):
    conf = configparser.ConfigParser()
    conf.read("config.ini")
    database = pymysql.connect(host=conf.get(section="sql", option="host"),
                               user=conf.get(section="sql", option="user"),
                               password=conf.get(section="sql", option="password"),
                               port=int(conf.get(section="sql", option="port")),
                               db=conf.get(section="sql", option="db"), charset='utf8')
    cursor = database.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    database.close()
    return data


def get_tag_info():
    sql_terms = "select `term_id`, `name` from forblog.wp_terms"
    sql_term_to_post = "select `object_id`, `term_taxonomy_id` from forblog.wp_term_relationships"
    term_data_all = get_data_in_db(sql_terms)
    term_to_post_data_all = get_data_in_db(sql_term_to_post)
    for term in term_data_all:
        term_dic[term[0]] = term[1]

    term_to_post_dic = {}

    for term_to_post in term_to_post_data_all:
        term_to_post_dic.setdefault(term_to_post[0], []).append(term_to_post[1])

    return term_dic, term_to_post_dic
