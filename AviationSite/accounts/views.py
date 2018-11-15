from django.shortcuts import render


# Create your views here.
def home(request):
    # numbers = [1, 2, 3, 4, 5]
    # name = 'Marley Chinn'
    # args = {'myName': name, 'numbers': numbers}
    return render(request, 'accounts/home.html')

