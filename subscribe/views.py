from django.shortcuts import render

# Create your views here.

from .models import SubscribeList
from django.shortcuts import redirect, get_object_or_404



def add_to_sublist_view(request):
    if request.method == 'POST':
        if not SubscribeList.objects.filter(email = request.POST['email']).exists():
            obj = SubscribeList.objects.create(email = request.POST['email'])

        return render(request, 'add_sublist_done.html', {'email': request.POST['email']})
    else:
        return redirect('home')



