from .scheduler_jobs import *
from .serializers import *
from .utils import *
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


scheduler.add_job(get_random_product, 'interval', minutes=3)
scheduler.add_job(get_random_product, 'interval', seconds=2,
                  end_date=timezone.now()+datetime.timedelta(0, 3))
scheduler.start()
