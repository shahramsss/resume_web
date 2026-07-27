from django.db import models

class Technology(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    github_link = models.URLField(blank=True, null=True)
    demo_link = models.URLField(blank=True, null=True)

    technologies = models.ManyToManyField(Technology)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="projects/")
    alt = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.project.title}"

