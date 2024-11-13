from django.shortcuts import render

from comments.models import Comment


# Create your views here.
def comments_view(request):
    all_comments = Comment.objects.all()
    return render(request, 'comments/comments.html', {'comments' : all_comments})