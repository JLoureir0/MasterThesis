from django.shortcuts import render
from django.http import HttpResponse, Http404
import pymongo

mongo_client = pymongo.MongoClient('mongodb://mongodb:27017')
context = {'title': 'Stats'}

def home_stats(request):
    context['databases'] = []
    for database in mongo_client.list_database_names():
        if database != 'admin' and database != 'config' and database != 'local':
            db = {'name': database, 'collections': mongo_client[database].list_collection_names()}
            context['databases'].append(db)
    return render(request, 'stats/index.html', context)

def database_stats(request, database):
    if database not in mongo_client.list_database_names():
        raise Http404
    
    context['database'] = database
    context['collections'] = []
    for collection in mongo_client[database].list_collection_names():
        records = mongo_client[database][collection].count_documents({})
        coll = {'name': collection, 'records': records}
        context['collections'].append(coll)
    return render(request, 'stats/database.html', context)

def collection_stats(request, database, collection):
    if database not in mongo_client.list_database_names() or collection not in mongo_client[database].list_collection_names():
        raise Http404
    
    context['database'] = database
    context['collection'] = collection
    return render(request, 'stats/collection.html', context)


def about(request):
    return render(request, 'stats/about.html', context)

