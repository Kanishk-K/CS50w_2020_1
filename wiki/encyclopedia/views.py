from django.shortcuts import render, Http404,redirect

from . import util
import markdown2
import random


def index(request):
    #Send a list of all entries and a random entry.
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "random": random.choice(util.list_entries())
    })
def entry(request,selection):
    #Send data about the selected entry in html format.
    if util.get_entry(selection) != None:
        context = {
            "selection":selection,
            "data":markdown2.markdown(util.get_entry(selection)),
            "random": random.choice(util.list_entries())
        }
        return render(request,"encyclopedia/entry.html",context)
    else:
        raise Http404(request,f"a page for {selection} does not exist.")

def search(request):
    query = request.POST.get("q")
    print(query)
    #If the entry exists send person to the entry, else show them possible options
    if util.get_entry(query) != None:
        return redirect('entry',selection=query)
    else:
        context = {
            "similar":[entry for entry in util.list_entries() if query.lower() in entry.lower()],
            "random": random.choice(util.list_entries())
        }
        return render(request,"encyclopedia/search.html",context)
def edit(request,selection):
    #If the user has submitted a change, update it, else display the current page in markdown format.
    if request.method == "POST":
        util.save_entry(selection,request.POST.get("data"))
        return redirect('entry',selection=selection)
    else:
        if util.get_entry(selection) != None:
            context = {
                "selection":selection,
                "data":util.get_entry(selection),
                "random": random.choice(util.list_entries())
            }
            return render(request,"encyclopedia/edit.html",context)
        else:
            raise Http404(request,f"a page for {selection} does not exist.")
def new(request):
    #If the user submits a new entry, check if the entry exists, else create it. If the user gets the page, submit a creation form.
    if request.method == "POST":
        Name = request.POST.get("name")
        Data = request.POST.get("data")
        if util.get_entry(Name) != None:
            raise Http404(request,f"a page for {Name} already exists")
        else:
            util.save_entry(Name,Data)
            return redirect('entry',selection=Name)
    else:
        return render(request,"encyclopedia/new.html")