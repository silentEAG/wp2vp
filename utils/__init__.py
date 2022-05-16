import configparser
from bs4 import BeautifulSoup
import pymysql
import html2md
import requests


img_ls = ['https://tva4.sinaimg.cn/large/0072Vf1pgy1foxkiak921j31kw0w0nnl.jpg',
          'https://tva4.sinaimg.cn/large/87c01ec7gy1frqe3zuxm4j21hc0u04qp.jpg',
          'https://tva3.sinaimg.cn/large/0072Vf1pgy1foxlnx4mk0j31hc0u07k9.jpg',
          'https://tva3.sinaimg.cn/large/0072Vf1pgy1foxlhey5i9j31kw0w0khl.jpg',
          'https://tva1.sinaimg.cn/large/0072Vf1pgy1foxkfbb3c7j31kw0w04ou.jpg',
          'https://tva1.sinaimg.cn/large/87c01ec7gy1frkjbhza1tj21hc0u0npd.jpg',
          'https://tva1.sinaimg.cn/large/0072Vf1pgy1foxkizc9w8j31kw0w0e45.jpg',
          'https://tva2.sinaimg.cn/large/0072Vf1pgy1foxlhcoxbbj31kw0w0tz3.jpg',
          'https://tva3.sinaimg.cn/large/0072Vf1pgy1foxk3mu0ztj31hc0u07m5.jpg',
          'https://tva2.sinaimg.cn/large/0072Vf1pgy1foxk6qy63sj31kw0w0twh.jpg',
          'https://tva1.sinaimg.cn/large/0072Vf1pgy1foxkfylhhxj31hc0u04dv.jpg',
          'https://tva1.sinaimg.cn/large/0072Vf1pgy1foxkfg4cj2j31hc0u01a9.jpg',
          'https://tva1.sinaimg.cn/large/0072Vf1pgy1foxk7b1md7j31hc0u0qlb.jpg',
          'https://tva2.sinaimg.cn/large/0072Vf1pgy1foxlojk0kbj31kw0w0tyb.jpg',
          'https://tva2.sinaimg.cn/large/0072Vf1pgy1fodqnyvneij31hc0u01kx.jpg',
          'https://tva4.sinaimg.cn/large/0072Vf1pgy1foxloigdl2j31kw0w0kib.jpg',
          'https://tva4.sinaimg.cn/large/0072Vf1pgy1foxk782lbsj31hc0u0tr4.jpg',
          'https://tva2.sinaimg.cn/large/0072Vf1pgy1foxlnk8bzcj31hc0u0qia.jpg',
          'https://tva1.sinaimg.cn/large/0072Vf1pgy1foxkiijgosj31hc0u0140.jpg',
          'https://tva3.sinaimg.cn/large/0072Vf1pgy1fodqo0e8fzj31hc0xcqv5.jpg',
          'https://tva1.sinaimg.cn/large/0072Vf1pgy1foxk3wgs1qj31kw0w01jo.jpg',
          'https://tva4.sinaimg.cn/large/0072Vf1pgy1foxkix1n7kj31kw0w0tzl.jpg',
          'https://tva2.sinaimg.cn/large/0072Vf1pgy1foxkjdzgusj31hc0u0nfc.jpg',
          'https://tva4.sinaimg.cn/large/0072Vf1pgy1foxkc2jnyej31hc0u04g2.jpg',
          'https://tva4.sinaimg.cn/large/0072Vf1pgy1foxk3gtfinj31hc0u0k6t.jpg']


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
