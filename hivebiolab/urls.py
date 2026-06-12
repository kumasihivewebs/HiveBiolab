from django.contrib import admin
from django.urls import path

from contact.views import submit_message
from hivebiolab.api_views import (
    health_check,
    list_projects,
    list_training_programs,
    retrieve_project,
    retrieve_training_program,
    training_page,
)
from newsletter.views import subscribe
from training.views import register_participant

urlpatterns = [
    path('admin/', admin.site.urls),
    path("health/", health_check, name="health_check"),
    path('api/newsletter/subscribe/', subscribe, name='newsletter_subscribe'),
    path('api/contact/', submit_message, name='contact_submit'),
    path('api/training/register/', register_participant, name='training_register'),
    path('api/training/', training_page, name='training_page'),
    path('api/projects/', list_projects, name='projects_list'),
    path('api/projects/<slug:slug>/', retrieve_project, name='project_detail'),
    path(
        'api/training/programs/',
        list_training_programs,
        name='training_programs_list',
    ),
    path(
        'api/training/programs/<slug:slug>/',
        retrieve_training_program,
        name='training_program_detail',
    ),
]
