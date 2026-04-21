from django.db import models
from django.utils.translation import gettext_lazy as _

class Plant(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Plant Name"))
    description = models.TextField(verbose_name=_("Description"))
    uses = models.TextField(verbose_name=_("Uses"))
    how_to_grow = models.TextField(verbose_name=_("How to Grow"))
    how_to_use = models.TextField(verbose_name=_("How to Use"))
    image = models.ImageField(upload_to='garden/plants/', blank=True, null=True, verbose_name=_("Plant Image"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Plant")
        verbose_name_plural = _("Plants")
        ordering = ['name']

class UserPlant(models.Model):
    STATUS_CHOICES = [
        ('Planning', 'Planning'),
        ('Growing', 'Growing'),
        ('Harvested', 'Harvested'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='garden_plants')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='user_instances')
    date_planted = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Planning')
    notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))
    is_for_swap = models.BooleanField(default=False, verbose_name=_("Available for Swap/Share"))
    qr_code = models.ImageField(upload_to='garden/qrcodes/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s {self.plant.name}"

    class Meta:
        unique_together = ('user', 'plant')
        ordering = ['-date_planted']

class PlantJournal(models.Model):
    user_plant = models.ForeignKey(UserPlant, on_delete=models.CASCADE, related_name='journal_entries')
    entry_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    content = models.TextField(verbose_name=_("Content"))
    image = models.ImageField(upload_to='garden/journal/', blank=True, null=True, verbose_name=_("Photo"))

    def __str__(self):
        return f"{self.title} - {self.user_plant}"

    class Meta:
        ordering = ['-entry_date', '-id']

class Harvest(models.Model):
    user_plant = models.ForeignKey(UserPlant, on_delete=models.CASCADE, related_name='harvests')
    date = models.DateField()
    quantity = models.FloatField(help_text="Quantity harvested")
    unit = models.CharField(max_length=50, default='kg', help_text="Unit (e.g., kg, count, lbs)")
    rating = models.IntegerField(default=5, help_text="Quality rating (1-5)")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user_plant.plant.name} - {self.date}"

    class Meta:
        ordering = ['-date']

class GardenTask(models.Model):
    TASK_TYPES = [
        ('Watering', 'Watering'),
        ('Fertilizing', 'Fertilizing'),
        ('Pruning', 'Pruning'),
        ('Pest Control', 'Pest Control'),
        ('Other', 'Other'),
    ]

    user_plant = models.ForeignKey(UserPlant, on_delete=models.CASCADE, related_name='tasks')
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    recurrence_days = models.IntegerField(blank=True, null=True, help_text="Repeat every X days")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.task_type} - {self.user_plant.plant.name}"

    class Meta:
        ordering = ['due_date']

class HealthLog(models.Model):
    ISSUE_TYPES = [
        ('Pest', 'Pest'),
        ('Disease', 'Disease'),
        ('Nutrient', 'Nutrient Deficiency'),
        ('Other', 'Other'),
    ]
    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    STATUS_CHOICES = [
        ('Identified', 'Identified'),
        ('Treating', 'Treating'),
        ('Resolved', 'Resolved'),
    ]

    user_plant = models.ForeignKey(UserPlant, on_delete=models.CASCADE, related_name='health_logs')
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='Low')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Identified')
    image = models.ImageField(upload_to='garden/health/', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date_logged = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.issue_type} - {self.user_plant.plant.name}"

    class Meta:
        ordering = ['-date_logged']

class GardenExpense(models.Model):
    CATEGORY_CHOICES = [
        ('Seeds', 'Seeds/Plants'),
        ('Soil', 'Soil/Amendments'),
        ('Tools', 'Tools'),
        ('Equipment', 'Equipment'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='garden_expenses')
    user_plant = models.ForeignKey(UserPlant, on_delete=models.SET_NULL, related_name='expenses', blank=True, null=True)
    item_name = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.item_name} - {self.cost}"

    class Meta:
        ordering = ['-date']
