#!/usr/bin/env python
# encoding: utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import requests
from bs4 import BeautifulSoup

pic_dir = './unsplash'

def unsplash(page):
    headers = {
    'Accept':'*/*; q=0.01',
    'Accept-Encoding':'gzip,deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Referer':'https://unsplash.com/?page={0}'.format(page),
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.102 Safari/537.36'
    }
    r = requests.get('https://unsplash.com/?page={0}'.format(page),headers=headers)
    print '爬取第{0}页成功'.format(page)
    soup = BeautifulSoup(r.text)
    urls = soup.select('.photo a')
    pics = []
    for url in urls:
        pics.append(url.get('href'))
    return pics

def download(pics):
    headers = {
    'Accept':'*/*; q=0.01',
    'Accept-Encoding':'gzip,deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Referer':'https://unsplash.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.102 Safari/537.36'
    }
    ret = []
    for pic in pics:
        id = pic.split('/')[-2]
        file_name = 'unsplash/{0}.jpg'.format(id)
        ret.append(file_name)
        if os.path.exists(file_name):
            continue
        print '开始下载图片 https://unsplash.com/photos/{0}/download'.format(id)
        with open('unsplash/{0}.jpg'.format(id), 'wb') as f:
            f.write(requests.get('https://unsplash.com/photos/{0}/download'.format(id),headers = headers).content)
    return ret

class UnsplashShow(QWidget):
    def __init__(self, pics):
        super(QWidget, self).__init__()
        self.pics = pics
        self.initUI()

    def initUI(self):
        pic = QPixmap(self.pics[-1]).scaledToHeight(480)
        self.pic = piclabel = QLabel(self)
        piclabel.setPixmap(pic)

        slider = QSlider(Qt.Horizontal, self)
        slider.setTickPosition(QSlider.TicksBelow)
        m = len(self.pics) - 1
        slider.setMaximum(m)
        slider.setSliderPosition(m)
        slider.valueChanged[int].connect(self.changePic)

        vbox = QVBoxLayout()
        vbox.addWidget(piclabel)
        vbox.addWidget(slider)
        self.setLayout(vbox)

        self.resize(960 + 10, 720 + 50)
        self.setWindowTitle('unsplash')
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Q:
            self.close()

    def changePic(self, value):
        pic = QPixmap(self.pics[value]).scaledToHeight(480)
        self.pic.setPixmap(pic)

def main():
    pic_page = unsplash(1)
    pics = download(pic_page)
    app = QApplication(sys.argv)
    us = UnsplashShow(pics)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
