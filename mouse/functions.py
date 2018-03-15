from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response,render,redirect
import re
import math
import os,sys
from .models import *
import uuid
from shutil import copyfile
from django.conf import settings
#PIL
from PIL import Image, ImageDraw
def paginate(request, totalQuery):
    #Pagination
    pagesize = 30
    # totalCount = len(totalQuery)

    totalCount = 300
    pages = int(math.ceil(totalCount / float(pagesize)))
    if "page" in request.GET:
        page = int(request.GET['page'])
    else:
        page = 1
    offset = pagesize * (page - 1)
    #pageURL
    pageURL = request.get_full_path()
    if re.search(r'=', pageURL):
        if re.search(r'page=', pageURL):
            pageURL = re.sub(u'page=\d*','page=',pageURL)
        else:
            pageURL += "&page="
    else:
        pageURL += "?page="
    pagination = {"pageURL":pageURL,"page":page, "pages":pages, "pageRange":range(1,pages + 1), "offset":offset,"offsetEnd": offset + pagesize}
    return pagination

def sequence(request, lncrnaid):
    lncrnaRecord = lncrna_info.objects.using('mouse').get(pk=lncrnaid)
    wild_sequence = ">%s\n%s"  % (lncrnaRecord.lncrna_id,lncrnaRecord.wild_sequence )
    return HttpResponse(wild_sequence, content_type="text/plain")

def lncrnaStructure(request, lncrnaid):
    lncrnaRecord = lncrna_info.objects.using('mouse').get(pk=lncrnaid)
    editingSites = edit_site_info.objects.using('mouse').filter(lncrna_info_id__exact=lncrnaid)

    exonsCount = lncrnaRecord.exons_count
    exonsStart = [int(i) for i in lncrnaRecord.exons_start.split(",")]
    exonsEnd = [int(i) for i in lncrnaRecord.exons_end.split(",")]

    startPos = min(exonsStart)
    endPos = max(exonsEnd)
    offset = 10
    stepSize = 400.0 / (endPos - startPos)

    im = Image.new('RGB', (420,30), (255,255,255))
    draw = ImageDraw.Draw(im)
    draw.line((0, 15,520,15), fill = (49,117,176))
    # draw.rectangle(((offset + (exonsStart[0] - startPos) * stepSize , 0), (offset + (exonsEnd[0] - startPos) * stepSize , 14)), fill=(0, 0, 0))
    for i in range(exonsCount):
        x1 = offset + (exonsStart[i] - startPos) * stepSize
        y1 = 7
        x2 = offset + (exonsEnd[i] - startPos) * stepSize
        y2 = 23
        draw.rectangle(((x1,y1), (x2, y2)), fill=(255,0,0))

    for edit in editingSites:
        x1 = offset + (int(edit.chr_edit_pos) - startPos) * stepSize
        y1 = 2
        x2 = x1
        y2 = 28
        draw.line((x1,y1,x2,y2), fill = "black")

    response = HttpResponse(content_type="image/png")
    im.save(response, "PNG")
    return response

def functionGainLoss(request, function, editingid, mirnaid):
    title = "mouse Editing Site"
    editingRecord = edit_site_info.objects.using('mouse').get(pk=editingid)
    editingLncrna = lncrna_info.objects.using('mouse').get(pk=editingRecord.lncrna_info_id)
    editingGain = None
    editingLoss = None
    try:
        editingGain = function_gains.objects.using('mouse').filter(edit_site_info_id=editingid).get(mirna_info_id__exact=mirnaid)
    except:
        pass
    try:
        editingLoss = function_losses.objects.using('mouse').filter(edit_site_info_id=editingid).get(mirna_info_id__exact=mirnaid)
    except:
        pass

    context = {"title": title, "editingid": editingid, "editingRecord": editingRecord, "editingLncrna": editingLncrna,
               "editingGain": editingGain, "editingLoss": editingLoss, 'function':function}
    if function == "gain":
        return render(request, 'mouse/function_gain.html', context)
    if function == "loss":
        return render(request, 'mouse/function_loss.html', context)

def rnafold(request, lncrnaid, editingid):
    title = "mouse RNA fold"
    lncrnafold = lncrna_info.objects.using('mouse').get(pk=lncrnaid)
    editingfold = edit_site_info.objects.using('mouse').get(pk=editingid)

    context = {"title": title, "lncrnaid": lncrnaid, "editingid":editingid, "lncrnafold":lncrnafold, "editingfold":editingfold}

    return render(request, 'mouse/rnafold.html', context)

def quickSearch(request):
    title = "Quick Search"
    term = request.GET.get("term")
    regex = re.compile('[#$%^&*()+=\[\]\';,\/{}|"<>?~\\\\]')
    if regex.search(term):
        html = "<html><body>Input is illegal</body></html>"
        return HttpResponse(html)
    if not term:
        term = ''
    else:
        term=term.strip()
    # editing position
    positionPattern = re.compile(r'chr',flags = re.IGNORECASE)
    positionSelect = list()

    #lncrna as default search
    lncrnaSelect = list()

    #mirna search
    mirnaPattern = re.compile(r'mir', flags = re.IGNORECASE)
    mirnaSelect = list()

    if positionPattern.search(term):
        total = edit_site_info.objects.using("mouse")
        position = term

        positionPattern = re.compile(r'[:-]')
        if positionPattern.search(position):
            positionSplit = positionPattern.split(position)
            if len(positionSplit) == 3:
                total = total.filter(chromosome__exact=positionSplit[0]).filter(
                    chr_edit_pos__gte=int(positionSplit[1])).filter(chr_edit_pos__lte=positionSplit[2])
            else:
                total = total.filter(chromosome__exact=positionSplit[0])
        elif position.startswith("chr"):
            total = total.filter(chromosome__icontains=position)
        else:
            pass
        pagination = paginate(request, total)
        positionSelect = total[pagination["offset"]: pagination["offsetEnd"]]

    elif mirnaPattern.search(term):
        total = mirna_info.objects.using('mouse')
        total = total.filter(mirna_id__icontains=term)
        pagination = paginate(request, total)
        mirnaSelect = total[pagination["offset"]: pagination["offsetEnd"]]
    else:
        total = lncrna_info.objects.using('mouse')
        total = total.filter(lncrna_id__icontains=term) | total.filter(resource__resource__icontains=term)
        pagination = paginate(request, total)
        lncrnaSelect = total[pagination["offset"]: pagination["offsetEnd"]]

    context = {"title":title, "term":term,"total":total, "positionSelect":positionSelect,"mirnaSelect": mirnaSelect,"lncrnaSelect": lncrnaSelect,"pagination": pagination}
    return render(request, 'mouse/search.html', context)

def tInteraction(request):
    functionPath = os.path.dirname(os.path.abspath(__file__))
    title = "miRNA lncRNA Interaction"

    wild = request.GET.get('wild')
    if not wild:
        return redirect('http://bioinfo.life.hust.edu.cn/LNCediting/mouse/')
    position = int(request.GET.get('position').strip())
    edit = wild[:position - 1] + "G" + wild[position:]
    uniq_code = uuid.uuid4().hex.upper()
    command = "perl %s/templates/mouse_tools/tool_list/interaction/online_analysis.pl %s %s %s" %(functionPath, wild, edit, uniq_code)
    os.system(command)

    #Wild file
    file_wild = functionPath + "/templates/mouse_tools/tool_result/interaction_result/seq1_target." + uniq_code
    copyfile(file_wild, functionPath + '/static/mouse/download/wild_download.txt')
    copyfile(file_wild, settings.BASE_DIR + '/static/mouse/download/wild_download.txt')
    file_wild_list = list()
    with open(file_wild, 'r') as foo:
        for line in foo:
            if line.startswith("#"): continue
            arr = line.rstrip().split("\t")
            wild_dict={
                "mir_wild":arr[0],
                'start_ts_wild': arr[1],
                'end_ts_wild':arr[2],
                'start_da_wild': arr[3],
                'end_da_wild': arr[4],
                'da_sc_wild': arr[5],
                'da_en_wild': arr[6]
            }
            file_wild_list.append(wild_dict)

    #Edit file
    file_edit = functionPath + "/templates/mouse_tools/tool_result/interaction_result/seq2_target." + uniq_code
    copyfile(file_edit, functionPath + '/static/mouse/download/edit_download.txt')
    copyfile(file_edit, settings.BASE_DIR + '/static/mouse/download/edit_download.txt')
    file_edit_list = list()
    with open(file_edit ,'r') as foo:
        for line in foo:
            if line.startswith("#"): continue
            arr = line.rstrip().split("\t")
            edit_dict = {
                "mir_edit": arr[0],
                'start_ts_edit': arr[1],
                'end_ts_edit': arr[2],
                'start_da_edit': arr[3],
                'end_da_edit': arr[4],
                'da_sc_edit': arr[5],
                'da_en_edit': arr[6]
            }
            file_edit_list.append(edit_dict)

    #Loss file
    file_loss = functionPath + "/templates/mouse_tools/tool_result/interaction_result/seq_target_loss." + uniq_code
    copyfile(file_loss, functionPath + '/static/mouse/download/loss_download.txt')
    copyfile(file_loss, settings.BASE_DIR + '/static/mouse/download/loss_download.txt')
    file_loss_list = list()
    with open(file_loss ,'r') as foo:
        for line in foo:
            if line.startswith("#"): continue
            arr = line.rstrip().split("\t")
            loss_dict = {
                "mir_loss": arr[0],
                'start_ts_loss': arr[1],
                'end_ts_loss': arr[2],
                'start_da_loss': arr[3],
                'end_da_loss': arr[4],
                'da_sc_loss': arr[5],
                'da_en_loss': arr[6]
            }
            file_loss_list.append(loss_dict)

    #Gain file
    file_gain = functionPath + "/templates/mouse_tools/tool_result/interaction_result/seq_target_gain." + uniq_code
    copyfile(file_gain, functionPath + '/static/mouse/download/gain_download.txt')
    copyfile(file_gain, settings.BASE_DIR + '/static/mouse/download/gain_download.txt')
    file_gain_list = list()
    with open(file_gain ,'r') as foo:
        for line in foo:
            if line.startswith("#"): continue
            arr = line.rstrip().split("\t")
            gain_dict = {
                "mir_gain": arr[0],
                'start_ts_gain': arr[1],
                'end_ts_gain': arr[2],
                'start_da_gain': arr[3],
                'end_da_gain': arr[4],
                'da_sc_gain': arr[5],
                'da_en_gain': arr[6]
            }
            file_gain_list.append(gain_dict)

    context = {"title": title, "wild": wild, "position": position, "edit": edit, "file_wild_list":file_wild_list, "file_edit_list":file_edit_list, "file_loss_list":file_loss_list, "file_gain_list":file_gain_list}
    return render(request, 'mouse_tools/tool_result/miRNA_lncRNA_result.html', context)

def tStructure(request):
    functionPath = os.path.dirname(os.path.abspath(__file__))
    title = 'Editing Structure'

    wild = request.GET.get('wild')
    if not wild:
        return redirect('http://bioinfo.life.hust.edu.cn/LNCediting/mouse/')
    position = int(request.GET.get('position').strip())
    edit = wild[:position-1] + "G" + wild[position:]
    command = "perl %s/templates/mouse_tools/tool_list/structure/online_analysis.pl %s %s" %(functionPath, wild, edit)
    os.system(command)

    #copy to mouse/static/mouse
    copyfile(functionPath + "/templates/mouse_tools/tool_list/structure/SEQ1.png", functionPath + "/static/mouse/tool_structure/SEQ1.png")
    copyfile(functionPath + "/templates/mouse_tools/tool_list/structure/SEQ2.png", functionPath + "/static/mouse/tool_structure/SEQ2.png")

    #copy to static/mouse in root path
    copyfile(functionPath + "/templates/mouse_tools/tool_list/structure/SEQ1.png", settings.BASE_DIR + "/static/mouse/tool_structure/SEQ1.png")
    copyfile(functionPath + "/templates/mouse_tools/tool_list/structure/SEQ2.png", settings.BASE_DIR + "/static/mouse/tool_structure/SEQ2.png")

    file_wild = "%s/templates/mouse_tools/tool_list/structure/seq1_RNAfold_re" % functionPath
    fe_wild = open(file_wild, 'r').readlines()
    fe_wild_sequence = fe_wild[1]
    fe_wild_notation = fe_wild[2].split(" ")[0]
    fe_wild_energy = fe_wild[2].split(" ")[1].rstrip("\n").strip("(").strip(")")

    file_editing = "%s/templates/mouse_tools/tool_list/structure/seq2_RNAfold_re" % functionPath
    fe_editing = open(file_editing, 'r').readlines()
    fe_editing_sequence = fe_editing[1]
    fe_editing_notation = fe_editing[2].split(" ")[0]
    fe_editing_energy = fe_editing[2].split(" ")[1].rstrip("\n").strip("(").strip(")")

    context = {"titile": title, "wild": wild, "position": position, "edit": edit, "fe_wild_sequence": fe_wild_sequence,
               "fe_wild_notation": fe_wild_notation, "fe_wild_energy": fe_wild_energy,
               "fe_editing_sequence": fe_editing_sequence, "fe_editing_notation": fe_editing_notation,
               "fe_editing_energy": fe_editing_energy}

    return render(request,'mouse_tools/tool_result/editing_lncRNA_result.html',context)
