from ctypes import *
import os
from urllib import request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import time
import win32api
import win32con


class Crawler(object):
    """
    Wed crawler
    """
    random_state = 42
    driver = None

    def __init__(self, random_state=None):
        self.random_state = random_state
        self.driver = None

    def simple_scraping(self):
        url = 'http://wsjs.saic.gov.cn/txnS01.do?y7bRbp=qmM60ZTGrmfFTNlWpVsGVJzNaFkX6j6kdsG47HvET_N1cCD6oa1Vn25OOxaXXsKRL0zNckk6r5b0f.CA3PlUlErkljZxgxs15suUISKeU1UjjJGnYT7iYfaWM7c5UrlAzmhSmSLuF8OCXkphqS79S6GCGqi&c1K5tw0w6_=2JwTPeGol02uJIEoS5AsnFj0nIDNIDLYHq.dvjno1tAr0uo69TWnCUjSDyXIKk2QUgW3a.5d5PvreevqPtlreFwiQotVSWxyEAZrm9OYRj9K0HF3TPJHIRv_hdqypDtJY'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            # 'Accept': 'text/html;q=0.9,*/*;q=0.8',
            # 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            # 'Accept-Encoding': 'gzip',
            # 'Connection': 'close',
            'Referer': 'http://wsjs.saic.gov.cn/txnT01.do?locale=zh_CN&y7bRbP=KamgqGraQoraQoraQtseHtN0MLleD2DHQ3ohTdrMXxma'  # 注意如果依然不能抓取，这里可以设置抓取网站的host
            }
        opener = request.Request(url, headers=headers)
        response = request.urlopen(opener)
        print(response.code)
        html = response.read().decode('utf-8')
        print(html)

    def simulate_as_browser_scraping(self):
        url = 'http://wsjs.saic.gov.cn/txnT01.do?locale=zh_CN&y7bRbP=KamgqGraQoraQoraQtseHtN0MLleD2DHQ3ohTdrMXxma'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'Referer': 'http://wsjs.saic.gov.cn/txnT01.do?locale=zh_CN&y7bRbP=KamgqGraQoraQoraQtseHtN0MLleD2DHQ3ohTdrMXxma'  # 注意如果依然不能抓取，这里可以设置抓取网站的host
            }
        opener = request.Request(url, headers=headers)
        response = request.urlopen(opener)
        print(response.code)
        html = response.read().decode('utf-8')
        print(html)

    def phantomjs_scraping(self):
        chrome_path = "chromedriver.exe"

        # 不加载图片,不缓存在硬盘(内存)
        SERVICE_ARGS = ['--load-images=true', '--disk-cache=false']
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # 创建浏览器, 添加参数设置为无界面浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Referer': 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearch.html?annNum=1605',
            'Host': 'sbgg.saic.gov.cn:9080',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Origin': 'http://sbgg.saic.gov.cn:9080'
        }

        cap = dict(DesiredCapabilities.CHROME)

        for key, value in headers.items():
            cap['phantomjs.page.settings.' + key] = value
        driver = webdriver.Chrome(executable_path=chrome_path, service_args=SERVICE_ARGS, chrome_options=chrome_options, port=40, desired_capabilities=cap)
        driver.set_window_size(1400, 900)
        # 设置等待时间
        waite = WebDriverWait(driver, 5)

        driver.get('http://wsjs.saic.gov.cn')
        # driver.get('https://www.taobao.com')
        self.driver = driver
        handle = driver.current_window_handle
        self.save_screen(0)
        js = 'document.getElementsByTagName("a")[0].click()'    # 点击“关于使用商标网上查询系统的说明”
        driver.execute_script(js)
        self.save_screen(1)
        js = 'document.getElementsByTagName("a")[14].click()'   # 点击“首页”
        driver.execute_script(js)
        self.save_screen(2)
        js = 'document.getElementsByTagName("a")[39].click()'   # 点击“网上查询”
        driver.execute_script(js)
        self.save_screen(3)
        handles = driver.window_handles         # 切换到“商标查询”标签页
        for new_handle in handles:
            if new_handle != handle:
                driver.switch_to_window(new_handle)
                break
        js = 'document.getElementsByTagName("a")[24].click()'    # 点击“我接受”
        driver.execute_script(js)
        self.save_screen(4)
        js = 'document.getElementById("nc").value = 9;'    # 设置输入框值
        driver.execute_script(js)
        self.save_screen(5)

        # 退出浏览器
        driver.quit()

    def save_screen(self, index=0):
        if self.driver is None:
            return
        time.sleep(5)
        self.driver.save_screenshot(self.driver.title + str(index) + ".png")
        print(self.driver.title + str(index))

    def js_scraping(self):
        class POINT(Structure):
            _fields_ = [("x", c_ulong), ("y", c_ulong)]

        po = POINT()

        def mouse_move(x, y):
            windll.user32.SetCursorPos(x, y)

        def get_mouse_point():
            windll.user32.GetCursorPos(byref(po))
            return int(po.x), int(po.y)

        os.system('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" http://wsjs.saic.gov.cn')
        time.sleep(5)
        dx = 1
        mouse_move(400, 400)
        while True:
            x, y = get_mouse_point()
            mouse_move(x + dx, y)
            dx = -dx
