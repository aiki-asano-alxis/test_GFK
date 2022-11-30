from django.urls import include, path
from . import views
urlpatterns = [
    #preview
    path('', views.preview, name='preview'),

    path('previewsubfolder/<slug:subfolder>', views.previewsubfolder, name='previewsubfolder')
]
