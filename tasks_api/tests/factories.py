from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from tasks_api.ephemeral_task.models import EphemeralTask
from tasks_api.invitation.models import Invitation
from tasks_api.member.models import Member
from tasks_api.models import Family
from tasks_api.possibles_task.models import PossibleTask
from tasks_api.task.models import Task


class FamilyFactory(DjangoModelFactory):
    class Meta:
        model = Family

    family_name = LazyAttribute(lambda o: "Test Family")


class MemberFactory(DjangoModelFactory):
    class Meta:
        model = Member

    member_name = LazyAttribute(lambda o: "Test Member")
    family = SubFactory(FamilyFactory)


class PossibleTaskFactory(DjangoModelFactory):
    class Meta:
        model = PossibleTask

    possible_task_name = LazyAttribute(lambda o: "Test Task")
    description = LazyAttribute(lambda o: "Task description")
    family = SubFactory(FamilyFactory)


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    related_possible_task = SubFactory(PossibleTaskFactory)
    member = SubFactory(MemberFactory)
    duration_in_seconds = LazyAttribute(lambda o: 3600)


class InvitationFactory(DjangoModelFactory):
    class Meta:
        model = Invitation

    code = LazyAttribute(lambda o: "TESTCODE")
    family = SubFactory(FamilyFactory)


class EphemeralTaskFactory(DjangoModelFactory):
    class Meta:
        model = EphemeralTask

    ephemeral_task_name = LazyAttribute(lambda o: "Test Ephemeral Task")
    description = LazyAttribute(lambda o: "Ephemeral Task description")
    value = LazyAttribute(lambda o: 5)
    family = SubFactory(FamilyFactory)
    member = SubFactory(MemberFactory)
