from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

import logging

from .forms import InquiryForm, DiaryCreateForm
from .models import Diary
# Create your views here.

logger = logging.getLogger(__name__)


class TopPageView(generic.TemplateView):

    template_name = 'diary/top_page.html'


class InquiryView(generic.FormView):

    template_name = 'diary/inquiry.html'
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        name = form.cleaned_data['name']
        logger.info(f'Inquiry sent by {name}')
        return super().form_valid(form)


class DiaryListView(generic.ListView):

    model = Diary
    template_name = 'diary/diary_list.html'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return queryset


class DiaryDetailView(generic.DetailView):

    model = Diary
    template_name = 'diary/diary_detail.html'


class DiaryCreateView(generic.CreateView):

    model = Diary
    template_name = 'diary/diary_create.html'
    form_class = DiaryCreateForm
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '日記の作成に失敗しました。')
        return super().form_invalid(form)


class DiaryUpdateView(LoginRequiredMixin, generic.UpdateView):

    model = Diary
    template_name = 'diary/diary_update.html'
    form_class = DiaryCreateForm

    def get_success_url(self):
        return reverse_lazy('diary:diary_detail', kwargs={'pk':self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '日記の更新に失敗しました。')
        return super().form_invalid(form)


class DiaryDeleteView(LoginRequiredMixin, generic.DeleteView):

    model = Diary
    template_name = 'diary/diary_delete.html'
    success_url = reverse_lazy('diary:diary_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '日記を削除しました。')
        return super().delete(request, *args, **kwargs)



