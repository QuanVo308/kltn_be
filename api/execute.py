from .scheduler_jobs import *
from .serializers import *
from .utils import *
from .crawl_shopee import *
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()


# scheduler.add_job(FirstCronTest, 'interval', seconds=1)
RANDOM_PRODUCTS_SERIALIZER = []


def get_random_product():
    global RANDOM_PRODUCTS_SERIALIZER

    print('getting random product')
    products = list(Product.objects.all())
    random.shuffle(products)
    RANDOM_PRODUCTS_SERIALIZER = ProductSearchSerializer(
        products[:600], many=True).data
    print('getting random product done')


def get_random_product_serializer():
    products = RANDOM_PRODUCTS_SERIALIZER
    return products


def cleanup_temp_folder():
    print('cleanup_temp_folder')
    base_dir = pathlib.Path('temp')
    for path in base_dir.glob("*"):
        create_time = time.time() - os.path.getctime(path)
        # print(path, time.time() - os.path.getctime(path))
        if create_time > 3600:
            try:
                shutil.rmtree(str(path.resolve()))
            except:
                pass
            try:
                os.remove(str(path.resolve()))
            except:
                pass

def test():
    print('testting')
    test_process, _ = BackgroundProcess.objects.get_or_create(name = 'test')
    run = True
    start = timezone.now()
    runtime = timezone.now() - test_process.updated_at

    if test_process.running == True and runtime.total_seconds()/3600 < 50:
        print(f'other process {test_process.name} is running')
        return
    
    test_process.running = True
    test_process.save()

    while run:
        runtime = timezone.now() - test_process.updated_at

            
        print(f'current runtime: {timezone.now() - start}')
        print(f'current updateat: {runtime} and hour {runtime.total_seconds()/3600} and day {runtime.days} \n')

        if runtime.total_seconds()/3600 >= 48:
            run = False
            break

        time.sleep(3600*2)

    test_process.running = False
    test_process.save()

def auto_update_new_data():
    print('update new data')
    update_new_process, _ = BackgroundProcess.objects.get_or_create(name = 'update_new')
    start = timezone.now()
    runtime = timezone.now() - update_new_process.updated_at

    if update_new_process.running == True and runtime.total_seconds()/3600 < AUTO_UPDATE_NEW_TIMEOUT_H + 2:
        print(f'other process {update_new_process.name} is running')
        return
    
    update_new_process.running = True
    update_new_process.save()

    while True:
        runtime = timezone.now() - update_new_process.updated_at

        if runtime.total_seconds()/3600 >= AUTO_UPDATE_NEW_TIMEOUT_H:
            break

        try:
            crawl_update_shopee_categories()
            source_data = SourceData.objects.filter(platform='Shopee', crawled__in=[False])

            # print(len(source_data))
            if len(source_data) == 0:
                crawl_shopee_categories()
            
            autocrawl_shopee_all(update_new_process)
        except Exception as e:
            print(f'auto update new error: {e}')

        time.sleep(3600)
        # for test only
        # break

    update_new_process.running = False
    update_new_process.save()

def auto_update_old_data():
    print('update old data')
    update_old_process, _ = BackgroundProcess.objects.get_or_create(name = 'update_old')
    start = timezone.now()
    runtime = timezone.now() - update_old_process.updated_at

    if update_old_process.running == True and runtime.total_seconds()/3600 < AUTO_UPDATE_OLD_TIMEOUT_H + 2:
        print(f'other process {update_old_process.name} is running')
        return
    
    update_old_process.running = True
    update_old_process.save()

    while True:
        runtime = timezone.now() - update_old_process.updated_at

        if runtime.total_seconds()/3600 >= AUTO_UPDATE_OLD_TIMEOUT_H:
            break

        try:
            
            shopee_autorecrawl_product(update_old_process)

        except Exception as e:
            print(f'auto update new error: {e}')

        time.sleep(3 * 3600)
        # for test only
        # break

    update_old_process.running = False
    update_old_process.save()
    

# """get random product"""
# scheduler.add_job(get_random_product, 'interval', minutes=10)
# scheduler.add_job(get_random_product, 'interval', seconds=2,
#                   end_date=timezone.now()+datetime.timedelta(0, 3))

# """cleanup temp folder"""
# scheduler.add_job(cleanup_temp_folder, 'interval', minutes=10)

# """test auto update data"""
# scheduler.add_job(test, 'interval', seconds=2, end_date=timezone.now()+datetime.timedelta(0, 3))
# scheduler.add_job(test, 'interval', days=1)

# """auto update new data"""
# scheduler.add_job(auto_update_new_data, 'interval', hours=12)

# """auto update old data"""
# scheduler.add_job(auto_update_new_data, 'interval', hours=12)

scheduler.start()
