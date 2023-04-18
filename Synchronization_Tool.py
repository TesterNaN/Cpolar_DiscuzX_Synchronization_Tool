from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import requests
import pymysql
import urllib
import time
import git
import os

#######################################

Website_root=r""    #DiscuzX根目录位置(结尾不加"/")
Cpolar_user=""    #Cpolar用户名
Cpolar_pwd=""    #Cpolar密码
Mysql_ip=""    #mysql服务器IP(一般为127.0.0.1)
Mysql_user=""    #mysql数据库用户名
Mysql_pwd=""     #mysql数据库密码
Mysql_database_name=""    #mysql数据库名称
UC_key=""    #UCenter通信密钥
git_ssh=""    #Github Page的SSH地址

#######################################

bat3=open('del.bat',mode='w+')
bat3.write("@echo off&rmdir git /s /q")
bat3.close()
os.system("del.bat")

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver_service = Service(executable_path="geckodriver.exe")
driver = webdriver.Firefox(service=driver_service,options=options)
driver.get("http://localhost:9200/")
driver.find_element(By.XPATH, "/html/body/div/div/form/div[2]/div/div/input").send_keys(Cpolar_user)
driver.find_element(By.XPATH, "/html/body/div/div/form/div[3]/div/div/input").clear()
driver.find_element(By.XPATH, "/html/body/div/div/form/div[3]/div/div/input").send_keys(Cpolar_pwd)
driver.find_element(By.XPATH, "/html/body/div/div/form/button").click()
time.sleep(2)
driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div[1]/div/ul/div[3]/li/div").click()
driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div[1]/div/ul/div[3]/li/ul/div[1]/a/li").click()
time.sleep(2)
ip=driver.find_element(By.XPATH, '/html/body/div/div/div[2]/section/div/div/div[3]/table/tbody/tr[3]/td[3]/div').text
driver.quit()

php=open(Website_root+r'\config\config_ucenter.php',mode='w+')
php.write("<?php\n\n\ndefine('UC_CONNECT', 'mysql');\n\ndefine('UC_DBHOST', '"+Mysql_ip+"');\ndefine('UC_DBUSER', '"+Mysql_user+"');\ndefine('UC_DBPW', '"+Mysql_pwd+"');\ndefine('UC_DBNAME', '"+Mysql_database_name+"');\ndefine('UC_DBCHARSET', 'utf8');\ndefine('UC_DBTABLEPRE', '`"+Mysql_database_name+"`.pre_ucenter_');\ndefine('UC_DBCONNECT', 0);\n\ndefine('UC_CHARSET', 'utf-8');\ndefine('UC_KEY', '"+UC_key+"');\ndefine('UC_API', '"+ip+"/uc_server');\ndefine('UC_APPID', '1');\ndefine('UC_IP', '');\ndefine('UC_PPP', 20);")
php.close()

db = pymysql.connect(host=Mysql_ip,user=Mysql_user,password=Mysql_pwd,database=Mysql_database_name)
cursor = db.cursor()
cursor.execute("UPDATE `pre_ucenter_applications` SET `url` = '"+ip+"' WHERE `pre_ucenter_applications`.`appid` = 1")
db.close()

repo = git.Repo.init(path='./git')
remote = repo.create_remote(name='origin', url=git_ssh)

sh1=open('./git/pull.sh',mode='w+')
sh1.write('touch index.html\ngit add index.html\ntime2=$(date "+%Y%m%d%H%M%S")\ngit commit -m $time2\ngit push -u origin "master"')
sh1.close()

sh2=open('./git/push.sh',mode='w+')
sh2.write('git remote add origin '+git_ssh+'\ngit pull origin "master" --allow-unrelated-histories')
sh2.close()

bat1=open('push.bat',mode='w+')
bat1.write("@echo off&cd %~dp0\git\nstart push.sh")
bat1.close()
os.system("push.bat")
input()

file_handle=open('./git/index.html',mode='w+')
file_handle.write('<script type="text/javascript" id="'+str(time.time())+'">window.location.href="'+ip+'"</script>')
file_handle.close()

bat=open('pull.bat',mode='w+')
bat.write("@echo off&cd %~dp0\git\nstart pull.sh")
bat.close()
os.system("pull.bat")

bat2=open('del.bat',mode='w+')
bat2.write("@echo off&del push.bat\ndel pull.bat\ndel del.bat\nrmdir git /s /q\npause")
bat2.close()

time.sleep(10)
os.system("del.bat")
