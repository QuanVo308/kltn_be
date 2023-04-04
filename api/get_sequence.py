from .scheduler_jobs import *
from .serializers import *
from .utils import *
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()


# scheduler.add_job(FirstCronTest, 'interval', seconds=1)
RANDOM_PRODUCTS_SERIALIZER = []


def get_sequence_all():
    product = Product.objects.all().latest('id')
    image = Image.objects.all().latest('id')
    category = Category.objects.all().latest('id')
    source_data = SourceData.objects.all().latest('id')


def get_random_product_serializer():
    products = RANDOM_PRODUCTS_SERIALIZER
    return products


# scheduler.add_job(get_random_product, 'interval', minutes=10)
# scheduler.add_job(get_random_product, 'interval', seconds=2,
#                   end_date=timezone.now()+datetime.timedelta(0, 3))
scheduler.start()
