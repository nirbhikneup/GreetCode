from django.shortcuts import render, get_object_or_404
from .models import Question, Tag
from .forms import SubmissionForm, CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User  # Fallback user
import sys
import io
from contextlib import redirect_stdout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    output = ''
    is_correct = None
    expected_output = question.expected_output.strip()

    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.question = question

            # Assign user safely
            if request.user.is_authenticated:
                submission.user = request.user
            else:
                submission.user = User.objects.first()  # fallback for dev

            # Run submitted code and capture output
            f = io.StringIO()
            try:
                with redirect_stdout(f):
                    exec(submission.code, {})
                output = f.getvalue().strip()
            except Exception as e:
                output = str(e).strip()

            submission.result = output[:1000]  # Limit output to 1000 characters

            # Compare result with expected_output
            if output == expected_output:
                submission.score = 100  # full score
                is_correct = True
            else:
                submission.score = 0  # wrong answer
                is_correct = False

            submission.save()

    else:
        form = SubmissionForm()

        form = SubmissionForm()
    comment_form = CommentForm()
    comments = question.comments.order_by('-created_at')

    if request.method == 'POST':
        if 'submit_code' in request.POST:
            # (Your existing submission logic here)
            pass
        elif 'submit_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.question = question
                comment.user = request.user
                comment.save()
                return redirect('question_detail', question_id=question.id)

    return render(request, 'core/question_detail.html', {
        'question': question,
        'form': form,
        'output': output,
        'expected_output': expected_output,
        'is_correct': is_correct
    })

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'core/question_list.html', {'questions': questions})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after signup
            return redirect('question_list')  # or wherever you want
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

@login_required
def my_submissions(request):
    user_subs = request.user.submission_set.select_related('question').order_by('-submitted_at')
    return render(request, 'core/my_submissions.html', {'submissions': user_subs})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    submissions = user.submission_set.select_related('question').order_by('-submitted_at')
    total_score = submissions.aggregate(Sum('score'))['score__sum'] or 0

    return render(request, 'core/user_profile.html', {
        'user_profile': user,
        'submissions': submissions,
        'total_score': total_score
    })

def leaderboard_view(request):
    leaderboard = User.objects.annotate(
        total_score=Sum('submission__score')
    ).order_by('-total_score')[:10]  # TOP 10 only

    return render(request, 'core/leaderboard.html', {
        'leaderboard': leaderboard
    })

def questions_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    questions = tag.question_set.all()
    return render(request, 'core/questions_by_tag.html', {
        'tag': tag,
        'questions': questions
    })
