from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response,render
from django.template import RequestContext,loader
from django.http import Http404, HttpResponseRedirect, HttpResponse
from .functions import *
# Create your views here.
def index(request):
    title = "fly LNCediting"
    context = {"title":title}
    return render(request, 'fly/index.html', context)

def editing(request):
    title = "Fly Editing Site"
    # Form input
    csrfmiddlewaretoken =request.GET['csrfmiddlewaretoken']
    regex = re.compile('[#$%^&*()+=\[\]\';,\/{}|"<>?~\\\\]')
    if regex.search(csrfmiddlewaretoken):
        html = "<html><body>Input is illegal</body></html>"
        return HttpResponse(html)
    total = edit_site_info.objects.using("fly")
    if 'position' in request.GET:
        # position
        position = request.GET['position']

        regex = re.compile('[#$%^&*()+=\[\]\';,\/{}|"<>?~\\\\]')
        if regex.search(position):
            html = "<html><body>Input is illegal</body></html>"
            return HttpResponse(html)

        positionPattern = re.compile(r'[:-]')
        if positionPattern.search(position):
            positionSplit = positionPattern.split(position)
            if len(positionSplit) == 3:
                total = total.filter(chromosome__exact=positionSplit[0]).filter(
                    chr_edit_pos__gte=int(positionSplit[1])).filter(chr_edit_pos__lte=positionSplit[2])
            else:
                total = total.filter(chromosome__exact=positionSplit[0])
        elif position.startswith("chr"):
            total = total.filter(chromosome__exact=position)

        # source
    #     source = request.GET['source']
    #     if not source == "":
    #         total = total.filter(resource__contains=source)
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

    context = {"total": total, "select": select, "title": title, "position": position, "pagination": pagination}
    return render(request, 'fly/editing.html', context)

def lncrna(request):
    title = "Fly lncRNA"
    total = lncrna_info.objects.using('fly')

    csrfmiddlewaretoken =request.GET['csrfmiddlewaretoken']
    regex = re.compile('[#$%^&*()+=\[\]\';,\/{}|"<>?~\\\\]')
    if regex.search(csrfmiddlewaretoken):
        html = "<html><body>Input is illegal</body></html>"
        return HttpResponse(html)

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
    return render(request, 'fly/lncrna.html', context)

def mirna(request):
    title = "fly miRNA"
    total_temp = mirna_info.objects.using('fly')
    total = list()
    for i in total_temp:
        if i.function_gains_set.count() or i.function_losses_set.count():
            total.append(i)
    pagination = paginate(request, total)
    select = total[pagination["offset"]: pagination["offsetEnd"]]
    context = {"title": title, "total": total, "select": select, "pagination": pagination}
    return render(request, 'fly/mirna.html', context)

def download(request):

    return render(request, 'fly/download.html')

def help(request):

    return render(request, 'fly/help.html')

def contact(request):

    return render(request, 'fly/contact.html')

def getQuerySet(request, page):
    total=list()
    if page == "Fly Editing Site":
        total = edit_site_info.objects.using('fly')
    if page == "Fly lncRNA":
        total = lncrna_info.objects.using('fly')

    return HttpResponse(total, content_type='text/plain')


def editingShow(request, editingid):
    title = "Rhesus Editing Site"
    editingRecord = edit_site_info.objects.using('fly').get(pk=editingid)
    editingLncrna = lncrna_info.objects.using('fly').get(pk=editingRecord.lncrna_info_id)
    editingEach = edit_sequence.objects.using('fly').get(edit_site_info_id__exact=editingid)

    rep_cons = repeat_conservation.objects.using("fly").filter(chromosome__exact=editingRecord.chromosome).filter(chr_edit_pos__exact=editingRecord.chr_edit_pos).first()

    editingGain = None
    editingLoss = None
    try:
        editingGain = function_gains.objects.using('fly').filter(edit_site_info_id=editingid)
    except:
        pass
    try:
        editingLoss = function_losses.objects.using('fly').filter(edit_site_info_id=editingid)
    except:
        pass

    context = {"title": title, "editingid": editingid, "editingRecord": editingRecord, "editingLncrna": editingLncrna,"editingGain": editingGain, "editingLoss": editingLoss, "editingEach": editingEach, "rep_cons":rep_cons}
    return render(request, 'fly_editing/show.html', context)

def lncrnaChr(request):
    csrfmiddlewaretoken =request.GET['csrfmiddlewaretoken']
    regex = re.compile('[#$%^&*()+=\[\]\';,\/{}|"<>?~\\\\]')
    if regex.search(csrfmiddlewaretoken):
        html = "<html><body>Input is illegal</body></html>"
        return HttpResponse(html)
    chrom = request.GET.get("chromosome", "all_chromosome")
    if regex.search(chrom):
        html = "<html><body>Input is illegal</body></html>"
        return HttpResponse(html)
    title = "fly lncRNA"
    total = lncrna_info.objects.using('fly')
    if chrom != "all_chromosome":
        total = total.filter(chromosome__exact = chrom)
    pagination = paginate(request, total)
    select = total[pagination["offset"]: pagination["offsetEnd"]]

    context = {"title": title, "total": total, "select": select,"chromosome":chrom, "pagination": pagination}
    return render(request, 'fly/lncrna.html', context)

def lncrnaShow(request, lncrnaid):
    title = "fly lncRNA"
    lncrnaRecord = lncrna_info.objects.using('fly').get(pk=lncrnaid)
    lncrnaEditing = edit_site_info.objects.using('fly').filter(lncrna_info_id__exact=lncrnaRecord.id)
    lncrnaGain = list()
    lncrnaLoss = list()
    for edit in lncrnaEditing:
        try:
            lncrnaGain.extend(function_gains.objects.using('fly').filter(edit_site_info_id=edit.id))
        except:
            continue
    for edit in lncrnaEditing:
        try:
            lncrnaLoss.extend(function_losses.objects.using('fly').filter(edit_site_info_id=edit.id))
        except:
            continue

    context = {"title": title, "lncrnaid": lncrnaid, "lncrnaRecord": lncrnaRecord, "lncrnaEditing": lncrnaEditing,
               "lncrnaGain": lncrnaGain, "lncrnaLoss": lncrnaLoss}
    return render(request, 'fly_lncrna/show.html', context)

def mirnaExpression(request):
    title = "fly miRNA"
    mirnaid = request.GET['mirna']

    mirnaInfo = mirna_info.objects.using('fly').get(pk=mirnaid)
    mirnaProfile = mirna_profile.objects.using('fly').get(mirna_info_id__exact=mirnaid)
    mirnaGain = function_gains.objects.using('fly').filter(mirna_info_id__exact=mirnaid)
    mirnaLoss = function_losses.objects.using('fly').filter(mirna_info_id__exact=mirnaid)

    context = {"title":title,"mirnaid":mirnaid, "mirnaInfo":mirnaInfo, "mirnaProfile":mirnaProfile, "mirnaGain":mirnaGain, "mirnaLoss":mirnaLoss}
    return render(request, 'fly_mirna/show.html', context)

def mirnaShow(request, mirnaid):
    title = "fly miRNA"


    mirnaInfo = mirna_info.objects.using('fly').get(pk=mirnaid)
    try:
        mirnaProfile = mirna_profile.objects.using('fly').get(mirna_info_id__exact=mirnaid)
    except:
        mirnaProfile=""
    mirnaGain = function_gains.objects.using('fly').filter(mirna_info_id__exact=mirnaid)
    mirnaLoss = function_losses.objects.using('fly').filter(mirna_info_id__exact=mirnaid)

    context = {"title": title, "mirnaid": mirnaid, "mirnaInfo": mirnaInfo, "mirnaProfile": mirnaProfile,
               "mirnaGain": mirnaGain, "mirnaLoss": mirnaLoss}
    return render(request, 'fly_mirna/show.html', context)
