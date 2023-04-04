from .utils import *


def crawl_shopee_categories_from_home():
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=otps)
    driver.get("https://shopee.vn/")

    try:
        close = driver.execute_script(
            'return document.querySelector("#main shopee-banner-popup-stateful").shadowRoot.querySelector("div.home-popup__close-area div.shopee-popup__close-btn")')
        close.click()
    except Exception as e:
        print("cannot close ad shopee", e)

    try:
        next = driver.execute_script(
            'return document.querySelector("div.LYxxi- div.carousel-arrow--next")')
        next.click()
        time.sleep(2)
        image_menu = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.K34m1x")))
    except Exception as e:
        print(f"cannot load other categories shopee {e}")

    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    for a in soup.find_all('a', href=True, attrs={"class": "home-category-list__category-grid"}):
        link = "https://shopee.vn" + a['href']
        a.find('div', attrs={"class": "K34m1x"}).text

    SourceData.objects.filter(platform='Shopee').delete()

    for a in soup.find_all('a', href=True, attrs={"class": "home-category-list__category-grid"}):
        category_link = "https://shopee.vn" + a['href']
        description = "Shopee " + a.find('div', attrs={"class": "K34m1x"}).text

        source = SourceData()
        source.platform = "Shopee"
        source.link = f"{category_link}"
        source.description = unidecode(description)
        source.save()

    driver.quit()


def crawl_shopee_categories():
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=otps2)
    driver.get("https://shopee.vn/all_categories")

    try:
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")

        for a in soup.find_all('a', href=True, attrs={"class": "a-sub-category--display-name"}):
            a['href']
            a.text

        SourceData.objects.filter(platform='Shopee').delete()

        for a in soup.find_all('a', href=True, attrs={"class": "a-sub-category--display-name"}):
            category_link = "https://shopee.vn" + a['href']
            description = "Shopee " + a.text

            source = SourceData()
            source.platform = "Shopee"
            source.link = f"{category_link}"
            source.description = unidecode(description)
            source.save()

        driver.quit()

    except Exception as e:
        print(e)
        driver.quit()


def shopee_recrawl_product():
    product_list = []
    products = Product.objects.annotate(image_count=Count("images")).filter(
        source_description__startswith="Shopee", crawled__in=[True])

    product_list = [
        product for product in products if product.image_count == 0]

    if len(product_list) > 0:
        for _ in range(2):
            print(len(product_list))
            n = 0
            while True:
                crawl_shopee_image_multithread(
                    product_list[n:min(len(product_list), n + 60)], recrawl=True, try_time=0)
                n += 60
                if n >= len(product_list):
                    break
            products = Product.objects.annotate(image_count=Count("images")).filter(
                source_description__startswith="Shopee", crawled__in=[True])
            product_list = [
                product for product in products if product.image_count == 0]
            if len(product_list) == 0:
                break
    products = Product.objects.annotate(image_count=Count("images")).filter(
        source_description__startswith="Shopee", crawled__in=[True])
    product_list = [
        product for product in products if product.image_count == 0]
    for product in product_list:
        product.delete()


def crawl_shopee_all():
    """
    crawl everything of shopee source, product, image with multithread
    """

    try_time = 3
    # try again if any error occur
    while try_time >= 0:
        try:
            try_time -= 1
            sources = SourceData.objects.filter(
                platform='Shopee', crawled__in=[False])
            threads = []
            # distribute source for threads
            for thread_num in range(0, THREAD_NUMBER_LINK_SOURCE):
                threads.append(PropagatingThread(
                    target=crawl_shopee_page_multithread, args=(sources, thread_num,)))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            sources = SourceData.objects.filter(
                platform='Shopee', crawled__in=[False])
            if len(sources) == 0:
                return
        except Exception as e:
            print("crawl shopee all error ", e)


def crawl_shopee_page_multithread(sources, thread_num):
    """
    decide which source of each thread belong to and init webdriver
    """
    # sources = sources[:2]

    try:
        source_quantity = len(sources)
        for i in range(source_quantity):
            if i % THREAD_NUMBER_LINK_SOURCE == thread_num:
                driver = webdriver.Chrome(service=Service(
                    ChromeDriverManager().install()), options=otps)
                crawl_shopee_page(sources[i], driver)
                driver.quit()

    except Exception as err_374:
        driver.quit()
        print('shopee multithread crawl page error', err_374)


def crawl_shopee_image(product, driver):
    driver.get(product.link)
    try_times = 0
    crawled = True
    len_old = 0
    # try again if cannot find element to click to open image menu or close 18+ alert
    while try_times < 3:
        try:
            # try:
            """close 18+ alert"""
            alert_close = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.shopee-alert-popup__btn.btn-solid-primary")))
            alert_close.click()
            break
            # except:
            #     pass
            """open image menu (removed)"""
            # image_menu = WebDriverWait(driver, 2).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, f"div.MZ9yDd:nth-of-type({2 if try_times < 7 else 1})")))
            # image_menu.click()
            # break
        except Exception as e:
            # print("check", e)
            # time.sleep(1)
            try_times += 1
    # print(f'done 0 {product.name}')

    try_times = 0
    while try_times < 10:

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".MZ9yDd div")))
        except Exception as e:
            # print(e)
            try_times += 1

        try_times += 1
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        all_soup = soup.find_all('div', attrs={"class": "MZ9yDd"})
        len_new = len(all_soup)
        if len_new == 0 or len_new != len_old:
            len_old = len_new
            time.sleep(1)
        else:
            try:
                for a in all_soup:
                    image_link = a.find(
                        'div', attrs={"class": "A4dsoy uno8xj"})['style']
                    image_link = re.findall("url\(\"(.+)\"\)", image_link)[0]
                soup.select(".dR8kXc a.akCPfg:last-of-type")[0].text
                break
            except:
                time.sleep(1)
                pass

    next_button = True
    new_image = False
    while next_button:
        content = driver.page_source
        next_button = False
        for _ in range(2):
            soup = BeautifulSoup(content, "html.parser")
            try:
                fail = 0
                for a in soup.find_all('div', attrs={"class": "MZ9yDd"}):
                    try:
                        image_link = a.find(
                            'div', attrs={"class": "A4dsoy uno8xj"})['style']
                        image_link = re.findall(
                            "url\(\"(.+)\"\)", image_link)[0]

                        images = Image.objects.filter(
                            link=f"{image_link}", product=product)
                        
                        if len(images) > 1:
                            for image in images:
                                image.delete()
                            i = Image()
                        elif len(images) == 0:
                            i = Image()
                        else:
                            i = images[0]
                            new_image = True

                        if check_update_expire(i):
                            i.link = f"{image_link}"
                            i.product = product
                            i.embedding_vector = json.dumps(exact_embedding_from_link(
                                i.link))
                            next_button = True
                            i.save()
                            new_image = True
                    except Exception as e:
                        print("craw image shopee product error", e)

                        fail += 1
                        pass
                if fail != 0:
                    raise exceptions.ValidationError('shopee load image error')
                break
            except Exception as e:
                print('shopee not load image after click next', e)
                time.sleep(1)

        for i in range(2):
            try:
                image_menu = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"button.shopee-icon-button.JaQdda.Xr3frH")))
                for _ in range(5):
                    image_menu.click()

                time.sleep(1)
                break
            except Exception as e:
                if i == 1:
                    next_button = False
                time.sleep(1)
                print(f"shopee click next error {i}")
                pass

    gc.collect()
    if new_image:
        try:
            addition_category = ''
            category = soup.select(".dR8kXc a.akCPfg:last-of-type")[0].text
            print(category)
            if unidecode(category).lower() == 'khac':
                addition_category = soup.select(".dR8kXc a.akCPfg:nth-last-child(3)")[0].text
                print(addition_category)
                category = f'{addition_category} {category}'
                print(category)
            print(1)
            product.category, _ = Category.objects.get_or_create(
                name=unidecode(category).lower())
            print(2)    
            product.crawled = True
            print(3)
            product.save()
            print(4)
        except Exception as e:
            print(f"get category error product {product.id}: {e}")


def crawl_shopee_image_multithread(product_list, recrawl=False, try_time=3):
    # try_time = 3
    while try_time >= 0:
        try:
            cleanup_webdriver()
            cleanup_category()
        except Exception as ewd:
            print("cleanup webdriver", ewd)
        products_not_crawled = get_not_crawl_products(
            product_list) if not recrawl else product_list
        if len(products_not_crawled) == 0:
            return

        try_time -= 1

        try:
            threads = []
            l = len(products_not_crawled)
            if l == 0:
                return
            for thread_num in range(0, THREAD_QUANTITY_CRAWL_PRODUCT):
                threads.append(PropagatingThread(
                    target=crawl_shopee_image_thread, args=(products_not_crawled, thread_num,)))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

        except Exception as e:
            print("shopee crawl image error", e)
            pass

        # exact_embedding_vector_product(product_list)


def crawl_shopee_image_thread(product_list, thread_num):
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=otps2)
    print(f'thread {thread_num} crawling image')
    try:
        l = len(product_list)
        for i in range(l):
            if i % THREAD_QUANTITY_CRAWL_PRODUCT == thread_num:
                try:
                    crawl_shopee_image(product_list[i], driver)
                except Exception as err:
                    print('shopee crawl image error thread', thread_num,   err)
                    driver.quit()
                    try:
                        cleanup_webdriver()
                        cleanup_category()
                    except Exception as e:
                        print(e)
                        pass
                    driver = webdriver.Chrome(service=Service(
                        ChromeDriverManager().install()), options=otps2)
        driver.quit()
        gc.collect()

    except Exception as e:
        driver.quit()
        print('shopee multithread crawl image error', e)
    print(f'thread {thread_num} crawling image done')


def shopee_scroll_to_end(driver):
    try:
        height = driver.execute_script("return document.body.scrollHeight")
        scroll_length = 0
        scroll_step = 500
        while scroll_length < height:
            # print(scroll_length, height)
            driver.execute_script(
                f"window.scrollTo({scroll_length}, {scroll_length + scroll_step})")
            scroll_length += scroll_step
            time.sleep(0.5)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-sqe=\"link\"]")))
            height = driver.execute_script("return document.body.scrollHeight")
    except Exception as e:
        print("shopee scroll end error", e)


def crawl_shopee_page(source, driver):
    link = source.link
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=otps)
    same = 0
    product_list = []
    try:
        print("crawling", link)
        driver.get(link)

    except Exception as e_481:
        print("crawl shopee page 0 error", e_481)

    prev_url = ''
    while same <= 4:

        try:
            print(driver.current_url)
            try_time = 3
            if (driver.current_url == prev_url):
                same += 1
                time.sleep(1)
                # print('same', same, prev_url)
                if same == 2:
                    driver.get(driver.current_url)
            else:
                prev_url = driver.current_url 
                same = 0
                # print('new', same)
            shopee_scroll_to_end(driver)
            
            new_product = False
            while try_time >= 0:

                try_time -= 1
                failed = False

                content = driver.page_source
                print(driver.current_url)
                soup = BeautifulSoup(content, "html.parser")
                product_list = []
                for a in soup.find_all('div', attrs={"class": "col-xs-2-4 shopee-search-item-result__item"}):
                    try:
                        product_price = a.find(
                            'span', attrs={"class": "du3pq0"}).getText()
                        product_name = a.find(
                            'div', attrs={"class": "_1yN94N WoKSjC _2KkMCe"}).getText()  # name
                        product_link = a.find(
                            'a', attrs={"data-sqe": "link"})['href'].split('?')[0]  # product link

                        products = Product.objects.filter(
                            name=f"{unidecode(product_name)}")

                        if len(products) > 1:
                            for product in products:
                                print(f'delete product {product.id}')
                                product.delete()
                            p = Product()
                        elif len(products) == 0:
                            p = Product()
                        else:
                            p = products[0]
                        # p = Product() if len(products) == 0 else products[0]

                        if check_update_expire(p):
                            p.link = f"https://shopee.vn{product_link}"
                            p.name = unidecode(product_name)
                            p.price = unidecode(product_price)
                            p.source_description = source.description
                            # p.key_words.extend(new_key_words)
                            p.save()
                            new_product = True
                            product_list.append(p)
                    except Exception as e1:
                        failed = True
                        print("shopee crawl page find element", e1)

                if not failed:
                    break

        except Exception as err:
            print(f'shopee crawl page error {link}', err)
            pass

        if new_product:
            crawl_shopee_image_multithread(product_list)

        try:
            next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".shopee-icon-button.shopee-icon-button--right")))
            next_page.click()
        except Exception as e_533:
            print(f'shopee change page error {link}', e_533)
            pass
    source.crawled = True
    source.save()
    gc.collect()
    # driver.quit()
