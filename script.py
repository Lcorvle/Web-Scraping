from Crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler()
    # try:
    #     crawler.simple_scraping()
    # except BaseException as e:
    #     print("simple_scraping 失败：", e)
    # else:
    #     print("simple_scraping 成功")
    #
    # try:
    #     crawler.simulate_as_browser_scraping()
    # except BaseException as e:
    #     print("simulate_as_browser_scraping 失败：", e)
    # else:
    #     print("simulate_as_browser_scraping 成功")
    #
    # try:
    #     crawler.phantomjs_scraping()
    # except BaseException as e:
    #     print("phantomjs_scraping 失败：", e)
    # else:
    #     print("phantomjs_scraping 成功")
    # exit(1)
    try:
        crawler.js_scraping()
    except BaseException as e:
        print("js_scraping 失败：", e)
    else:
        print("js_scraping 成功")



