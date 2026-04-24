from django.contrib import admin
from django.urls import path

from contact.views import submit_message
from hivebiolab.api_views import health_check, list_projects, list_training_programs
from newsletter.views import subscribe
from training.views import register_participant

urlpatterns = [
    path('admin/', admin.site.urls),
    path("health/", health_check, name="health_check"),
    path('api/newsletter/subscribe/', subscribe, name='newsletter_subscribe'),
    path('api/contact/', submit_message, name='contact_submit'),
    path('api/training/register/', register_participant, name='training_register'),
    path('api/projects/', list_projects, name='projects_list'),
    path(
        'api/training/programs/',
        list_training_programs,
        name='training_programs_list',
    ),
]
