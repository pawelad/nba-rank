import random


def get_two_random(model):
    """
    Get two random instances of passed model
    :type model: Django's `db.Model`
    """
    last = model.objects.count() - 1

    index1, index2 = random.sample(range(0, last), 2)

    all_objects = model.objects.all()
    object1 = all_objects[index1]
    object2 = all_objects[index2]

    return object1, object2
