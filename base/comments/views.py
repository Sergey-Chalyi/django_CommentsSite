from django.contrib.admin.templatetags.admin_list import pagination
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render, redirect
from comments.forms import AddCommentForm
from comments.models import Comment


def comments_view(request):
    """
    This function handles the display of comments in a paginated manner, with sorting and filtering options.

    Parameters:
    request (HttpRequest): The incoming HTTP request object. It contains information about the client and the request.

    Returns:
    render: A render object that renders the 'comments/comments.html' template with the paginated comments.
    """
    sort_by = request.GET.get('sort_by', 'time_created')  # default sorting field
    order = request.GET.get('order', 'desc')  # default sorting order

    if order == 'asc':
        order_by = f"{sort_by}"
    else:
        order_by = f"-{sort_by}"

    all_comments = Comment.objects.all().order_by(order_by)

    # Create a Paginator object to handle pagination of the comments
    paginator = Paginator(all_comments, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'comments/comments.html', {'page_obj' : page_obj})


def handle_uploaded_file(f):
    """
    This function handles the upload of a file and saves it to the 'media' directory.

    Parameters:
    f (File): The uploaded file object. It contains information about the file, such as its name and content.

    Returns:
    None: This function does not return any value. It saves the uploaded file to the 'media' directory.
    """
    if f is None:
        return

    # loading in parts
    with open(f'media/{f.name}', "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def comments_form(request: HttpRequest) -> render:
    """
    This function handles the display of a form for adding comments, including file attachments.
    It processes POST requests to save the form data and redirect to the comments page,
    or renders the form for GET requests.

    Parameters:
    request (HttpRequest): The incoming HTTP request object. It contains information about the client and the request.

    Returns:
    render: A render object that renders the 'comments/add_comment.html' template with the form.
    If the form is valid and the request method is POST, it redirects to the 'comments' URL.
    """
    if request.method == 'POST':
        form = AddCommentForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['attachment'])
            form.save()
            return redirect('comments')
    else:
        form = AddCommentForm()

    return render(request, 'comments/add_comment.html', {'form' : form})

