from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from app.forms import MergeForm, SplitForm
from django.contrib import messages


def merge(request):
    if request.method == 'POST':
        merge_form = MergeForm(request.POST, request.FILES)
        if merge_form.is_valid():
            pdf_files = request.FILES.getlist('pdf')

            # merge
            out_file = PdfFileMerger()
            for pdf in pdf_files:
                out_file.append(pdf)

            with open('merged.pdf', 'wb') as output_stream:
                out_file.write(output_stream)
            messages.success(request, 'done successfully')
            return redirect(reverse_lazy('app:merge'))
    else:
        merge_form = MergeForm()

    context = {
        'upload_pdf_form': merge_form
    }
    return render(request, 'app/merge.html', context)


def split(request):
    if request.method == 'POST':
        split_form = SplitForm(request.POST, request.FILES)
        if split_form.is_valid():
            pdf = split_form.cleaned_data.get('pdf')

            numbers_array = request.POST['array']
            numbers_array = numbers_array.replace('[', '').replace(']', '').replace('(', '').replace(')', '').split(',')

            # split
            input_pdf = PdfFileReader(pdf)

            for i in range(0, int(len(numbers_array) / 2)):
                output_pdf = PdfFileWriter()

                a = int(numbers_array[2 * i]) - 1
                b = int(numbers_array[2 * i + 1])

                for j in range(a, b):
                    output_pdf.addPage(input_pdf.getPage(j))

                with open(f'{i}.pdf', 'wb') as out:
                    output_pdf.write(out)

        messages.success(request, 'done successfully')
        return redirect(reverse_lazy('app:split'))

    else:
        split_form = SplitForm()

    context = {
        'upload_pdf_form': split_form
    }
    return render(request, 'app/split.html', context)
