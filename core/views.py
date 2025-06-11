from django.shortcuts import render, get_object_or_404
from .models import Question
from .forms import SubmissionForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User  # Fallback user
import sys
import io
from contextlib import redirect_stdout

def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.question = question

            #  Assign user safely
            if request.user.is_authenticated:
                submission.user = request.user
            else:
                submission.user = User.objects.first()  # fallback for dev

            # Run submitted code and capture output
            f = io.StringIO()
            try:
                with redirect_stdout(f):
                    exec(submission.code, {})
                output = f.getvalue()
            except Exception as e:
                output = str(e)

            submission.result = output[:1000]  # Limit output to 1000 characters
            submission.save()
            return HttpResponseRedirect(reverse('question_detail', args=[question.id]))
    else:
        form = SubmissionForm()

    return render(request, 'core/question_detail.html', {
        'question': question,
        'form': form,
    })

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'core/question_list.html', {'questions': questions})
