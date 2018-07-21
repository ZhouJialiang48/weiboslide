#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/20 19:37
# @Author  : zhoujl
# @Site    : 
# @File    : crack.py
# @Software: PyCharm
import time
from io import BytesIO
from os import listdir
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config import *
from error import NoMatchedTemplateError


class WeiboSlideCracker():
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = USERNAME
        self.password = PASSWORD

    def __del__(self):
        self.browser.close()

    def open(self):
        """
        打开登陆网站，输入用户名密码，点击登录
        :return:
        """
        self.browser.get(LOGIN_URL)
        time.sleep(1)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.presence_of_element_located((By.ID, 'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

    def get_position(self):
        """
        获取验证码位置
        返回图片的四条边横纵坐标值
        :return:
        """
        try:
            img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'patt-shadow')))
            time.sleep(2)
            location = img.location
            size = img.size
            top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + \
                                       size['width']
            return (top, bottom, left, right)
        except TimeoutException:
            print('未出现验证码')
            self.open()

    def get_screenshot(self):
        """
        获取网页截图
        :return:
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_image(self, name='captcha.png'):
        """
        返回验证码图片
        :param name:
        :return:
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        screenshot.save('screenshot.png')
        # 若是Retina屏，先对分辨率进行还原
        # 否则直接截取验证码区域图片
        if RETINA:
            captcha = screenshot.crop((2 * left, 2 * top, 2 * right, 2 * bottom))
            captcha = captcha.resize((right - left, bottom - top), Image.ANTIALIAS)
        else:
            captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1:
        :param image2:
        :param x:
        :param y:
        :return:
        """
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 20
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def same_image(self, image, template):
        """
        判断当前验证码与验证码模板是否相同
        :param image:
        :param template:
        :return:
        """
        threshold = 0.99
        count = 0
        for x in range(image.width):
            for y in range(image.height):
                if self.is_pixel_equal(image, template, x, y):
                    count += 1
        result = float(count) / (image.width * image.height)
        if result > threshold:
            print('匹配成功')
            return True
        return False

    def detect_match(self, image):
        """
        寻找匹配模板，返回匹配模板编号，即拖动顺序
        :param image:
        :return:
        """
        for template_name in listdir(TEMPLATES_DIR):
            print('正在匹配', template_name)
            template = Image.open(TEMPLATES_DIR + template_name)
            if self.same_image(image, template):
                numbers = [int(number) for number in list(template_name.split('.')[0])]
                print('拖动顺序', numbers)
                return numbers
        raise NoMatchedTemplateError

    def move(self, numbers):
        """
        根据顺序，模拟拖动
        :param numbers:
        :return:
        """
        circles = self.browser.find_elements_by_css_selector('.patt-circ')
        dx = dy = 0
        for step in range(4):
            circle = circles[numbers[step] - 1]
            # 如果第一次循环，则点击第一个按钮
            if step == 0:
                ActionChains(self.browser) \
                    .move_to_element_with_offset(circle, circle.size['width'] / 2, circle.size['height'] / 2) \
                    .click_and_hold().perform()
            # 否则，移动到下一目标点
            else:
                # 小幅移动次数
                times = 30
                # 分times次拖动到下一个目标点
                for i in range(times):
                    ActionChains(self.browser).move_by_offset(dx / times, dy / times).perform()
                    time.sleep(1 / times)
            if step == 3:
                ActionChains(self.browser).release().perform()
            else:
                # 下一次所需水平位移
                dx = circles[numbers[step + 1] - 1].location['x'] - circle.location['x']
                # 下一次所需竖直位移
                dy = circles[numbers[step + 1] - 1].location['y'] - circle.location['y']

    def crack(self):
        self.open()
        image = self.get_image('captcha.png')
        numbers = self.detect_match(image)
        self.move(numbers)
        time.sleep(10)
        print('识别结束')


if __name__ == '__main__':
    cracker = WeiboSlideCracker()
    cracker.crack()
