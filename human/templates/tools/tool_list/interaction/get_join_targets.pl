#!/usr/bin/perl 

#infile1  
=comment infile1 wild_targetscan_re
Gene_ID miRNA_family_ID species_ID      MSA_start       MSA_end UTR_start       UTR_end Group_num       Site_type       miRNA in this species   Group_type      Species_in_this_group        Species_in_this_group_with_this_site_type
NM_032291       hsa-let-7a-3p   9606    1169    1176    1169    1176    1       8mer-1a x       8mer-1a  9606

=comment infile2 wild_miranda_re
>hsa-let-7a-5p  NM_013943       156.00  -17.78  2 21    191 211 20      75.00%  80.00%
>>hsa-let-7a-5p NM_013943       156.00  -17.78  156.00  -17.78  5       22      3387     191

=cut 
#use warnings;

($infile,$infile2,$outfile)=@ARGV ;
open(IN,$infile) or die "can't find $infile";
open(OUT,">$outfile") or die $!;
print OUT join("\t", ("#miR", "TargetScan binding start", "TargetScan binding end", "miRanda binding start", "miRanda binding end", "score by miRanda", "binding energy predicted by miRanda")), "\n";
while(<IN>){

	chomp;
	@data=split("\t",$_);
#	$gene=$data[0];
	$mir=$data[1];
	$h_line1{$mir}{$_}=$_;
}
close IN;
open(IN2,$infile2) or die $!;
while(<IN2>){
 if(/>>/){next;}
 if(!/>/){next;}
	chomp;
          @data2=split("\t",$_);
          $mir2=$data2[0];
		  $mir2=~s/>//;
	$h_line2{$mir2}{$_}=$_;
  }
close IN2;

foreach $mir (keys %h_line1){
	if (exists $h_line1{$mir} && exists $h_line2{$mir} ){
	foreach $line1 (keys %{$h_line1{$mir}}){
	foreach $line2 (keys %{$h_line2{$mir}}){
	($t_start,$t_end)=(split/\t/,$line1)[3,4];
	my  @data=split(/\t/,$line2);
	$data[5]=~/(\d+)\s+(\d+)/;
	$m_start=$1;
	$m_end=$2;

if($t_start>=$m_start && $t_end<=$m_end){
	print OUT "$mir\t$t_start\t$t_end\t$m_start\t$m_end\t$data[2]\t$data[3]\n";
	}
	
}
}
}
}

