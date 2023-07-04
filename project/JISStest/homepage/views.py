#views
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.views import View
from django.views.generic import View
from django.views.generic.list import ListView
from django.utils import timezone
from .forms import get_user
from .models import User

def home(request): 
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render())


def login1(request):
    template = loader.get_template('homepage/login1.html')
    return HttpResponse(template.render())



def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

def help(request):
    template = loader.get_template('help.html')
    return HttpResponse(template.render())

class login(View):
    form_class = get_user
    template_name = 'homepage/signin_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            temp = User.objects.filter(username=username,password=password)
            

            if not temp:
                return render(request, self.template_name, {'form': form,'error_message':True}) 
                
            else:
                for user in temp:
                    if user.is_registrar == True:
                        template = template = loader.get_template('registrar.html')
                        print(user)
                        data={'key':user}
                       
                        return HttpResponse(template.render(data,request))
                    if user.is_lawyer == True:
                        template = template = loader.get_template('lawyer.html')
                        data={'key':user}
                        return HttpResponse(template.render(data,request))
                       
                    if user.is_judge == True:
                        template = template = loader.get_template('judge.html')
                        data={'key':user}
                        return HttpResponse(template.render(data,request))

        return render(request, self.template_name, {'form': form})

