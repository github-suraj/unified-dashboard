from django.shortcuts import render

def homepage(request):
    return render(request, 'base.html')

def handle_404(request, exception):
    context = {'err_code': 404, 'err_type': 'Page not found'}
    return render(request, 'errors.html', context)

def handle_500(request):
    context = {'err_code': 500, 'err_type': 'Internal Server Error'}
    return render(request, 'errors.html', context)
