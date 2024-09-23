from django.db import models
from django import forms


# class github_dataset(models.Model):
#     repositories = models.CharField(max_length=600)
#     stars_count = models.IntegerField()
#     forks_count = models.IntegerField()
#     issues_count = models.IntegerField()
#     pull_requests = models.IntegerField()
#     contributors = models.IntegerField()
#     language = models.CharField(max_length=600)
#     description = models.CharField(max_length=600)
#     score = models.IntegerField()

#     class Meta:
#         db_table = 'github_dataset'

# class CV(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     education = models.TextField()
#     experience = models.TextField()
#     skills = models.TextField()

#     db_table = 'CV'
    
# class users_dataset(models.Model):
#     repositories_count = models.CharField(max_length=600)
#     stars_count = models.IntegerField(max_length=600)
#     forks_count = models.IntegerField(max_length=600)
#     watchers = models.IntegerField(max_length=600)
#     pull_requests = models.IntegerField(max_length=600)
#     contributors = models.IntegerField(max_length=600)
#     issues_count= models.IntegerField(max_length=200)
#     bio = models.TextField(max_length=400)

#     class Meta:
#         db_table = 'users_dataset'

# class repo_dataset(models.Model):
#     repo_name = models.CharField(max_length=300)

#     class Meta:
#         db_table = 'repo_dataset'

class gitusername_dataset(models.Model):
    username = models.CharField(max_length=100)
    gitusername = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'gitusername_dataset'
        

    
class gitreponame_dataset(models.Model):
    username = models.CharField(max_length=100)
    repositories = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'gitreponame_dataset'

class gitrepodetail_dataset(models.Model):
    username = models.CharField(max_length=100)
    repositories = models.CharField(max_length=100)
    stars_count = models.IntegerField()
    forks_count = models.IntegerField()
    pull_requests = models.IntegerField()
    contributors = models.IntegerField()
    language = models.TextField(max_length=300)
    description = models.TextField(max_length=100)
    topics = models.TextField(max_length=100)
    
    class Meta:
        db_table = 'gitrepodetail_dataset'
        
class gituserall_dataset(models.Model):
    username = models.CharField(max_length=100)
    stars_count = models.IntegerField()
    forks_count = models.IntegerField()
    pull_requests = models.IntegerField()
    contributors = models.IntegerField()
    language = models.TextField(max_length=300)
    description = models.TextField(max_length=100)
    topics = models.TextField(max_length=100)
    
    class Meta:
        db_table = 'gituserall_dataset'
        
        
        
        
class Job(models.Model):
    CATEGORY_CHOICES = [
        ('webdev', 'Web Development'),
        ('ml', 'Machine Learning'),
        ('uiux', 'UI/UX Development'),
        ('iot', 'Internet of Things'),
        ('blockchain', 'Blockchain Technology'),
        ('cybersec', 'Cybersecurity'),
        ('cloud', 'Cloud Computing'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='job_images/', blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'category', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control p-0 ps-2'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }