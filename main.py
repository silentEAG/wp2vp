import pymysql
import html2md
import requests
import configparser
import utils

DEBUG = 0


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
headerImage: {utils.img_ls[cnt]}
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
