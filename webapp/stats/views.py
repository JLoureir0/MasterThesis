from django.shortcuts import render
from django.http import HttpResponse, Http404
import pymongo

mongo_client = pymongo.MongoClient('mongodb://mongodb:27017')
context = {'title': 'Stats'}

def home_stats(request):
    context['databases'] = []
    for database in mongo_client.list_database_names():
        if database not in ('admin','local','config','stats'):
            db = {'name': database, 'collections': mongo_client[database].list_collection_names()}
            context['databases'].append(db)
    return render(request, 'stats/index.html', context)

def database_stats(request, database):
    if database not in mongo_client.list_database_names():
        raise Http404
    
    context['database'] = database

    records = mongo_client['stats']['database']
    context['collections'] = sorted(records.find_one({ 'database': database })['collections'].items())

    return render(request, 'stats/database.html', context)

def collection_stats(request, database, collection):
    if database not in mongo_client.list_database_names() or collection not in mongo_client[database].list_collection_names():
        raise Http404
    
    context['database'] = database
    context['collection'] = collection
    stat = mongo_client['stats']['collection'].find_one({ 'database': database, 'collection': collection })
    context['attributes'] = stat['attributes']
    
    return render(request, 'stats/collection.html', context)

def attribute_stats(request, database, collection, attribute):
    if database not in mongo_client.list_database_names() or collection not in mongo_client[database].list_collection_names():
        raise Http404
    if attribute not in mongo_client[database][collection].find_one({}):
        raise Http404

    context['attribute_stats'] = mongo_client['stats']['statistics'].find_one({ 'database': database, 'collection': collection, 'attribute': attribute })

    return render(request, 'stats/attribute.html', context)

def about(request):
    return render(request, 'stats/about.html', context)

