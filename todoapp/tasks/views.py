from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from tasks.models import TodoItem, Category
from datetime import datetime
from django.core.cache import cache
from tasks.signals import task_priority



def index(request):

    from django.db.models import Count

    counts = Category.objects.annotate(total_tasks=Count(
        'todoitem')).order_by("-total_tasks")
    counts = {c.name: c.total_tasks for c in counts}
    send_time = datetime.now()
    
    priority = cache.get_many(["High", "Medium", "Low"])
    print("get_priority", priority)
    if priority == {}:

        task_priority()
        priority = cache.get_many(["High", "Medium", "Low"])
    send_data = {"counts": counts,
                "send_time": send_time,
                "priority": priority}

    return render(request, "tasks/index.html", send_data)


def filter_tasks(tags_by_task):
    return set(sum(tags_by_task, []))


def tasks_by_cat(request, cat_slug=None):
    u = request.user
    tasks = TodoItem.objects.filter(owner=u).all()

    cat = None
    if cat_slug:
        cat = get_object_or_404(Category, slug=cat_slug)
        tasks = tasks.filter(category__in=[cat])

    categories = Category.objects.all()
    # for t in tasks:
    #     for cat in t.category.all():
    #         if cat not in categories:
    #             categories.append(cat)

    return render(
        request,
        "tasks/list_by_cat.html",
        {"category": cat, "tasks": tasks, "categories": categories},
    )


class TaskListView(ListView):
    model = TodoItem
    context_object_name = "tasks"
    template_name = "tasks/list.html"

    def get_queryset(self):
        u = self.request.user
        qs = super().get_queryset()
        return qs.filter(owner=u)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_tasks = self.get_queryset()
        tags = []
        for t in user_tasks:
            tags.append(list(t.category.all()))

            categories = []
            for cat in t.category.all():
                if cat not in categories:
                    categories.append(cat)
            context["categories"] = categories
        context["cats"] = Category.objects.all()
        return context


class TaskCatListView(ListView):
    model = Category
    template_name = "tasks/list.html"


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = "tasks/details.html"
