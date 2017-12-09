from django.db import connection
from django.http import JsonResponse

def checkconnectivity(request):
    with connection.cursor() as cursor:
        query = "SELECT * FROM employees"
        cursor.execute(query)
        row = cursor.fetchone()

    if row:
        return JsonResponse({'result':'connection successful!'})
    else:
        return JsonResponse({'result':'connection failed!'})

