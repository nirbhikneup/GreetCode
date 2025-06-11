from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    DIFFICULTY_LEVELS = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)
    tags = models.CharField(max_length=255, blank=True)  # e.g. "Array, HashMap"
    starter_code = models.TextField(blank=True)
    expected_output = models.TextField(help_text="Expected output for testing")

    def __str__(self):
        return self.title

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=30)
    result = models.TextField(blank=True, null=True)
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.title} - {self.submitted_at}"
