import configparser

from bs4 import BeautifulSoup
import pymysql
import html2md
import requests

conf = configparser.ConfigParser()
conf.read("../config.ini")

print(conf.items(section="self_meta_settings"))