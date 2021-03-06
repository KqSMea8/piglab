#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 从百度图片下载车牌照片，用于训练素材
import re
import uuid
import requests
import os


class DownloadImages:
    def __init__(self, download_max, key_word):
        self.download_sum = 0
        self.download_max = download_max
        self.key_word = key_word
        self.save_path = './data/download/'

    def start(self):
        self.download_sum = 0
        gsm = 80
        str_gsm = str(gsm)
        pn = 0
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        while self.download_sum < self.download_max:
            str_pn = str(self.download_sum)
            url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&' \
                  'word=' + self.key_word + '&pn=' + str_pn + '&gsm=' + str_gsm + '&ct=&ic=0&lm=-1&width=0&height=0'
            print url
            result = requests.get(url)
            self.downloadImages(result.text)
        print '下载完成'

    def downloadImages(self, html):
        img_urls = re.findall('"objURL":"(.*?)",', html, re.S)
        print '找到关键词:' + self.key_word + '的图片，现在开始下载图片...'
        for img_url in img_urls:
            print '正在下载第' + str(self.download_sum + 1) + '张图片，图片地址:' + str(img_url)
            try:
                pic = requests.get(img_url, timeout=50)
                #pic_name = self.save_path + '/' + str(uuid.uuid1()) + '.jpg'
                pic_name = self.save_path + '/' + str(self.download_sum + 1) + '.jpg'
                with open(pic_name, 'wb') as f:
                    f.write(pic.content)
                self.download_sum += 1
                if self.download_sum >= self.download_max:
                    break
            except  Exception, e:
                print '【错误】当前图片无法下载，%s' % e
                continue


if __name__ == '__main__':
    downloadImages = DownloadImages(100, '车牌')
    downloadImages.start()
