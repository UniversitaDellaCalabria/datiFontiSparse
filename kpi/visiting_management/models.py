from django.contrib.auth import get_user_model
from django.db import models

from organizational_area.models import OrganizationalStructure


class Role(models.Model):
    role_type = models.CharField(max_length=256)

    def __str__(self):
        return '{}'.format(self.role_type)


class Collaboration(models.Model):
    collab_type = models.CharField(max_length=256)

    def __str__(self):
        return '{}'.format(self.collab_type)


class Visiting(models.Model):
    visitor = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    from_structure = models.ForeignKey(
        OrganizationalStructure, on_delete=models.PROTECT, related_name='from_structure')
    to_structure = models.ForeignKey(
        OrganizationalStructure, on_delete=models.PROTECT, related_name='to_structure')
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    mission = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    didactic_hour = models.PositiveIntegerField()
    effective_days = models.PositiveIntegerField()
    note = models.TextField(blank=True, default='')

    def __str__(self):
        return '{}-{}-{}'.format(self.visitor, self.from_structure, self.to_structure)


class VisitingCollaboration(models.Model):
    visiting = models.ForeignKey(Visiting, on_delete=models.CASCADE)
    collab = models.ForeignKey(Collaboration, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('visiting', 'collab')
