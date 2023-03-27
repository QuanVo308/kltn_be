from .utils import *


def get_similar_product_category(anchor_product):
    category_products = Product.objects.filter(
        category=anchor_product.category)
    print(len(category_products))


def calculate_best_similar_product(anchor_product, test_product):
    best_similar = {"euclidean_distance": float(
        'inf'), "cosine_distance": 0}
    for anchor_image in anchor_product.images.all():
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

    return best_similar


def calculate_similar_image(anchor_image, test_image):
    anchor_embedding = np.asarray(anchor_image.embedding_vector)
    test_embedding = np.asarray(test_image.embedding_vector)

    euclidean_distance = tf.math.reduce_euclidean_norm(
        anchor_embedding - test_embedding, axis=1).numpy()

    anchor_embedding = normalize(anchor_embedding, axis=1)
    test_embedding = normalize(test_embedding, axis=1)
    cosine_distance = cosine_similarity(anchor_embedding, test_embedding)

    return {"euclidean_distance": euclidean_distance[0], "cosine_distance": cosine_distance[0][0], 'anchor_image': anchor_image.id, "test_image": test_image.id}
