from django.db import models
from django.utils.translation import gettext_lazy as _


class PlantCheck(models.Model):
    CHECK_TYPE_CHOICES = [
        ('health', 'Plant Health Checkup'),
        ('disease', 'Plant Disease Detection'),
        ('yield', 'Crop Recommendation'),
        ('encyclopedia', 'Plants Encyclopedia'),
    ]

    SEVERITY_CHOICES = [
        ('healthy', 'Healthy'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='plant_checks'
    )
    check_type = models.CharField(
        max_length=20,
        choices=CHECK_TYPE_CHOICES,
        verbose_name=_("Check Type")
    )
    image = models.ImageField(
        upload_to='checks/uploads/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_("Plant Image")
    )
    temperature = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_("Temperature (°C)")
    )
    soil_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Soil Type")
    )
    rainfall = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_("Rainfall (mm/year)")
    )
    proposed_crop = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Proposed Crop")
    )
    result_title = models.CharField(
        max_length=300,
        blank=True,
        default='',
        verbose_name=_("Result Title")
    )
    result_summary = models.TextField(
        blank=True,
        default='',
        verbose_name=_("Result Summary")
    )
    result_details = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("Detailed Results")
    )
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        blank=True,
        default='',
        verbose_name=_("Severity")
    )
    confidence_score = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_("Confidence %")
    )
    recommendations = models.TextField(
        blank=True,
        default='',
        verbose_name=_("Recommendations")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_check_type_display()} - {self.user.username} ({self.created_at:%Y-%m-%d})"

    class Meta:
        verbose_name = _("Plant Check")
        verbose_name_plural = _("Plant Checks")
        ordering = ['-created_at']

    @property
    def severity_color(self):
        colors = {
            'healthy': 'emerald',
            'low': 'yellow',
            'medium': 'orange',
            'high': 'red',
            'critical': 'red',
        }
        return colors.get(self.severity, 'slate')

    @property
    def check_type_icon(self):
        icons = {
            'health': '💚',
            'disease': '🔬',
            'yield': '📊',
            'encyclopedia': '🌿',
        }
        return icons.get(self.check_type, '🌿')
