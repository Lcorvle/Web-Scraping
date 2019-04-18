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
        from urllib import request
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
        print()

    def simulate_as_browser_scraping(self):
        from urllib import request
        url = 'http://wsjs.saic.gov.cn/txnT01.do?locale=zh_CN&y7bRbP=KamgqGraQoraQoraQtseHtN0MLleD2DHQ3ohTdrMXxma'
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
        print()

    def phantomjs_scraping(self):
        chrome_path = "chromedriver.exe"
        from selenium import webdriver
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        from bs4 import BeautifulSoup
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.action_chains import ActionChains

        # 不加载图片,不缓存在硬盘(内存)
        SERVICE_ARGS = ['--load-images=true', '--disk-cache=false']
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # 创建浏览器, 添加参数设置为无界面浏览器
        driver = webdriver.Chrome(executable_path=chrome_path, service_args=SERVICE_ARGS, chrome_options=chrome_options, port=40)
        # 设置等待时间
        waite = WebDriverWait(driver, 5)
        driver.get('http://wsjs.saic.gov.cn')
        # driver.get('https://www.taobao.com')
        self.driver = driver
        self.save_screen(0)
        js = 'document.getElementsByTagName("table")[0].click()'
        driver.execute_script(js)  # 执行js的方法
        self.save_screen(1)
        input1 = driver.find_element_by_css_selector('#nc')
        input1.send_keys('9')
        self.save_screen(2)
        input1 = driver.find_element_by_css_selector('#mn')
        input1.send_keys('手机')
        self.save_screen(3)
        js = 'document.getElementById("_searchButton").click()'
        driver.execute_script(js)  # 执行js的方法
        self.save_screen(4)
        print()

        page_num_div = driver.find_element_by_css_selector('#mainsrp-pager > div > div > div > div.total')
        text = page_num_div.text
        data = text[2:6]
        print(data)

        # 得到某一个宝贝,商品的大体信息
        def get_product_info():
            waite.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
            # 通过BeautifulSoup取数据
            soup = BeautifulSoup(driver.page_source, 'lxml')
            # 取所有的列表数据
            item_lists = soup.select("#mainsrp-itemlist .items .item")
            for item_list in item_lists:
                item_dict = {}
                image = item_list.select('.J_ItemPic.img')[0].attrs["data-src"]
                if not image:
                    image = item_list.select('.J_ItemPic.img')[0].attrs["data-ks-lazyload"]
                # 销售地
                location = item_list.select(".location")[0].text
                # 价格
                price = item_list.select(".price")[0].text
                # 商店名称
                shopname = item_list.select(".shopname")[0].text.strip()
                # 宝贝名称
                title = item_list.select('a[class="J_ClickStat"]')[0].text.strip()
                # 链接
                data_link = item_list.select('a[class="J_ClickStat"]')[0].attrs["href"]

                item_dict["image"] = "https:" + image
                item_dict["location"] = location
                item_dict["shopname"] = shopname
                item_dict["title"] = title
                item_dict["data_link"] = "https:" + data_link
                item_dict["price"] = price
                print(item_dict)

        # 切换下一页
        def next_page(page):
            print("当前正在加载第%s页的数据--------" % page)
            try:
                input = waite.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div > input')))
                input.clear()  # 清空输入框
                # 页面框添加页码
                input.send_keys(page)
                # 找到确定按钮,点击确定
                driver.find_element_by_css_selector(
                    "#mainsrp-pager > div > div > div > div > span.btn.J_Submit").click()
                waite.until(EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul.items > li.item.active"), str(page)))
            except Exception as e:
                print(e)
                next_page(page)
            # 当前切换后的页面的数据
            get_product_info()

        # data = get_page_num()
        # print('总页数是=', data)
        # for page in range(2, int(data) + 1):
        #     next_page(page)

        # 退出浏览器
        driver.quit()

    def save_screen(self, index=0):
        if self.driver is None:
            return
        import time
        time.sleep(3)
        self.driver.save_screenshot(self.driver.title + str(index) + ".png")
        print(self.driver.title + str(index))

