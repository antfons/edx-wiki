from django.shortcuts import render
from . import util
import markdown2
from markdown2 import Markdown
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse


class NewPageForm(forms.Form):
    page_title = forms.CharField(
        label="Title",
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'Inform your title page'
            }))
    page_content = forms.CharField(label="Page Content",
    widget=forms.Textarea(
        attrs={
            'style':'resize: none;',
            'class':'form-control',
            "placeholder": "Write your page content"
        }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "h1_title": "All Pages"
    })

def get_title(request, title):
    entries = util.list_entries()
    md = Markdown()
    if title in entries:
        title_body = util.get_entry(title)
        body_text = md.convert(title_body)

        return render(request, "encyclopedia/title.html", {
            "title": title,
            "body": body_text
        })
    return render(request, "encyclopedia/error.html", {
        "error_message": "There is no page with this title"
    })


def search(request):
    entries = util.list_entries()
    md = Markdown()
    title = request.GET["q"]
    if title in entries:
        title_body = util.get_entry(title)
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "body": md.convert(title_body)
        })
    else:
        possible_entries = [entry for entry in entries if title.lower() in entry.lower()]
        if possible_entries:
            return render(request, "encyclopedia/index.html", {
                "entries": possible_entries,
                "h1_title": "Possible pages"
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "error_message": "There is no page for your request"
            })

def add_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            page_t = form.cleaned_data["page_title"]
            page_c = form.cleaned_data["page_content"]
            entries = util.list_entries()
            if page_t in entries:
                return render(request, "encyclopedia/error.html", {
                    "error_message": "entry already exists"
                })
            else:
                util.save_entry(page_t, page_c)
                title = page_t
                title_body = util.get_entry(title)
                md = Markdown()
                return render(request, "encyclopedia/title.html", {
                    "title": title,
                    "body": md.convert(title_body)
                })
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })
    return render(request, "encyclopedia/newpage.html",{
        "form": NewPageForm()
    })


def edit_page(request, title):
    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            page_t = form.cleaned_data["page_title"]
            page_c = form.cleaned_data["page_content"]
            util.save_entry(page_t, page_c)
            title_body = util.get_entry(title)
            md = Markdown()
            return render(request, "encyclopedia/title.html", {
                "title": title,
                "body": md.convert(title_body)
            })            
    else:
        entry_data = util.get_entry(title)
        form_data = {
            "page_title": title,
            "page_content": entry_data
        }
        form = NewPageForm(
            request.POST or None,
            initial=form_data
        )        
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "form": form
        })

def random_page(request):
    title = util.get_random_entry()
    return HttpResponseRedirect(reverse("encyclopedia:title", args=(title,)))
    
