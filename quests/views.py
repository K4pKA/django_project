from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormMixin, CreateView, DeleteView
from .models import ProfileTest, Question, Responds, Answer, Comment, IsPassedTest
from django.views.generic import DetailView, ListView
from .forms import RespondTestForm, LoginUserForm, RegisterUserForm, CommentForm, IsPassedForm
from django.contrib.auth import logout, login


class CommDeleteView(DeleteView, FormMixin):
    model = Comment
    success_url = '/about'
    template_name = 'quests/delete.html'


class IndexView(ListView):
    model = IsPassedTest
    template_name = 'quests/index.html'

    def get(self, request, *args, **kwargs):
        IsPassed = IsPassedTest.objects.all()
        test1 = False
        for item in IsPassed:
            if item.UserID == request.user:
                if item.TestID.id == 1:
                    test1 = True
        return render(request, self.template_name, {'data': test1})


class TestsView(ListView, FormMixin):
    model = IsPassedTest
    template_name = 'quests/quests.html'

    def get(self, request, *args, **kwargs):
        IsPassed = IsPassedTest.objects.all()
        test1 = list()
        test2 = list()
        test3 = list()
        test4 = list()
        for item in IsPassed:
            if item.UserID.id == request.user.id:
                if item.TestID.id == 1:
                    test1 = [item.TestID.id, item.UserID.id, item.IsPassed]
                elif item.TestID.id == 2:
                    test2 = [item.TestID.id, item.UserID.id, item.IsPassed]
                elif item.TestID.id == 3:
                    test3 = [item.TestID.id, item.UserID.id, item.IsPassed]
                elif item.TestID.id == 4:
                    test4 = [item.TestID.id, item.UserID.id, item.IsPassed]
        return render(request, self.template_name, {'test1': test1, 'test2': test2, 'test3': test3, 'test4': test4})


class IsTestProcessed(ListView, FormMixin):
    model = IsPassedTest
    success_url = 'result'
    template_name = 'quests/unprocessed.html'
    form_class = IsPassedForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        test = ProfileTest.objects.all()
        PK = self.kwargs['pk']
        return render(request, self.template_name, {'form': form, 'test': test, 'PK': PK})

    def post(self, request, *args, **kwargs):
        post = dict(request.POST)
        b = 0
        PK = self.kwargs['pk']
        for i in post["csrfmiddlewaretoken"]:
            new_dict_for_form = {
                "csrfmiddlewaretoken": i,
                "TestID": post["TestID"][b],
                "UserID": post["UserID"][b],
                "IsPassed": post["IsPassed"][b]
            }
            b += 1
            form = self.form_class(new_dict_for_form)
            if form.is_valid():
                form.save()
                return redirect('result', pk=PK)
            else:
                return redirect('home')


class RegisterUser(CreateView, FormMixin):
    form_class = RegisterUserForm
    template_name = 'quests/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView, FormMixin):
    form_class = LoginUserForm
    template_name = 'quests/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class ResultView(ListView, FormMixin):
    model = Answer
    template_name = 'quests/result.html'
    context_object_name = 'item'

    # Handle GET HTTP requests
    def get(self, request, *args, **kwargs):
        test = ProfileTest.objects.all()
        data1 = Answer.objects.all()
        PK = self.kwargs['pk']
        data2 = Responds.objects.all()
        data3 = list()
        for i in test:
            if i.id == PK:
                for q in data2:
                    if q.UserId.id == request.user.id:
                        for p in data1:
                            if p.QuestionID.id == q.QuestionID.id and p.IsRight and p.QuestionID.ProfileId.id == PK:
                                if p.Answer == q.Answer.lower():
                                    data3 += [[p.Answer, q.Answer, True, p.QuestionID.Title]]
                                else:
                                    data3 += [[p.Answer, q.Answer, False, p.QuestionID.Title]]

        return render(request, self.template_name, {'answers': data1,
                                                    'PK': PK,
                                                    'respond': data2,
                                                    'test': test, 'data': data3})


class Quest1ListView(DetailView, FormMixin):
    form_class = RespondTestForm

    model = ProfileTest
    template_name = 'quests/details_view.html'
    context_object_name = 'item'

    # Handle GET HTTP requests
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        answer = Question.objects.all()
        answers = Answer.objects.all()
        PK = self.kwargs['pk']
        Respond = Responds.objects.all()
        IsPassed = IsPassedTest.objects.all()
        test1, test2, test3, test4 = False, False, False, False
        for item in IsPassed:
            if item.UserID == request.user:
                if item.TestID.id == 1:
                    test1 = True
                elif item.TestID.id == 2:
                    test2 = True
                elif item.TestID.id == 3:
                    test3 = True

        return render(request, self.template_name, {'form': form,
                                                    'answer': answer,
                                                    'PK': PK,
                                                    'respond': Respond,
                                                    'answers': answers,
                                                    'test1': test1, 'test2': test2, 'test3': test3, 'test4': test4})

    # Handle POST GTTP requests
    def post(self, request, *args, **kwargs):
        post = dict(request.POST)
        b = 0
        PK = self.kwargs['pk']
        for i in post["csrfmiddlewaretoken"]:
            new_dict_for_form = {
                "csrfmiddlewaretoken": i,
                "QuestionID": post["QuestionID"][b],
                "UserId": post["UserId"][b],
                "Answer": post["Answer"][b],
            }
            b += 1
            form = self.form_class(new_dict_for_form)
            if form.is_valid():
                form.save()
        return redirect('redirect_to_result', pk=PK)


class AboutView(ListView, FormMixin):
    form_class = CommentForm
    model = Comment
    template_name = 'quests/about.html'
    context_object_name = 'item'

    # Handle GET HTTP requests
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        mod = Comment.objects.all().order_by('-id')[:10]
        mod1 = Comment.objects.all().order_by('-id')
        return render(request, self.template_name, {'form': form, 'mod': mod, 'for_admin': mod1})

    # Handle POST GTTP requests
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/about')


def help(request):
    return render(request, 'quests/help.html')


def logout_user(request):
    logout(request)
    return redirect('home')
