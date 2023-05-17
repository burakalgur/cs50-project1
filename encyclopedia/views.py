from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse


from . import util
from . import form


def index(request):
    if request.method == 'POST':
        entries = util.list_entries()
        query = request.POST['q']
        if query in entries:
            return entry(request, query)
        else:
            filtered_entries = []
            for e in entries:
                if query in e:
                    filtered_entries.append(e)
            return render(request, "encyclopedia/index.html", {
            "entries": filtered_entries })


    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html = util.markdown_to_html(title)
    return render(request, "encyclopedia/entry.html", {"entry": html, "title": title})

def new(request):
    if(request.method == 'POST'):
        newForm = form.CreateForm(request.POST)
        if newForm.is_valid():
            title = newForm.cleaned_data["title"]
            content = newForm.cleaned_data["content"]
            isSuccess = util.save_entry(title, content)
            if isSuccess:
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
            else:
                return render(request, "encyclopedia/new.html", {
                    "err": "Page couldn't created"
                })

        else:
            return render(request, "encyclopedia/new.html", {
                "form" : newForm
            })



    return render(request, "encyclopedia/new.html", {
        "form": form.CreateForm()
    })

def edit(request, title):
    if request.method == 'POST':
        newForm = form.EditForm(request.POST, initial_content=util.get_entry(title))
        if newForm.is_valid():
            content = newForm.cleaned_data['content']
            isSuccess = util.change_entry(title, content)
            if isSuccess:
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
            else:
                return render(request, "encyclopedia/new.html", {
                    "err": "Page couldn't created"
                })
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": newForm,
                "title": title
            })
    else:
        newForm = form.EditForm( initial_content=util.get_entry(title))
        return render(request, "encyclopedia/edit.html", {
            "form": newForm,
            "title": title
        })


def random(request):
    randomPageTitle = util.get_random_page()
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[randomPageTitle]))