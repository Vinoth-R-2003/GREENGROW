from django import forms
from .models import UserPlant, Harvest, GardenTask, HealthLog, GardenExpense

class HarvestForm(forms.ModelForm):
    class Meta:
        model = Harvest
        fields = ['date', 'quantity', 'unit', 'rating', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

class GardenTaskForm(forms.ModelForm):
    class Meta:
        model = GardenTask
        fields = ['task_type', 'due_date', 'recurrence_days', 'notes']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class HealthLogForm(forms.ModelForm):
    class Meta:
        model = HealthLog
        fields = ['issue_type', 'severity', 'status', 'image', 'notes']

class GardenExpenseForm(forms.ModelForm):
    class Meta:
        model = GardenExpense
        fields = ['item_name', 'cost', 'date', 'category', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class PlantUpdateForm(forms.ModelForm):
    class Meta:
        model = UserPlant
        fields = ['status', 'notes', 'is_for_swap']
