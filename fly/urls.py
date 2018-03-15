from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^editing/$', views.editing, name="editing"),
    url(r'^lncrna/$', views.lncrna, name="lncrna"),
    url(r'^mirna/$', views.mirna, name="mirna"),
    url(r'^download/$', views.download, name="download"),
    url(r'^help/$', views.help, name="help"),
    url(r'^contact/$', views.contact, name="contact"),
    url(r'^queryset/(?P<page>\w*.*\w*)/$', views.getQuerySet, name="queryset"),

    #Editing details
    url(r'^editing/show/(?P<editingid>\d*)/$', views.editingShow, name="editingshow"),

    #lncRNA detail
    # url(r'^lncrna/(?P<chrom>chr[1-9|XYM][0-9]?)/$', views.lncrnaChr, name="lncrnachr"),
    url(r'^lncrna_chr/$', views.lncrnaChr, name="lncrnachr"),
    url(r'^lncrna/show/(?P<lncrnaid>\d*)/$', views.lncrnaShow, name="lncrnashow"),
    url(r'^lncrna/sequence/(?P<lncrnaid>\d*)/$', views.sequence, name='lncrnasequence'),
    url(r'^lncrna/structure/lncrnastructure_(?P<lncrnaid>\d*).png/$', views.lncrnaStructure, name="lncrnastructure"),

    # miRNA details
    url(r'^mirna/expression/$', views.mirnaExpression, name='mirnaexpression'),
    url(r'^mirna/show/(?P<mirnaid>\d*)/$', views.mirnaShow, name="mirnashow"),

    #funciton gain and loss
    # funciton gain and loss
    url(r'^function/(?P<function>gain|loss)/(?P<editingid>\d*)/(?P<mirnaid>\d*)/$', views.functionGainLoss,
        name='functiongainloss'),

    # rnafold
    url(r'^rnafold/(?P<lncrnaid>\d*)/(?P<editingid>\d*)/$', views.rnafold, name='rnafold'),

    #quick search
    url(r'^search/$', views.quickSearch, name='quicksearch'),
    # tools
    url(r'^tool/interaction/$', views.tInteraction, name='tinteraction'),
    url(r'^tool/structure/$', views.tStructure, name='tstructure')
]
