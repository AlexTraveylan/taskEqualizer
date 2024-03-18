from tasks_api.family.models import Family
from tasks_api.invitation.models import Invitation
from tasks_api.member.models import Member
from tasks_api.possibles_task.models import PossibleTask
from tasks_api.task.models import Task

if __name__ == "__main__":
    print("Family")
    print(Family.objects.all())
    print("Invitation")
    print(Invitation.objects.all())
    print("Member")
    print(Member.objects.all())
    print("PossibleTask")
    print(PossibleTask.objects.all())
    print("Task")
    print(Task.objects.all())
