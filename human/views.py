from django.shortcuts import render_to_response,render
from django.template import RequestContext,loader
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
#from .forms import QuickSearchForm
# Create your views here.
import base64
from .models import *
import operator
import re
from .functions import *

def index(request):
    title = "Human LNCediting"
    context = {"title":title}

    return render(request, 'human/index.html', context)

def editing(request):
    title = "Human Editing Site"
    #Form input
    # csrfmiddlewaretoken =request.GET['csrfmiddlewaretoken']
    # regex = re.compile('[#$%^&*()+=\[\]\';,\/{}|"<>?~\\\\]')
    # if regex.search(csrfmiddlewaretoken):
    #     html = "<html><body>Input is illegal</body></html>"
    #     return HttpResponse(html)
    total = edit_site_info.objects.using("human")
    if 'position' in request.GET:
        #position
        position = request.GET['position']

        regex = re.compile('[#$%^&*()+=\[\]\';,\/{}|"<>?~\\\\]')
        if regex.search(position):
            html = "<html><body>Input is illegal</body></html>"
            return HttpResponse(html)

        positionPattern = re.compile(r'[:-]')
        if positionPattern.search(position):
            positionSplit = positionPattern.split(position)
            if len(positionSplit) == 3:
                total = total.filter(chromosome__exact=positionSplit[0]).filter(chr_edit_pos__gte=int(positionSplit[1])).filter(chr_edit_pos__lte=positionSplit[2])
            else:
                total = total.filter(chromosome__exact=positionSplit[0])
        elif position.startswith("chr"):
            total = total.filter(chromosome__contains=position)

        #source
        source = request.GET['source']
        regex = re.compile('[#$%^&*()+=\[\]\';,\/{}|"<>?~\\\\]')
        if regex.search(source):
            html = "<html><body>Input is illegal</body></html>"
            return HttpResponse(html)

        if not source=="":
            total = total.filter(resource__exact=source)
    else:
        position = ""
    if 'term' in request.GET:
        term = request.GET['term']
        regex = re.compile('[#$%^&*()+=\[\]\';,\/{}|"<>?~\\\\]')
        if regex.search(term):
            html = "<html><body>Input is illegal</body></html>"
            return HttpResponse(html)
        total = total.filter(lncrna_id__icontains=term)


    pagination = paginate(request, total)
    select = total[pagination["offset"]: pagination["offsetEnd"]]


    context = {"total": total, "select":select,"title":title,"position":position, "pagination": pagination}
    return render(request, 'human/editing.html', context)

def lncrna(request):
    title = "Human lncRNA"

    # csrfmiddlewaretoken =request.GET['csrfmiddlewaretoken']
    # regex = re.compile('[#$%^&*()+=\[\]\';,\/{}|"<>?~\\\\]')
    # if regex.search(csrfmiddlewaretoken):
    #     html = "<html><body>Input is illegal</body></html>"
    #     return HttpResponse(html)

    total = lncrna_info.objects.using('human')
    if "term" in request.GET:
        term = request.GET.get('term')

        regex = re.compile('[#$%^&*()+=\[\]\';,\/{}|"<>?~\\\\]')
        if regex.search(term):
            html = "<html><body>Input is illegal</body></html>"
            return HttpResponse(html)

        total = total.filter(lncrna_id__icontains=term) | total.filter(resource__resource__icontains=term)
    pagination = paginate(request, total)
    select = total[pagination["offset"]: pagination["offsetEnd"]]
    context = {"title":title, "total":total, "select": select,"pagination": pagination}
    return render(request, 'human/lncrna.html', context)

def mirna(request):
    title = "Human miRNA"

    context = {"title":title}
    return render(request, 'human/mirna.html', context)

def download(request):
    title = "Human Download"

    context = {"title":title}
    return render(request, 'human/download.html',context)

def help(request):
    title = "Help Human"

    context = {"title": title}
    return render(request, 'human/help.html', context)

def contact(request):
    title = "Contact Us"

    context = {"title": title}
    return render(request, 'human/contact.html', context)

def getQuerySet(request, page):
    total=list()
    if page == "Human Editing Site":
        total = edit_site_info.objects.using('human')
    if page == "Human lncRNA":
        total = lncrna_info.objects.using('human')

    return HttpResponse(total, content_type='text/plain')

def lncrnaChr(request, chrom):
    title = "Human lncRNA"
    total = lncrna_info.objects.using('human')
    total = total.filter(chromosome__exact = chrom)
    pagination = paginate(request, total)
    select = total[pagination["offset"]: pagination["offsetEnd"]]

    context = {"title": title, "total": total, "select": select,"chromosome":chrom, "pagination": pagination}
    return render(request, 'human/lncrna.html', context)

def lncrnaShow(request, lncrnaid):
    title = "Human lncRNA"
    lncrnaRecord = lncrna_info.objects.using('human').get(pk=lncrnaid)
    lncrnaEditing = edit_site_info.objects.using('human').filter(lncrna_info_id__exact=lncrnaRecord.id)
    lncrnaGain = list()
    lncrnaLoss = list()
    for edit in lncrnaEditing:
        try:
            lncrnaGain.extend(function_gains.objects.using('human').filter(edit_site_info_id=edit.id))
        except :
            continue
    for edit in lncrnaEditing:
        try:
            lncrnaLoss.extend(function_losses.objects.using('human').filter(edit_site_info_id=edit.id))
        except:
            continue

    context = {"title":title, "lncrnaid":lncrnaid, "lncrnaRecord":lncrnaRecord,"lncrnaEditing":lncrnaEditing, "lncrnaGain":lncrnaGain, "lncrnaLoss":lncrnaLoss }
    return render(request, 'lncrna/show.html', context)

def editingShow(request, editingid):
    title = "Human Editing Site"
    editingRecord = edit_site_info.objects.using('human').get(pk=editingid)
    editingLncrna = lncrna_info.objects.using('human').get(pk=editingRecord.lncrna_info_id)
    editingEach = edit_sequence.objects.using('human').get(edit_site_info_id__exact=editingid)

    #Repeat and Conservation

    rep_cons = repeat_conservation.objects.using("human").filter(chromosome__exact=editingRecord.chromosome).filter(chr_edit_pos__exact=editingRecord.chr_edit_pos).first()


    editingGain = None
    editingLoss = None
    try:
        editingGain = function_gains.objects.using('human').filter(edit_site_info_id=editingid)
    except :
        pass
    try:
        editingLoss = function_losses.objects.using('human').filter(edit_site_info_id=editingid)
    except:
        pass


    context = {"title":title, "editingid":editingid, "editingRecord":editingRecord, "editingLncrna":editingLncrna, "editingGain":editingGain, "editingLoss":editingLoss, "editingEach":editingEach, "rep_cons":rep_cons}
    return render(request, 'editing/show.html', context)

def mirnaExpression(request):
    title = "Human miRNA"
    mirnaid = request.GET.get('mirna')

    mirnaInfo = mirna_info.objects.using('human').get(pk=mirnaid)
    mirnaProfileHeight = list()
    try:
        mirnaProfile = mirna_profile.objects.using('human').get(mirna_info_id__exact=mirnaid)

        mirnaProfile = [mirnaProfile.acc, mirnaProfile.blca, mirnaProfile.brca, mirnaProfile.cesc, mirnaProfile.coad,
                        mirnaProfile.dlbc, mirnaProfile.esca, mirnaProfile.hnsc, mirnaProfile.kich, mirnaProfile.kirc,
                        mirnaProfile.kirp, mirnaProfile.laml, mirnaProfile.lgg, mirnaProfile.lihc, mirnaProfile.luad,
                        mirnaProfile.lusc, mirnaProfile.meso, mirnaProfile.ov, mirnaProfile.paad, mirnaProfile.pcpg,
                        mirnaProfile.prad, mirnaProfile.reada, mirnaProfile.sarc, mirnaProfile.skcm, mirnaProfile.stad,
                        mirnaProfile.thca, mirnaProfile.ucec, mirnaProfile.ucs]

        cancerName = ["acc", "blca", "brca", "cesc", "coad", "dlbc", "esca", "hnsc", "kich", "kirc", "kirp", "laml",
                      "lgg", "lihc", "luad", "lusc", "meso", "ov", "paad", "pcpg", "prad", "reada", "sarc", "skcm",
                      "stad", "thca", "ucec", "ucs"]

        mirnaProfileExpression = [0.0 if i is None else i for i in mirnaProfile]
        # print(mirnaProfileExpression)
        mirnaProfileExpression = [float(i) for i in mirnaProfileExpression]
        averageProfile = sum(mirnaProfileExpression) / len(mirnaProfileExpression)
        maxH = max(mirnaProfileExpression) - min(mirnaProfileExpression)
        ratio = 255 / maxH

        mirnaProfileExpression = dict(zip(cancerName, mirnaProfileExpression))
        mirnaProfileExpression = sorted(mirnaProfileExpression.items(), key=operator.itemgetter(1), reverse=True)
        print(mirnaProfileExpression)

        for name, exp in mirnaProfileExpression:
            expressionDict = {
                "name": name,
                "expression": exp,
                "r": int(ratio * exp),
                "g": 255 - int(ratio * exp),
                "b": 0
            }

            mirnaProfileHeight.append(expressionDict)
    except:
        mirnaProfile = ""
        averageProfile = ""

    mirnaGain = function_gains.objects.using('human').filter(mirna_info_id__exact=mirnaid)
    mirnaLoss = function_losses.objects.using('human').filter(mirna_info_id__exact=mirnaid)

    context = {"title": title, "mirnaid": mirnaid, "mirnaInfo": mirnaInfo, "mirnaProfile": mirnaProfile,
               "mirnaGain": mirnaGain, "mirnaLoss": mirnaLoss, "mirnaProfileHeight": mirnaProfileHeight,
               "averageProfile": averageProfile}
    return render(request, 'mirna/show.html', context)

def mirnaShow(request, mirnaid):
    title = "Human miRNA"

    mirnaInfo = mirna_info.objects.using('human').get(pk=mirnaid)
    mirnaProfileHeight = list()
    try:
        mirnaProfile = mirna_profile.objects.using('human').get(mirna_info_id__exact=mirnaid)

        mirnaProfile = [mirnaProfile.acc, mirnaProfile.blca, mirnaProfile.brca, mirnaProfile.cesc, mirnaProfile.coad, mirnaProfile.dlbc,mirnaProfile.esca, mirnaProfile.hnsc, mirnaProfile.kich,mirnaProfile.kirc, mirnaProfile.kirp, mirnaProfile.laml, mirnaProfile.lgg, mirnaProfile.lihc, mirnaProfile.luad, mirnaProfile.lusc, mirnaProfile.meso, mirnaProfile.ov, mirnaProfile.paad, mirnaProfile.pcpg, mirnaProfile.prad, mirnaProfile.reada, mirnaProfile.sarc, mirnaProfile.skcm, mirnaProfile.stad, mirnaProfile.thca, mirnaProfile.ucec, mirnaProfile.ucs]

        cancerName=["acc","blca","brca","cesc","coad","dlbc","esca","hnsc","kich","kirc","kirp","laml","lgg","lihc","luad","lusc","meso","ov","paad","pcpg","prad","reada","sarc","skcm","stad","thca","ucec","ucs"]

        mirnaProfileExpression = [0.0 if i is None else i for i in mirnaProfile ]
        # print(mirnaProfileExpression)
        mirnaProfileExpression = [float(i) for i in mirnaProfileExpression]
        averageProfile = sum(mirnaProfileExpression) / len(mirnaProfileExpression)
        maxH = max(mirnaProfileExpression) - min(mirnaProfileExpression)
        ratio = 255 / maxH

        mirnaProfileExpression = dict(zip(cancerName, mirnaProfileExpression))
        mirnaProfileExpression = sorted(mirnaProfileExpression.items(), key=operator.itemgetter(1), reverse=True)
        print(mirnaProfileExpression)

        for name, exp in mirnaProfileExpression:
            expressionDict = {
            "name" : name,
            "expression": exp,
            "r": int(ratio * exp),
            "g": 255 - int(ratio * exp),
            "b":0
            }

            mirnaProfileHeight.append(expressionDict)
    except:
        mirnaProfile=""
        averageProfile=""

    mirnaGain = function_gains.objects.using('human').filter(mirna_info_id__exact=mirnaid)
    mirnaLoss = function_losses.objects.using('human').filter(mirna_info_id__exact=mirnaid)

    context = {"title": title, "mirnaid": mirnaid, "mirnaInfo": mirnaInfo, "mirnaProfile": mirnaProfile,
               "mirnaGain": mirnaGain, "mirnaLoss": mirnaLoss, "mirnaProfileHeight":mirnaProfileHeight,"averageProfile": averageProfile }
    return render(request, 'mirna/show.html', context)
