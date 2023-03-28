from .utils import *

def crawl_lazada_categories():
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=otps)
    driver.get("https://www.lazada.vn/")

    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    for a in soup.find_all('li', attrs={"class": "lzd-site-menu-sub-item"}):
        category_link = a.find('a', href=True)
        description = unidecode(category_link.find('span').text)

    for a in soup.find_all('a', href=True, attrs={"class": "UPUwyq"}):
        a.text
        a['href']

    SourceData.objects.filter(platform='Lazada').delete()

    for a in soup.find_all('li', attrs={"class": "lzd-site-menu-sub-item"}):
        category_link = a.find('a', href=True)
        description = "Lazada " + category_link.find('span').text
        source = SourceData()
        source.platform = "Lazada"
        source.link = f"https:{category_link['href']}"
        source.description = description
        source.save()

    driver.quit()

def crawl_lazada_all():
    sources = SourceData.objects.filter(platform='Lazada')

    threads = []
    for thread_num in range(0, THREAD_NUMBER_LINK_SOURCE):
        threads.append(PropagatingThread(
            target=crawl_lazada_page_multithread, args=(sources, thread_num,)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


# def crawl_lazada_multi_page(source):
#     driver = webdriver.Chrome(
#         "D:\Downloads\chromedriver_win32\chromedriver.exe", options=otp)
#     # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=otp)
#     if source.multi_page == True:
#         for page in range(source.min_page, source.max_page+1):
#             print(f"{source.link}{page}")
#             crawl_lazada_page(f"{source.link}{page}",
#                              driver, source.key_words)
#     else:
#         crawl_lazada_page(source.link, driver, source.key_words)

#     driver.quit()


def crawl_lazada_page_multithread(sources, thread_num):
    source_quantity = len(sources)
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=otps)
    for i in range(source_quantity):
        if i % THREAD_NUMBER_LINK_SOURCE == thread_num:
            crawl_lazada_page(sources[i], driver, thread_num)
    driver.quit()


def crawl_lazada_page(source, driver, thread_num):
    link = source.link

    # webdriver.Chrome("D:\Downloads\chromedriver_win32\chromedriver.exe", options=otp)
    try:
        product_list = []
        driver.get(link)
        same = 0
    except Exception as e:
        print("crawl lazada page 0 error", e)
    while same <= 5:
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        print(f"crawling page {thread_num} {driver.current_url}")
        product_list = []
        same += 1

        for a in soup.find_all('div', attrs={"class": "qmXQo"}):
            try:
                product_info = a.find('div', attrs={"class": "RfADt"}).find(
                    'a', attrs={'age': '0'},  href=True)
                price = a.find('span', attrs={"class": "ooOxS"})
                product_info.getText()  # name
                product_info['href']  # product link
                price.text  # price

                products = Product.objects.filter(
                    link=f"https:{product_info['href']}")

                p = Product() if len(products) == 0 else products[0]

                if check_update_expire(p):
                    p.link = f"https:{product_info['href']}"
                    p.name = unidecode(product_info.getText())
                    p.price = unidecode(price.text)
                    p.source_description = unidecode(source.description)
                    p.save()
                    same = 0
                    product_list.append(p)

            except Exception as e:
                print("crawl page error", e)
                pass

        # crawl_lazada_image_multithread(product_list)

        try:
            next_page = WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "li[title = \"Next Page\"] button.ant-pagination-item-link:not([disabled])")))
            next_page.click()
        except:
            print(f'lazada change page error {link}', e)
            pass
    # driver.quit()


def crawl_lazada_image_multithread(product_list):
    try:
        threads = []
        l = len(product_list)
        if l == 0:
            return
        for thread_num in range(0, THREAD_QUANTITY_CRAWL_PRODUCT):
            threads.append(PropagatingThread(
                target=crawl_lazada_image_thread, args=(product_list, thread_num,)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    except Exception as e:
        print("crawl image error", e)
        pass


def crawl_lazada_image_thread(product_list, thread_num):
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=otps)

    l = len(product_list)
    for i in range(l):
        if i % THREAD_QUANTITY_CRAWL_PRODUCT == thread_num:
            crawl_lazada_image(product_list[i], driver)

    driver.quit()


def crawl_lazada_image(product, driver):
    driver.get(product.link)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    for a in soup.find_all('img', attrs={"class": "pdp-mod-common-image item-gallery__thumbnail-image"}):
        try:
            a['src']
            images = Image.objects.filter(link=f"{a['src']}")

            i = Image() if len(images) == 0 else images[0]

            if check_update_expire(i):
                i.link = f"{a['src']}"
                i.product = product
                i.save()

        except Exception as e:
            print("craw image product error", e)
            pass