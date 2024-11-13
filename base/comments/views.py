from django.contrib.admin.templatetags.admin_list import pagination
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render, redirect

from comments.forms import AddCommentForm
from comments.models import Comment


# Create your views here.
def comments_view(request):
    all_comments = Comment.objects.all().order_by('-time_created')
    paginator = Paginator(all_comments, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'comments/comments.html', {'page_obj' : page_obj})

def handle_uploaded_file(f):
    if f is None:
        return
    with open(f'media/{f.name}', "wb+") as destination:
        for chunck in f.chunks():
            destination.write(chunck)

def comments_form(request: HttpRequest):
    if request.method == 'POST':
        form = AddCommentForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['attachment'])
            form.save()
            return redirect('comments')
    else:
        form = AddCommentForm()

    return render(request, 'comments/add_comment.html', {'form' : form})

