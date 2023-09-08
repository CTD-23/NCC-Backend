from .models import *

def getContainer():
    container = Container.objects.filter(status=False).exists()
    if container:
        containerId = Container.objects.filter(status=False).first()
        containerId.status = True
        containerId.count+=1
        containerId.save()
        return containerId.containerId
    return False

def deallocate(containerid):
    container = Container.objects.get(containerId=containerid)
    container.status = False
    container.save()