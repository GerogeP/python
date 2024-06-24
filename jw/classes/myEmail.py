#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import smtplib, ssl
from email.mime.text import MIMEText
from email.header import Header
 
# 第三方 SMTP 服务
mail_host="smtp.189.com"  #设置服务器
mail_user="panglili"    #用户名
mail_pass="eF%7uL)4E%3dU%3e"   #口令 
 
 
sender = 'panglili@189.com'
receivers = ['georgepanglili@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
 
message = {
        'subject': 'Python 邮件发送测试...',
        'From': "jw test",
        'To': "测试",
        'subject': 'Python SMTP 邮件测试'
        } 
 
print(message)

try:
    smtpObj = smtplib.SMTP() 
    smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
    smtpObj.login(mail_user,mail_pass)  
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")
