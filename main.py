import pymysql
import html2md
import requests
import configparser
import utils

DEBUG = 0

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


def set_tag(list_id, term_dic):
    res = ""
    for id in list_id:
        res += f"\n  - {term_dic[id]}"
    return res


def get_post_meta_info(data):
    return data[0], str(data[1]).split(" ")[0], data[2], change_the_name_of_file(data[3])


def change_the_name_of_file(name):
    return name.replace(' ', '-')


def invalid(ct):
    if "<!-- /wp:" in ct:
        return True
    return False


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read("config.ini")
    sql_posts = "select `ID`, `post_date`, `post_content`, `post_title` from forblog.wp_posts where `post_status` = 'publish' and `post_type` = 'post'"
    post_data_all = utils.get_data_in_db(sql_posts)
    term_dic, term_to_post_dic = utils.get_tag_info()

    cnt = 0
    for dt in post_data_all:
        post_id, post_date, post_content, post_title = get_post_meta_info(dt)

        if DEBUG:
            print(post_content)
        if invalid(post_content):
            print(f"Sry that \"{post_title}\" is wordpress's native format which is not supported at present.")
            continue
        content = html2md.work_from_html_to_md(post_content)
        if content == "":
            continue
        tag_content = set_tag(term_to_post_dic[post_id], term_dic)
        meta_data = f"""---
layout: Post
title: {post_title}
date: {post_date}
useHeaderImage: true
headerImage: {img_ls[cnt]}
headerMask: rgba(40, 57, 101, .4)
catalog: {conf.get(section="meta_settings", option="catalog")}
tags: {tag_content}
permalinkPattern: {conf.get(section="meta_settings", option="permalinkPattern")}
---\n"""
        content = meta_data + content
        cnt += 1
        if DEBUG:
            print(content)
        with open(f"./data/docs/{post_title}.md", 'w', encoding='utf-8') as file:
            file.write(content)
        if DEBUG:
            print(f"No.{cnt}:", post_id, post_date, "\"" + post_title + "\"", " Done!")
        else:
            print(f"No.{cnt}:", "\"" + post_title + "\"", " Done!")
