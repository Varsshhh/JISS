from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import View
from django.views.generic import View
from registrar.models import courtcases
from .forms import resolved_case_details,resolved_case_details_keyword
from django.db.models import Q
from homepage.models import User


# from django.views.generic.list import ListView
# from django.utils import timezone

def lawyer(request):
    template = loader.get_template('lawyer.html')
    return HttpResponse(template.render())

class pastcase(View):
    form_class = resolved_case_details
    template_name = 'lawyer/resolved_case_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        template = 'searched_case.html'
        if form.is_valid():
            temp = form.cleaned_data['cin']
            cases = courtcases.objects.all().filter(cin = temp)
            
            if len(cases) == 0:
             # handle empty queryset here
                return render(request,'searched_case.html', {'form': form,'error_message':True})
            # if cases:
            #     lawyer_user=User.objects.get(pk=request.user.id+1)
            #     current_user=User.objects.get(username=str(lawyer_user), credits=lawyer_user())
            #     # current_user.credits+=5
            #     # current_user.save()
            
            # context = {
            #         'object_list': cases,
            #         'due_credits':current_user(),
            #         'username':str(current_user),
            #     }
           # return render(request,template,context)

            context = {
                'object_list':cases
            }
            return render(request,template,context) 

        return render(request, self.template_name, {'form': form})

class keyword(View):
    form_class = resolved_case_details_keyword
    template_name = 'lawyer/resolved_case_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        template = 'searched_case.html'
        if form.is_valid():
            temp = form.cleaned_data['keyword']
            
            qs = Q(defendant_address__icontains=temp) | Q(crimetype__icontains=temp)|  Q(presiding_judge__icontains=temp)| Q(public_prosecuter__icontains=temp)| Q(lawyer__icontains=temp)| Q(judgement_summary__icontains=temp)  | Q(defendant__icontains=temp) 
            cases = courtcases.objects.filter(qs)
            # cases = courtcases.objects.filter(cin=temp)

            if len(cases) == 0:
             # handle empty queryset here
                return render(request,'searched_case.html', {'form': form,'error_message':True})
            
            context = {
                'object_list':cases
            }
            return render(request,template,context)

        return render(request, self.template_name, {'form': form})

        
