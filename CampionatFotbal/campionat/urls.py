from django.urls import path

from . import views

app_name = 'campionat'

urlpatterns = [
    path('', views.index, name='index'),
    path('echipe', views.echipe, name='echipe'),
    path('echipe/<int:id_echipa>', views.echipa, name='echipa'),
    path('echipe/<int:id_echipa>/addPage', views.addPage, name='addPage'),
    path('echipe/<int:id_echipa>/add', views.add, name='add'),
    path('echipe/<int:jucator_id>/editPage', views.editPage, name='editPage'),
    path('echipe/<int:jucator_id>/edit', views.edit, name='edit'),
    path('echipe/<int:jucatorId>/delete', views.delete, name='delete'),
    path('clasament/<int:etapa>', views.clasament, name='clasament'),
    path('clasament/<int:etapa>/filter', views.filter, name='filter'),
    path('valoare', views.clasamentValoare, name='valoare'),
    path('meciuri/<int:etapa>', views.meciuri, name='meciuri'),
]

