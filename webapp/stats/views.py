from django.shortcuts import render
from django.http import HttpResponse, Http404

from collections import Counter

import pymongo

mongo_client = pymongo.MongoClient('mongodb://mongodb:27017')
context = {'title': 'Stats'}
context['sidebar'] = {'title': '', 'description': '', 'links': []}
context['breadcrumb'] = { 'title': {'name':'Stats' }}

def home_stats(request):
    context['databases'] = []
    context['sidebar']['title'] = 'Stats'
    context['sidebar']['description'] = 'General statistics about your databases, select any of them to explore more details about it.'

    for database in mongo_client.list_database_names():
        if database not in ('admin','local','config','stats'):
            db = {'name': database, 'collections': mongo_client[database].list_collection_names()}
            context['databases'].append(db)

    context['breadcrumb'] = {
        'title': { 'name': 'Stats' }
    }
    
    return render(request, 'stats/index.html', context)

def database_stats(request, database):
    if database not in mongo_client.list_database_names():
        raise Http404
    
    context['database'] = database

    records = mongo_client['stats']['database']
    context['collections'] = sorted(records.find_one({ 'database': database })['collections'].items())

    context['sidebar']['title'] = str.upper(database)
    context['sidebar']['description'] = 'Listing with the exams from the ' + database + ', select any of the exams for more details about it.'
    context['sidebar']['links'] = []
    context['sidebar']['links'].append({'text': 'Export ' + database, 'view':'export-database', 'parameters':database})

    context['breadcrumb'] = {
        'title': { 'name': 'Stats', 'link': { 'view': 'stats-home' }},
        'database': { 'name': database }
    }

    return render(request, 'stats/database.html', context)

def collection_stats(request, database, collection):
    if database not in mongo_client.list_database_names() or collection not in mongo_client[database].list_collection_names():
        raise Http404
    
    context['database'] = database
    context['collection'] = collection
    stat = mongo_client['stats']['collection'].find_one({ 'database': database, 'collection': collection })
    context['attributes'] = stat['attributes']

    context['sidebar']['title'] = str.upper(database)
    context['sidebar']['description'] = 'Listing with attributes of the ' + collection + ' exam from the ' + database + ', select any of the attributes for more details about it.'
    context['sidebar']['links'] = []
    context['sidebar']['links'].append({'text': 'Export ' + database, 'view':'export-database', 'parameters':database})

    context['breadcrumb'] = {
        'title': { 'name': 'Stats', 'link': { 'view': 'stats-home' }},
        'database': { 'name': database, 'link': { 'view': 'stats-database', 'parameters':database }},
        'collection': { 'name': collection }
    }
    
    return render(request, 'stats/collection.html', context)

def attribute_stats(request, database, collection, attribute):
    if database not in mongo_client.list_database_names() or collection not in mongo_client[database].list_collection_names():
        raise Http404
    if attribute not in mongo_client[database][collection].find_one({}):
        raise Http404

    context['database'] = database
    context['collection'] = collection
    context['attribute'] = attribute

    context['attribute_stats'] = mongo_client['stats']['statistics'].find_one({ 'database': database, 'collection': collection, 'attribute': attribute })

    context['attribute_stats']['values_counter'] = Counter(context['attribute_stats']['values']).items()

    context['sidebar']['title'] = str.upper(database)
    context['sidebar']['description'] = 'Statistics about ' + attribute + ' from the ' + collection + ' exam.'
    context['sidebar']['links'] = []
    context['sidebar']['links'].append({'text': 'Export ' + database, 'view':'export-database', 'parameters':database})

    context['breadcrumb'] = {
        'title': { 'name': 'Stats', 'link': { 'view': 'stats-home' }},
        'database': { 'name': database, 'link': { 'view': 'stats-database', 'parameters':database }},
        'collection': { 'name': collection, 'link': { 'view': 'stats-collection', 'parameters': {'database': database, 'collection': collection } }},
        'attribute': { 'name': attribute }
    }

    return render(request, 'stats/attribute.html', context)

def about(request):
    return render(request, 'stats/about.html', context)

