import random


def get_two_random(qs):
    """
    Get two random instances of passed queryset
    :type qs: Django's `Queryset`
    """
    random.seed()
    index1, index2 = random.sample(range(0, qs.count()), 2)

    all_objects = qs.all().order_by('pk')
    object1 = all_objects[index1]
    object2 = all_objects[index2]

    return object1, object2
