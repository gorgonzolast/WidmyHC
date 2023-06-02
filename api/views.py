from django.http import JsonResponse
from pymongo import MongoClient
import datetime
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.parsers import JSONParser
from django.conf import settings
from bson.objectid import ObjectId
#import settings.py
from widmyHC import settings

# Create your views here.

@api_view(["GET", "POST", "DELETE"])
def hcs(request):
    client = MongoClient(settings.MONGO_CLI)
    db = client.hc_db
    hc = db['hcs']
    if request.method == "GET":
        result = []
        data = hc.find({})
        for dto in data:
            jsonData = {
                "id": str(dto['_id']),
                "hc": dto['hc'],
                'created_at': dto['created_at'],
                'paginas': dto['paginas'],
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result, safe=False)
    if request.method == "POST":
        data = JSONParser().parse(request)
        data['created_at'] = datetime.datetime.utcnow()
        paginas = []
        data['paginas'] = paginas
        result = hc.insert(data)
        respo ={
            "MongoObjectID": str(result),
            "Message": "nuevo objeto en la base de datos"
        }
        client.close()
        return JsonResponse(respo, safe=False)

    if request.method == "DELETE":
        data = hc.find({})
        for dto in data:
            hc.remove({"_id": dto['_id']})
        return JsonResponse({"Message": "Se han borrado todos los hcs"}, safe=False)
        
    

    
@api_view(["GET", "POST", "DELETE"])
def hcDetail(request, pk):
    client = MongoClient(settings.MONGO_CLI)
    db = client.hc_db
    hc = db['hc']
    if request.method == "GET":
        result = []
        data = hc.find({'_id': ObjectId(pk)})
        for dto in data:
            jsonData = {
                "id": str(dto['_id']),
                "hc": dto['hc'],
                'created_at': dto['created_at'],
                'paginas': dto['paginas'],
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result[0], safe=False)
    
    if request.method == "POST":
        data = JSONParser().parse(request)

        jsonData = {
            'descripcion': data["descripcion"],
            'datetime': datetime.datetime.utcnow()
        }

        result = hc.update(
        {'_id': ObjectId(pk)},
        {'$push': {'paginas': jsonData}}
        )

        respo = {
            "MongoObjectID": str(result),
            "Mensaje": "Se añadió una nueva pagina"
        }
        client.close()
        return JsonResponse(respo, safe=False)

    if request.method == "DELETE":
        result = hc.remove({"_id": ObjectId(pk)})
        respo = {
            "MongoObjectID": str(result),
            "Mensaje": "Se ha borrado una hc"
        }
        client.close()
        return JsonResponse(respo, safe=False)
