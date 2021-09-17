from django.db.models.signals import m2m_changed, post_save, pre_delete
from django.dispatch import receiver
from tasks.models import TodoItem, Category
from collections import Counter
from django.core.cache import cache



@receiver(post_save, sender=TodoItem)
def task_priority(sender=None, instance=None, **kwargs):
    # print(instance, instance.priority, f' Kwargs: {kwargs}')
    counter = {"High": 0, "Medium": 0, "Low": 0}
    for task in TodoItem.objects.all():
        if task.priority  == 1:
            counter["High"] += 1
        elif task.priority == 2:
            counter["Medium"] += 1
        else:
            counter["Low"] += 1
    # for key, value in counter.items():
    cache.set_many(counter, 60*60)
    print("Priority1", cache.get("High"), "Priority2", cache.get("Medium"), "Priority3", cache.get("Low"))


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats(sender, instance, action, model, **kwargs):
    print(instance, action, f' Kwargs: {kwargs}')
    for cat in instance.category.all():
        slug = cat.slug

        if action == "post_add":

            new_count = int(cat.todos_count) + 1
            print(10 * "+")

        elif action == "pre_remove":
            new_count = int(cat.todos_count) - 1
            print(10 * "-")
        else:
            return
        Category.objects.filter(slug=slug).update(todos_count = new_count)

@receiver(pre_delete, sender=TodoItem)
def del_task(sender=None, instance=None, **kwargs):
    print("pre_delete", instance)
    task_cats(sender, instance, action="pre_remove", model=TodoItem, **kwargs)
