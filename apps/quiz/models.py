from django.db import models

# Create your models here.
class Quiz(models.Model):
    TYPE_CHOICES = [
        ("ai", "AI"),
        ("manual", "Manual")
    ]

    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=True)
    description = models.TextField(null=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ["updated_at", "title"]
    
class Question(models.Model):
    TYPE_CHOICES = [
        ("multiple_choice", "Multiple Choice"),
        ("true_or_false", "True or False"),
        ("essay", "Essay"),
        ("fill_in_the_blank", "Fill in the blanks")
    ]

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("moderate", "Moderate"),
        ("hard", "Hard"),
    ]

    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    question = models.TextField()
    points = models.IntegerField()
    type = models.CharField(choices=TYPE_CHOICES, null=True)
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, null=False)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title
    
class Answer(models.Model):

    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)