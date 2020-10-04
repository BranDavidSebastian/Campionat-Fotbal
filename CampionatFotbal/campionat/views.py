from django.shortcuts import render, get_object_or_404
from .models import Echipa, Jucator, Meci, Clasament
from itertools import combinations, islice
import random
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect



def index(request):
    #se sterg datele din tabel
    Meci.objects.all().delete()
    Clasament.objects.all().delete()
    numeEchipe = []
    #se selecteaza toate echipele din baza de date si se creeaza clasamentul initial
    echipe = Echipa.objects.all()
    for echipa in echipe:
        numeEchipe.append(echipa.nume)
        clasament = Clasament(etapa=0, echipa=echipa.nume, victorii=0, egaluri=0, infrangeri=0,
                              goluri_primite=0, goluri_inscrise=0, punctaj=0)
        clasament.save()

        jucatori = Jucator.objects.filter(echipa=echipa)
        valoare = 0
        for jucator in jucatori:
            valoare += jucator.valoare
        echipa.valoare = valoare
        echipa.save()

    #se creeaza meciurile si se grupeaza in tur si retur
    if len(numeEchipe) % 2:
        numeEchipe.append('Zi libera')  # daca nr de echipe este impar

    n = len(numeEchipe)
    meciuri = []
    etape = []
    meciuri_retur = []
    for etapa in range(1, n):
        for i in range(int(n / 2)):
            # genereaza random daca echipa e acasa sau in deplasare
            ordine = random.randint(1, 10)
            if ordine % 2 == 0:
                meciuri.append((numeEchipe[i], numeEchipe[n - 1 - i]))
                meciuri_retur.append((numeEchipe[n - 1 - i], numeEchipe[i]))

            else:
                meciuri.append((numeEchipe[n - 1 - i], numeEchipe[i]))
                meciuri_retur.append((numeEchipe[i], numeEchipe[n - 1 - i]))

        numeEchipe.insert(1, numeEchipe.pop())  # pune pe pozitia 1 ultima echipa ex 14 devine 1, 1 devine 2 etc
        etape.insert(int(len(etape) / 2), meciuri)  # adauga in prima jumatate a listei meciurile
        etape.append(meciuri_retur)  # adauga la final meciurile retur (a doua jumatate a listei)
        meciuri = []  # se goleste lista de meciuri pentru urmatoarea etapa
        meciuri_retur = []  # se goleste lista de meciuri retur pentru urmatoarea etapa


    i = 1

    nrEtapa = 1
    nrMeci = 0
    for etapa in etape:
        for meciuri_etapa in etapa:
            goluri_gazda = random.randint(0, 5)
            goluri_oaspete = random.randint(0, 5)
            scor = str(goluri_gazda) + ' - ' + str(goluri_oaspete)
            meci = Meci(etapa=nrEtapa, gazda=etape[nrEtapa-1][nrMeci][0], oaspete=etape[nrEtapa-1][nrMeci][1], scor=scor)
            meci.save()
            gazdaAnterior = Clasament.objects.get(
                echipa=etape[nrEtapa - 1][nrMeci][0], etapa=nrEtapa - 1)
            oaspeteAnterior = Clasament.objects.get(
                echipa=etape[nrEtapa - 1][nrMeci][1], etapa=nrEtapa - 1)
            if goluri_gazda > goluri_oaspete:
                gazda = Clasament(etapa=nrEtapa, echipa=etape[nrEtapa - 1][nrMeci][0],
                                  victorii=gazdaAnterior.victorii + 1, egaluri=gazdaAnterior.egaluri,
                                  infrangeri=gazdaAnterior.infrangeri,
                                  goluri_primite=gazdaAnterior.goluri_primite + goluri_oaspete,
                                  goluri_inscrise=gazdaAnterior.goluri_inscrise + goluri_gazda,
                                  punctaj=gazdaAnterior.punctaj + 3)
                oaspete = Clasament(etapa=nrEtapa, echipa=etape[nrEtapa - 1][nrMeci][1],
                                    victorii=oaspeteAnterior.victorii, egaluri=oaspeteAnterior.egaluri,
                                    infrangeri=oaspeteAnterior.infrangeri + 1,
                                    goluri_primite=oaspeteAnterior.goluri_primite + goluri_gazda,
                                    goluri_inscrise=oaspeteAnterior.goluri_inscrise + goluri_oaspete,
                                    punctaj=oaspeteAnterior.punctaj)
                gazda.save()
                oaspete.save()
            elif goluri_gazda < goluri_oaspete:
                gazda = Clasament(etapa=nrEtapa, echipa=etape[nrEtapa - 1][nrMeci][0], victorii=gazdaAnterior.victorii,
                                  egaluri=gazdaAnterior.egaluri, infrangeri=gazdaAnterior.infrangeri + 1,
                                  goluri_primite=gazdaAnterior.goluri_primite + goluri_oaspete,
                                  goluri_inscrise=gazdaAnterior.goluri_inscrise + goluri_gazda,
                                  punctaj=gazdaAnterior.punctaj)
                oaspete = Clasament(etapa=nrEtapa, echipa=etape[nrEtapa - 1][nrMeci][1],
                                    victorii=oaspeteAnterior.victorii + 1, egaluri=oaspeteAnterior.egaluri,
                                    infrangeri=oaspeteAnterior.infrangeri,
                                    goluri_primite=oaspeteAnterior.goluri_primite + goluri_gazda,
                                    goluri_inscrise=oaspeteAnterior.goluri_inscrise + goluri_oaspete,
                                    punctaj=oaspeteAnterior.punctaj + 3)
                gazda.save()
                oaspete.save()
            else:
                gazda = Clasament(etapa=nrEtapa, echipa=etape[nrEtapa - 1][nrMeci][0], victorii=gazdaAnterior.victorii,
                                  egaluri=gazdaAnterior.egaluri + 1, infrangeri=gazdaAnterior.infrangeri,
                                  goluri_primite=gazdaAnterior.goluri_primite + goluri_oaspete,
                                  goluri_inscrise=gazdaAnterior.goluri_inscrise + goluri_gazda,
                                  punctaj=gazdaAnterior.punctaj + 1)
                oaspete = Clasament(etapa=nrEtapa, echipa=etape[nrEtapa - 1][nrMeci][1],
                                    victorii=oaspeteAnterior.victorii, egaluri=oaspeteAnterior.egaluri + 1,
                                    infrangeri=oaspeteAnterior.infrangeri,
                                    goluri_primite=oaspeteAnterior.goluri_primite + goluri_gazda,
                                    goluri_inscrise=oaspeteAnterior.goluri_inscrise + goluri_oaspete,
                                    punctaj=oaspeteAnterior.punctaj + 1)
                gazda.save()
                oaspete.save()
            nrMeci = nrMeci + 1

        nrMeci = 0
        nrEtapa = nrEtapa + 1



    return render(request, 'campionat/index.html')

def echipe(request):

    echipe = Echipa.objects.all()
    context = {
        'echipe': echipe
    }
    return render(request, 'campionat/echipe.html', context)

def echipa(request, id_echipa):
    #echipa = Echipa.objects.get(id=id_echipa)
    echipa = get_object_or_404(Echipa, pk=id_echipa)
    jucatori = echipa.jucator_set.all()
    echipe = Echipa.objects.all()
    context = {
        'echipa': echipa,
        'jucatori': jucatori,
        'echipe': echipe
    }
    return render(request, 'campionat/echipa.html', context)

def clasament(request, etapa):
    clasament = Clasament.objects.filter(etapa=etapa).order_by('-punctaj')
    totalEtape = (Echipa.objects.all().count()-1)*2
    context = {
        'clasament': clasament,
        'etapa': etapa,
        'etapaAnterioara': etapa-1,
        'etapaUrmatoare': etapa+1,
        'totalEtape': totalEtape
    }
    return render(request, 'campionat/clasament.html', context)

def meciuri(request, etapa):
    meciuri = Meci.objects.filter(etapa=etapa)
    totalEtape = (Echipa.objects.all().count()-1)*2
    context = {
        'meciuri':meciuri,
        'etapa': etapa,
        'etapaAnterioara': etapa-1,
        'etapaUrmatoare': etapa+1,
        'totalEtape': totalEtape
    }
    return render(request, 'campionat/meciuri.html', context)




def delete(request, jucatorId):
    jucator = Jucator.objects.get(pk=jucatorId)
    id_echipa = jucator.echipa.pk
    Jucator.objects.filter(pk=jucatorId).delete()
    echipe = Echipa.objects.all()
    echipa = get_object_or_404(Echipa, pk=id_echipa)
    jucatori = echipa.jucator_set.all()
    context = {
        'echipa': echipa,
        'jucatori': jucatori,
        'echipe': echipe
    }
    jucatori = Jucator.objects.filter(echipa=echipa)
    valoare = 0
    for jucator in jucatori:
        valoare += jucator.valoare
    echipa.valoare = valoare
    echipa.save()


    return render(request, 'campionat/echipa.html', context)

def addPage(request, id_echipa):
    echipe = Echipa.objects.all()
    echipa = get_object_or_404(Echipa, pk=id_echipa)
    context = {
        'echipa': echipa,
        'echipe': echipe
    }
    return render(request, 'campionat/add.html', context)

def add(request, id_echipa):
    nume = request.GET['nume']
    valoare = request.GET['valoare']
    echipa = Echipa.objects.get(pk=id_echipa)
    jucator = Jucator(nume=nume, valoare=valoare, echipa=echipa)
    jucator.save()
    echipa = get_object_or_404(Echipa, pk=id_echipa)
    jucatori = echipa.jucator_set.all()
    echipe = Echipa.objects.all()
    context = {
        'echipa': echipa,
        'jucatori': jucatori,
        'echipe': echipe
    }
    jucatori = Jucator.objects.filter(echipa=echipa)
    valoare = 0
    for jucator in jucatori:
        valoare += jucator.valoare
    echipa.valoare = valoare
    echipa.save()
    return render(request, 'campionat/echipa.html', context)

def editPage(request, jucator_id):
    jucator = Jucator.objects.get(pk=jucator_id)
    echipe = Echipa.objects.all()
    echipa = get_object_or_404(Echipa, pk=jucator.echipa.id)
    context = {
        'echipa': echipa,
        'echipe': echipe,
        'jucator': jucator
    }
    return render(request, 'campionat/edit.html', context)

def edit(request, jucator_id):
    valoare = request.GET['valoare']
    jucator = Jucator.objects.get(pk=jucator_id)
    jucator.valoare = valoare
    jucator.save()
    echipa = get_object_or_404(Echipa, pk=jucator.echipa.id)
    jucatori = echipa.jucator_set.all()
    echipe = Echipa.objects.all()
    context = {
        'echipa': echipa,
        'jucatori': jucatori,
        'echipe': echipe
    }
    jucatori = Jucator.objects.filter(echipa=echipa)
    valoare = 0
    for jucator in jucatori:
        valoare += jucator.valoare
    echipa.valoare = valoare
    echipa.save()

    return render(request, 'campionat/echipa.html', context)


def filter(request, etapa):
    criteriu = request.GET['criteriu']
    valoare = request.GET['valoare']
    if not valoare or not valoare.isnumeric():
        clasament = Clasament.objects.filter(etapa=etapa).order_by('-punctaj')
    elif criteriu == 'Punctaj >':
        clasament = Clasament.objects.filter(etapa=etapa, punctaj__gt=valoare).order_by('-punctaj')
    elif criteriu == 'Punctaj <':
        clasament = Clasament.objects.filter(etapa=etapa, punctaj__lt=valoare).order_by('-punctaj')
    elif criteriu == 'Goluri inscrise':
        clasament = Clasament.objects.filter(etapa=etapa, goluri_inscrise__gt=valoare).order_by('-punctaj')
    elif criteriu == 'Goluri primite':
        clasament = Clasament.objects.filter(etapa=etapa, goluri_primite__gt=valoare).order_by('-punctaj')
    totalEtape = (Echipa.objects.all().count()-1)*2
    context = {
        'clasament': clasament,
        'etapa': etapa,
        'etapaAnterioara': etapa-1,
        'etapaUrmatoare': etapa+1,
        'totalEtape': totalEtape
    }
    return render(request, 'campionat/clasament.html', context)


def clasamentValoare(request):
    echipe = Echipa.objects.all().order_by('-valoare')
    context = {
        'echipe': echipe,
    }
    return render(request, 'campionat/valoare.html', context)




