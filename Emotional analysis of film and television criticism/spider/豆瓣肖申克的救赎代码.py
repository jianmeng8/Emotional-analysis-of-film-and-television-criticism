from time import sleep
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 该函数接受一个driver参数，是一个selenium webdriver的实例
def get_data(driver):
    # 设置初始等待和变量
    # 首先等待3秒，然后初始化一个计数器count为0，再等待1秒
    sleep(3)
    count = 0  # 定义一个变量，用来统计爬取数据量
    sleep(1)
    # 定义了一个从366到576的分页循环。但注意，循环开始时page先加1，这意味着实际上是从367页开始
    page=366
    max_page=576
    while True:
        page+=1
        if page > max_page:
            break
        # 打印当前页码
        print("当前在第{}页！！！".format(page))
        #/html/body/div[3]/div[1]/div/div[1]/div[1]/div[19]/div/div/div[1]/div/a
        # 尝试点击页面上的20个展开按钮
        for i in range(20):
            # XPATH是硬编码的，且依赖于页面结构。
            # 变量aaaaaaa被设置为0
            # 捕获了所有异常，但没有具体的异常处理
            try:
                driver.find_element(By.XPATH,'/html/body/div[3]/div[1]/div/div[1]/div[1]/div[{}]/div/div/div[1]/div/a'.format(i)).click()  #点击展开
            except:
                aaaaaaa=0
        # 等待1秒后，获取当前页面的源码
        sleep(1)
        a1 = driver.page_source  # 获取网页源码
        # 使用etree解析HTML
        tree = etree.HTML(a1)
        # 使用了硬编码的XPATH来获取页面上的数据块
        data_list=tree.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div')
        # 遍历data_list，并尝试从每个数据块中提取信息，如电影名（Name）、影评（pinglun）、时间（time）和
        # 话题（huati）。如果提取失败，则设置相应的变量为空字符串
        for data in data_list:
            try:
                Name=data.xpath('.//div/header/a[2]/text()')[0]
            except:
                Name=""
            try:
                pinglun_list=data.xpath('.//div/div/div[2]/div/div/div[1]//text()')
                pinglun=""
                for pl in pinglun_list:
                    pinglun=pinglun+pl.replace("\n","")+"\n"
            except:
                pinglun=""
            try:
                time=data.xpath('.//span[@class="main-meta"]/text()')[0]
            except:
                time=""
            try:
                huati=data.xpath('.//div/div/h2/a/text()')[0]
            except:
                huati=""
            # 每成功提取一次数据，count就加1
            count+=1
            # 打开一个名为'肖申克的救赎影评.csv'的文件，准备写入数据
            file1 = open('肖申克的救赎影评.csv', mode='a', encoding='utf-8-sig', newline='')   #打开这个文件，没有则自动创建，以追加形式写入，’utf-8‘编码方法编码
            write1 = csv.writer(file1)  # 用csv模块创建一个写入器对象
            write1.writerow([Name,time,huati,pinglun])  # 将提取的数据写入CSV文件的当前行
            file1.close()  # 关闭文件
            print("当前正在第{}条!!!".format(count),Name,time,huati)
        # driver.find_element(By.XPATH, '//span[@class="next"]').click()  #点击下一页
        wait = WebDriverWait(driver, 10)  # 等待最多10秒
        # 使用了WebDriverWait和expected_conditions来确保在尝试点击“下一页”按钮之前，该按钮是可点击的
        # 使用了一个XPATH选择器来定位“下一页”按钮，并等待它变得可点击，然后执行点击操作
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="next"]')))
        next_button.click()


if __name__ == "__main__":
    options = Options()  # 实例化对象
    options.add_argument('--disable-blink-features=AutomationControlled')  # 配置反爬措施\
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    # 隐藏提示条
    driver = webdriver.Chrome(options=options)  # 定义自动化对象driver
    get_data(driver)
    wait = WebDriverWait(driver, 10)  # 等待最多10秒
    print("爬取结束")
