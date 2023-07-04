'''
create court case -- done
search pending court case --done
search resolved case over a period  --done
add a hearing date  --done
status of a particular case by cin  --done
update hearings --done
update resolved cases --done

'''
from django.db.models import Q
from django.shortcuts import  render
from django.http import  HttpResponse
from django.template import loader
from django.views.generic.list import ListView
from django.utils import timezone
from .models import courtcases
from django.views import View
from django.views.generic import View
from .forms import search_resolved_cases,create_case,allot_hearing_date,status_of_a_case,hearing_data,resolved_data,create_new

from homepage.models import User


def registrar(request):
        template = loader.get_template('registrar.html')
        return HttpResponse(template.render())

#pending court cases
class pendingcases(ListView):
    model = courtcases
    paginate_by = 100  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

#create new court cases
class casescreate(View):
    form_class = create_case
    template_name = 'registrar/courtcases_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        template = 'case_created.html'
        if form.is_valid():
            case = form.save(commit=False)
            case.save()
            courtcases.objects.filter(pk = case.pk).update(cin = case.pk)
            context = {
                'CIN':case.pk
            }
            return render(request, template, context)
        return render(request, self.template_name, {'form': form})


#searching resolved cases over a period
class resolvedcases(View):
    form_class = search_resolved_cases
    template_name = 'period.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        template = 'resolvedcase.html'
        if form.is_valid():
            object_list1 = courtcases.objects.all().filter(status = False)
            starting_date = form.cleaned_data['starting_date']
            end_date = form.cleaned_data['end_date']
            object_list = object_list1.filter(Q(judgement_date__range=[starting_date, end_date]))

            if len(object_list) == 0:
             # handle empty queryset here
                return render(request,'resolvedcase.html', {'form': form,'error_message':True})
            
            context = {
                'object_list':object_list,
                'start':starting_date,
                'end': end_date
            }

            return render(request, template, context)

        return render(request, self.template_name, {'form': form})

#adding hearing date to a pending case---needs some serious change
class hearings(View):
    form_class = allot_hearing_date
    template_name = 'registrar/hearing_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            temp = form.save()
            temp.save()
            courtcases.objects.filter(pk = temp.cin ).update(hearing_date = temp.date)
            #need change
            return HttpResponse("successs")

        return render(request, self.template_name, {'form': form})
                
#status of a particular case:
class case_status(View):
    form_class = status_of_a_case
    template_name = 'registrar/case_status_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        template = 'registrar/particular_case.html'
        if form.is_valid():
            temp = form.save(commit=False)
            object_list = courtcases.objects.all().filter(cin =temp.cin)

            if len(object_list) == 0:
             # handle empty queryset here
                return render(request,'registrar/particular_case.html', {'form': form,'error_message':True})

            context = {
                'object_list':object_list
            }
            return render(request,'registrar/particular_case.html',context)

#update hearing details:
class update_hearing(View):
    form_class = hearing_data
    template_name = 'registrar/update_hearing_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            temp = form.save(commit=False)
            case = courtcases.objects.filter(cin = temp.cin).count()

            if case > 0:
                temp.save()
                return render(request,'registrar/update_hearing_form.html', {'form': form,'success_message':True})
            
            return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})

#judgement summary update
class case_resolved(View):
    form_class = resolved_data
    template_name = 'registrar/case_resolved_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            temp = form.save(commit= False)
            case = courtcases.objects.filter(cin = temp.cin).count()

            if case > 0:
                courtcases.objects.filter(cin = temp.cin).update(judgement_date = temp.judgement_date)
                courtcases.objects.filter(cin = temp.cin).update(attending_judge = temp.attending_judge)
                courtcases.objects.filter(cin = temp.cin).update(judgement_summary = temp.judgement_summary)
                courtcases.objects.filter(cin = temp.cin).update(status = False)
                return render(request, self.template_name, {'form': form,'success_message':True})
            
            return render(request, self.template_name, {'form': form})
        
        return render(request, self.template_name, {'form': form})
    
class new_lawyer(View):
    form_class = create_new
    template_name = 'registrar/signin_form.html'

    def get(self, request): 
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confitm_password = form.cleaned_data['confirm_password']
            
            new_user = User(username=username,password=password,is_admin=False,is_registrar=False,is_judge=False,is_lawyer=True)
            new_user.save()
            
        template = loader.get_template('registrar.html')
        return HttpResponse(template.render())
            
    
class new_judge(View):
    form_class = create_new
    template_name = 'registrar/signin_form.html'

    def get(self, request): 
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confitm_password = form.cleaned_data['confirm_password']

            
            new_user = User(username=username,password=password,is_admin=False,is_registrar=False,is_judge=True,is_lawyer=False)
            new_user.save()
            
        template = loader.get_template('registrar.html')
        return HttpResponse(template.render())












