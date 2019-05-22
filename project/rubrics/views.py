# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import *

from .forms import *

from django.shortcuts import render, redirect

# Create your views here.


def rubrics_list(request):
    if request.POST:
        data = request.POST
        name = data['name']
        mi = data['dur_min']
        ma = data['dur_max']
        rubric = Rubric.objects.all()
        create = True
        for r in rubric:
            if r.name == name:
                create = False
        if create:
            ru = Rubric.objects.create(name=name, duration_min=mi, duration_max=ma, state=False)
            ru.save()

    rubrics = Rubric.objects.all()
    return render(request,'rubrics/rubrics_list.html', {'rubrics': rubrics})


def create_rubric(request):
    form = RubricForm()
    return render(request, 'rubrics/rubrics_create.html', {'form': form})


