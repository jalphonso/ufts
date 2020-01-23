from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.core.files.storage import FileSystemStorage
from .forms import BookForm
from .models import Book


class Home(TemplateView):
    template_name = 'home.html'


def upload_dayone(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)

        context['url'] = fs.url(name)
    return render(request, 'dayone/upload.html', context)


def book_list(request):
    books = Book.objects.all()

    return render(request, 'dayone/book_list.html', {
        'books': books
    })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'dayone/upload_book.html', {
        'form': form
    })


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')
