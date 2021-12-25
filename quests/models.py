from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin


class ProfileTest(models.Model):
    name_test = models.CharField(max_length=150, verbose_name="Название теста")
    questions_count = models.IntegerField(blank=True, verbose_name="Сколько вопросов в тесте?")

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.name_test


class Question(models.Model):
    ProfileId = models.ForeignKey(ProfileTest, on_delete=models.CASCADE, verbose_name='Тест')
    Title = models.CharField(max_length=300, verbose_name="Название")
    Content = models.TextField(blank=True, verbose_name="Описание")
    QuesType = models.IntegerField(blank=True, verbose_name="Тип вопроса", default=0)
    Audio = models.FileField(blank=True, verbose_name="Аудиозапись")

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.Title


class Comment(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    text = models.TextField(max_length=1000, blank=False)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Answer(models.Model):
    QuestionID = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    Answer = models.CharField(max_length=200, blank=True, verbose_name="Ответ")
    IsRight = models.BooleanField(blank=True, verbose_name="Правильный?")
    DescriptionForAnswer = models.TextField(max_length=100, blank=True, verbose_name="Описание к ответу")

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    def __str__(self):
        return self.Answer


class Result(models.Model):
    ProfileId = models.ForeignKey(ProfileTest, on_delete=models.CASCADE, verbose_name='Тест')
    UserName = models.CharField(max_length=300, verbose_name="ФИО")
    Rating = models.FloatField(verbose_name="Проценты")

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'


class Responds(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    QuestionID = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    Answer = models.TextField(verbose_name="Ответ")
    VideoAnswer = models.FileField(blank=True, upload_to="videos/answers/",verbose_name="Видео")

    class Meta:
        unique_together = 'UserId', 'QuestionID'
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'

    def __str__(self):
        return self.Answer


class IsPassedTest(models.Model):
    TestID = models.ForeignKey(ProfileTest, on_delete=models.CASCADE, verbose_name='Тест')
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    IsPassed = models.BooleanField(default=False, verbose_name='Пройден ли тест')


class QuestionsInline(admin.TabularInline):
    model = Answer


@admin.register(Question)
class BookAdmin(admin.ModelAdmin):
    inlines = [QuestionsInline]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display=("ProfileId", "UserName", "Rating")

    def has_add_permission(self, request):
        return False