from django.db import models

# Create your models here.

class mirna_info(models.Model):
    mirna_id = models.CharField(max_length=225)
    accession = models.CharField(max_length=225)
    chromosome = models.CharField(max_length=45)
    strand = models.CharField(max_length=4)
    start = models.BigIntegerField()
    end = models.BigIntegerField()
    mature_sequence = models.CharField(max_length=500)
    pre_mirna_id = models.CharField(max_length=45)
    pre_start = models.BigIntegerField()
    pre_end = models.BigIntegerField()
    pre_sequence = models.CharField(max_length=10000)

    def __str__(self):
        return self.mirna_id

class lncrna_info(models.Model):
    lncrna_id = models.CharField(max_length=225,null=True)
    combined_resource = models.CharField(max_length=225,null=True)
    strand = models.CharField(max_length=4,null=True)
    annotation_by_RADAR = models.CharField(max_length=225,null=True)
    chromosome = models.CharField(max_length=45,null=True)
    trans_start = models.BigIntegerField(null=True)
    trans_end = models.BigIntegerField(null=True)
    exons_count = models.IntegerField(null=True)
    exons_start = models.TextField(null=True)
    exons_end = models.TextField(null=True)
    wild_sequence = models.TextField(null=True)
    wild_energy = models.FloatField(null=True)
    edit_sequence = models.TextField( null=True)
    edit_energy = models.FloatField(null=True)
    delta_energy = models.FloatField(null=True)
    edit_num = models.IntegerField(null=True)
    gain_num = models.IntegerField(null=True)
    loss_num = models.IntegerField(null=True)

    def __str__(self):
        return self.lncrna_id

class edit_site_info(models.Model):
    chromosome = models.CharField(max_length=45,null=True)
    chr_edit_pos = models.BigIntegerField(null=True)
    trans_edit_pos = models.BigIntegerField(null=True)
    lncrna_id = models.CharField(max_length=225,null=True)
    resource = models.CharField(max_length=225,null=True)
    lncrna_info = models.ForeignKey(lncrna_info)

    def __str__(self):
        return self.lncrna_id

class function_losses(models.Model):
    mirna_id = models.CharField(max_length=225,null=True)
    chromosome = models.CharField(max_length=20,null=True)
    chr_edit_pos = models.BigIntegerField(null=True)
    lncrna_id = models.CharField(max_length=225,null=True)
    resource = models.CharField(max_length=200,null=True)
    score = models.FloatField(null=True)
    energy = models.FloatField(null=True)
    targetscan_start_r = models.BigIntegerField(null=True)
    targetscan_end_r = models.BigIntegerField(null=True)
    miranda_start_r = models.BigIntegerField(null=True)
    miranda_end_r = models.BigIntegerField(null=True)
    ref_edit_pos = models.IntegerField(null=True)
    en = models.FloatField(null=True)
    query_start = models.IntegerField(null=True)
    query_end = models.IntegerField(null=True)
    ref_start = models.IntegerField(null=True)
    ref_end = models.IntegerField(null=True)
    align_length = models.IntegerField(null=True)
    query_percentage = models.FloatField(null=True)
    ref_percentage = models.FloatField(null=True)
    query_match_sequence = models.CharField(max_length=225,null=True)
    match_string = models.CharField(max_length=225, null=True)
    ref_match_sequence = models.CharField(max_length=225,null=True)
    edit_site_info = models.ForeignKey(edit_site_info)
    mirna_info = models.ForeignKey(mirna_info)

    def __str__(self):
        return self.mirna_id

class function_gains(models.Model):
    mirna_id = models.CharField(max_length=225,null=True)
    chromosome = models.CharField(max_length=20,null=True)
    chr_edit_pos = models.BigIntegerField(null=True)
    lncrna_id = models.CharField(max_length=225,null=True)
    resource = models.CharField(max_length=200,null=True)
    score = models.FloatField(null=True)
    energy = models.FloatField(null=True)
    targetscan_start_r = models.BigIntegerField(null=True)
    targetscan_end_r = models.BigIntegerField(null=True)
    miranda_start_r = models.BigIntegerField(null=True)
    miranda_end_r = models.BigIntegerField(null=True)
    ref_edit_pos = models.IntegerField(null=True)
    en = models.FloatField(null=True)
    query_start = models.IntegerField(null=True)
    query_end = models.IntegerField(null=True)
    ref_start = models.IntegerField(null=True)
    ref_end = models.IntegerField(null=True)
    align_length = models.IntegerField(null=True)
    query_percentage = models.FloatField(null=True)
    ref_percentage = models.FloatField(null=True)
    query_match_sequence = models.CharField(max_length=225,null=True)
    match_string = models.CharField(max_length=225, null=True)
    ref_match_sequence = models.CharField(max_length=225,null=True)
    edit_site_info = models.ForeignKey(edit_site_info)
    mirna_info = models.ForeignKey(mirna_info)

    def __str__(self):
        return self.mirna_id

class edit_sequence(models.Model):
    wild_sequence = models.TextField(null=True)
    wild_energy = models.FloatField(null=True)
    edit_squence = models.TextField(null=True)
    edit_energy = models.FloatField(null=True)
    delta_energy = models.FloatField(null=True)
    edit_site_info = models.ForeignKey(edit_site_info)

    def __str__(self):
        return  self.edit_energy

class resource(models.Model):
    lncrna_name = models.CharField(max_length=45,null=True)
    resource = models.CharField(max_length=45,null=True)
    description = models.TextField(null=True)
    link = models.TextField(null=True)
    lncrna_info = models.ForeignKey(lncrna_info)

    def __str__(self):
        return  self.lncrna_name

class repeat_conservation(models.Model):
    chromosome = models.CharField(max_length=45, null=True)
    chr_edit_pos = models.BigIntegerField()
    repeat = models.CharField(max_length=45, null=True)
    human = models.CharField(max_length=225, null=True)
    
    def __str__(self):
        return self.chromosome