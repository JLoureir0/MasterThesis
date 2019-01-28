from django.shortcuts import render
from django.http import Http404

import pymongo

mongo_client = pymongo.MongoClient('mongodb://mongodb:27017')
context = {'title': 'Export'}
context['sidebar'] = {'title': '', 'description': '', 'links': [] }

def home_export(request):
    context['databases'] = []
    context['sidebar']['title'] = 'Export'
    context['sidebar']['description'] = 'Export from any database a dataset to CSV or ARFF formats, using custom options.'
    context['sidebar']['links'] = []
    
    for database in mongo_client.list_database_names():
        if database not in ('admin','local','config','stats'):
            context['databases'].append(database)
    return render(request, 'export/index.html', context)

def database_export(request, database):
    if database not in mongo_client.list_database_names():
        raise Http404

    context['database']= database
    context['sidebar']['title'] = str.upper(database)
    context['sidebar']['description'] = 'Export from '+ database +' a dataset to CSV or ARFF formats, with these options.'
    context['sidebar']['links'] = []
    context['sidebar']['links'].append({'text': 'Statistics for '+database, 'view':'stats-database', 'parameters':database})

    records = mongo_client['stats']['database']
    context['collections'] = sorted(records.find_one({ 'database': database })['collections'].keys())

    return render(request, 'export/database.html', context)
