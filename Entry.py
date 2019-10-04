from django.shortcuts import render

def index(request):
    submitbutton = request.POST.get('Submit')

    if submitbutton:
        print("Hello")

    context = {'submitbutton': submitbutton}

    return render(request, 'Articles/index.html', context)