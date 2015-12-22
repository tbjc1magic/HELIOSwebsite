from polls.models import Question, Choice
from django.utils import timezone
import datetime


q1 = Question(question_text="tt",pub_date=timezone.now())
q1.save()
q1.choice_set.create(choice_text='fdsaf',votes=1)
q1.was_published_recently()
q1.delete()
len(Question.objects.all())

q = Question.objects.get(pk=1)

q.choice_set.all()
c=q.choice_set.create(choice_text = 'just fdsa', votes=0)
c.question
q.choice_set.all()

Choice.objects.all()
kk=len(Choice.objects.all())-1

print "key number", c.id,kk
c1  = q.choice_set.get(pk=kk)
print c1
c1.delete()

for sc in Choice.objects.all():
    print sc.choice_text,sc.id



