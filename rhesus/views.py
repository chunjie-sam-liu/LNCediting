from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response,render
from django.template import RequestContext,loader
from django.http import Http404, HttpResponseRedirect, HttpResponse
from .functions import *
# Create your views here.
def index(request):
    title = "rhesus LNCediting"
    context = {"title":title}
    return render(request, 'rhesus/index.html', context)

def editing(request):
    title = "Rhesus Editing Site"
    # Form input
    csrfmiddlewaretoken =request.GET['csrfmiddlewaretoken']
    regex = re.compile('[#$%^&*()+=\[\]\';,\/{}|"<>?~\\\\]')
    if regex.search(csrfmiddlewaretoken):
        html = "<html><body>Input is illegal</body></html>"
        return HttpResponse(html)
    total = edit_site_info.objects.using("rhesus")
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
    return render(request, 'rhesus/editing.html', context)

def lncrna(request):
    title = "Rhesus lncRNA"
    csrfmiddlewaretoken =request.GET['csrfmiddlewaretoken']
    regex = re.compile('[#$%^&*()+=\[\]\';,\/{}|"<>?~\\\\]')
    if regex.search(csrfmiddlewaretoken):
        html = "<html><body>Input is illegal</body></html>"
        return HttpResponse(html)
    total = lncrna_info.objects.using('rhesus')
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
    return render(request, 'rhesus/lncrna.html', context)

def mirna(request):
    title = "Rhesus miRNA"
    total_tmp = mirna_info.objects.using('rhesus')
    total = list()
    for i in total_tmp:
        if i.function_gains_set.count() or i.function_losses_set.count():
            total.append(i)

    pagination = paginate(request, total)
    select = total[pagination["offset"]: pagination["offsetEnd"]]
    context = {"title": title, "total": total, "select": select, "pagination": pagination}
    return render(request, 'rhesus/mirna.html', context)

def download(request):

    return render(request, 'rhesus/download.html')

def help(request):

    return render(request, 'rhesus/help.html')

def contact(request):

    return render(request, 'rhesus/contact.html')

def getQuerySet(request, page):
    total=list()
    if page == "Rhesus Editing Site":
        total = edit_site_info.objects.using('rhesus')
    if page == "Rhesus lncRNA":
        total = lncrna_info.objects.using('rhesus')

    return HttpResponse(total, content_type='text/plain')

def editingShow(request, editingid):
    title = "Rhesus Editing Site"
    editingRecord = edit_site_info.objects.using('rhesus').get(pk=editingid)
    editingLncrna = lncrna_info.objects.using('rhesus').get(pk=editingRecord.lncrna_info_id)
    editingEach = edit_sequence.objects.using('rhesus').get(edit_site_info_id__exact=editingid)

    rep_cons = None
    try:
        rep_cons = repeat_conservation.objects.using("rhesus").filter(chromosome__exact=editingRecord.chromosome).filter(chr_edit_pos__exact=editingRecord.chr_edit_pos).first()
    except:
        pass

    editingGain = None
    editingLoss = None
    try:
        editingGain = function_gains.objects.using('rhesus').filter(edit_site_info_id=editingid)
    except:
        pass
    try:
        editingLoss = function_losses.objects.using('rhesus').filter(edit_site_info_id=editingid)
    except:
        pass

    context = {"title": title, "editingid": editingid, "editingRecord": editingRecord, "editingLncrna": editingLncrna,"editingGain": editingGain, "editingLoss": editingLoss, "editingEach": editingEach, "rep_cons":rep_cons}
    return render(request, 'rhesus_editing/show.html', context)

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
    title = "rhesus lncRNA"
    total = lncrna_info.objects.using('rhesus')
    if chrom != 'all_chromosome':
        total = total.filter(chromosome__exact = chrom)
    pagination = paginate(request, total)
    select = total[pagination["offset"]: pagination["offsetEnd"]]

    context = {"title": title, "total": total, "select": select,"chromosome":chrom, "pagination": pagination}
    return render(request, 'rhesus/lncrna.html', context)

def lncrnaShow(request, lncrnaid):
    title = "rhesus lncRNA"
    lncrnaRecord = lncrna_info.objects.using('rhesus').get(pk=lncrnaid)
    lncrnaEditing = edit_site_info.objects.using('rhesus').filter(lncrna_info_id__exact=lncrnaRecord.id)
    lncrnaGain = list()
    lncrnaLoss = list()
    for edit in lncrnaEditing:
        try:
            lncrnaGain.extend(function_gains.objects.using('rhesus').filter(edit_site_info_id=edit.id))
        except:
            continue
    for edit in lncrnaEditing:
        try:
            lncrnaLoss.extend(function_losses.objects.using('rhesus').filter(edit_site_info_id=edit.id))
        except:
            continue

    context = {"title": title, "lncrnaid": lncrnaid, "lncrnaRecord": lncrnaRecord, "lncrnaEditing": lncrnaEditing,
               "lncrnaGain": lncrnaGain, "lncrnaLoss": lncrnaLoss}
    return render(request, 'rhesus_lncrna/show.html', context)

def mirnaExpression(request):
    title = "rhesus miRNA"
    mirnaid = request.GET['mirna']

    mirnaInfo = mirna_info.objects.using('rhesus').get(pk=mirnaid)
    mirnaProfile = mirna_profile.objects.using('rhesus').get(mirna_info_id__exact=mirnaid)
    mirnaGain = function_gains.objects.using('rhesus').filter(mirna_info_id__exact=mirnaid)
    mirnaLoss = function_losses.objects.using('rhesus').filter(mirna_info_id__exact=mirnaid)

    context = {"title":title,"mirnaid":mirnaid, "mirnaInfo":mirnaInfo, "mirnaProfile":mirnaProfile, "mirnaGain":mirnaGain, "mirnaLoss":mirnaLoss}
    return render(request, 'rhesus_mirna/show.html', context)

def mirnaShow(request, mirnaid):
    title = "rhesus miRNA"


    mirnaInfo = mirna_info.objects.using('rhesus').get(pk=mirnaid)
    try:
        mirnaProfile = mirna_profile.objects.using('rhesus').get(mirna_info_id__exact=mirnaid)
    except:
        mirnaProfile=""
    mirnaGain = function_gains.objects.using('rhesus').filter(mirna_info_id__exact=mirnaid)
    mirnaLoss = function_losses.objects.using('rhesus').filter(mirna_info_id__exact=mirnaid)

    context = {"title": title, "mirnaid": mirnaid, "mirnaInfo": mirnaInfo, "mirnaProfile": mirnaProfile,
               "mirnaGain": mirnaGain, "mirnaLoss": mirnaLoss}
    return render(request, 'rhesus_mirna/show.html', context)
