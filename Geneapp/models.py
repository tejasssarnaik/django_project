from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=30, unique=True)
    institute_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    login_time = models.DateTimeField(null=True, blank=True)
    # You don't need to store the password in the UserProfile model because it's stored in the User model.

    def __str__(self):
        return self.full_name
    




class Workflow(models.Model):
    Workflow_name = models.CharField(max_length=255)
    Configuration = models.CharField(max_length=255)
    Samples = models.IntegerField()
    reference_genome = models.CharField(max_length=255) 
    Creation = models.DateTimeField()
    Status = models.CharField(max_length=50)
    Workflow_ID = models.CharField(max_length=10)
    sample_id = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.Configuration} - workflow ID: {self.Workflow_ID}'







class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.id}: {self.name}"



class UserHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    workflow_id = models.IntegerField()
    task_performance_time = models.DateTimeField()
    workflow_submission_time = models.DateTimeField()
    workflow_type = models.CharField(max_length=255)
    workflow_name = models.CharField(max_length=255)
    samples = models.IntegerField()
    reference_genome = models.CharField(max_length=255) 
    status = models.CharField(max_length=255)
    last_status = models.CharField(max_length=255, null=True, blank=True)
    sample_id = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.full_name} - {self.task_performance_time}'


from django.db import models

class IDCounter(models.Model):
    
    workflow_id = models.IntegerField(default=0)

    def increment_workflow_id(self):
        self.workflow_id += 1
        self.save()
        return self.workflow_id





    


