from .utils import *


def get_similar_products_multithread(anchor_product, anchor_images):
    compare_products = get_similar_product_category(anchor_product)
    quantity = len(compare_products)
    result = {}

    total_thread = os.cpu_count() * 8
    threads = []
    for thread_num in range(total_thread):
        temp_list = []
        result[f'{thread_num}'] = temp_list
        threads.append(PropagatingThread(
            target=get_similar_products_thread, args=(anchor_images, compare_products[
                int(quantity/total_thread * thread_num):
                int(quantity/total_thread * (thread_num + 1))
            ], temp_list,)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    all_result = []
    for key in result:
        print(key)
        all_result.extend(result[key])
    
    all_result = sorted(all_result, key=lambda d: d['euclidean_distance'], reverse=False)
    max_len = min(300, len(all_result))
    return all_result[:max_len]


def get_similar_products_thread(anchor_images, test_products, temp_list):
    quantiy = len(test_products)
    count = 0
    for test_product in test_products:
        count+=1
        print(f'{count}/{quantiy}')
        temp_list.append(calculate_best_similar_product(
            anchor_images, test_product))
    return temp_list


def get_similar_product_category(anchor_product):
    category_products = Product.objects.filter(
        category=anchor_product.category)
    print(len(category_products))
    return category_products


def calculate_best_similar_product(anchor_images, test_product):
    best_similar = {"euclidean_distance": float(
        'inf'), "cosine_distance": 0}
    for anchor_image in anchor_images:
        for test_image in test_product.images.all():
            try:
                distance = calculate_similar_image(anchor_image, test_image)
                # print("check", distance)
                if distance["euclidean_distance"] < best_similar["euclidean_distance"] or distance["cosine_distance"] > best_similar["cosine_distance"]:
                    # print("new best", distance, best_similar)
                    best_similar = distance
                # print('\n')
            except Exception as e:
                print(f"calculate best distance error {e}")

    best_similar['product_comapre'] = ProductSearchSerializer(test_product).data
    return best_similar


def calculate_similar_image(anchor_image, test_image):
    anchor_embedding = np.asarray(anchor_image.embedding_vector)
    test_embedding = np.asarray(test_image.embedding_vector)

    euclidean_distance = tf.math.reduce_euclidean_norm(
        anchor_embedding - test_embedding, axis=1).numpy()

    anchor_embedding = normalize(anchor_embedding, axis=1)
    test_embedding = normalize(test_embedding, axis=1)
    cosine_distance = cosine_similarity(anchor_embedding, test_embedding)

    return {"euclidean_distance": euclidean_distance[0], "cosine_distance": cosine_distance[0][0], 'anchor_image': anchor_image.id, "test_image": ImageSerializer(test_image).data}
