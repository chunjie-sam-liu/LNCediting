#!/usr/bin/perl 

#infile1  
=comment infile1 wild_targetscan_re
Gene_ID miRNA_family_ID species_ID      MSA_start       MSA_end UTR_start       UTR_end Group_num       Site_type       miRNA in this species   Group_type      Species_in_this_group        Species_in_this_group_with_this_site_type
NM_032291       hsa-let-7a-3p   9606    1169    1176    1169    1176    1       8mer-1a x       8mer-1a  9606

=comment infile2 wild_miranda_re
>hsa-let-7a-5p  NM_013943       156.00  -17.78  2 21    191 211 20      75.00%  80.00%
>>hsa-let-7a-5p NM_013943       156.00  -17.78  156.00  -17.78  5       22      3387     191

=comment infile3 snp_targetscan_re format same as wild_targetscan_re
NM_032291       hsa-miR-1236-3p_rs185147690     9606    1647    1653    1647    1653    1       7mer-1a  x       7mer-1a 9606

=comment infile4 snp_miranda_re
>hsa-miR-551a_rs187195064       NM_013943       155.00  -24.61  3 20    971 991 17      76.47%  94.12%
>>hsa-miR-551a_rs187195064      NM_013943       155.00  -24.61  155.00  -24.61  5       21      3387      971

=cut 
#use warnings;

($infile,$infile2,$infile3,$infile4,$outfile,$outfile2)=@ARGV ;
open(IN,$infile) or die "can't find $infile";
open(OUT,">$outfile") or die $!;
open (OUT2,">$outfile2") or die $!;
print OUT  join("\t", ("#miR", "TargetScan binding start", "TargetScan binding end", "miRanda binding start", "miRanda binding end", "score by miRanda", "binding energy predicted by miRanda")), "\n";
print OUT2 join("\t", ("#miR", "TargetScan binding start", "TargetScan binding end", "miRanda binding start", "miRanda binding end", "score by miRanda", "binding energy predicted by miRanda")), "\n";
while(<IN>){

	chomp;
	@data=split("\t",$_);
#	$gene=$data[0];
	$mir=$data[1];
	$h_line1{$mir}{$_}=$_;
	$h_wild{$mir}=$_;
}
close IN;
open(IN2,$infile2) or die $!;
while(<IN2>){
 if(/>>/){next;}
 if(!/>/){next;}
	chomp;
          @data2=split("\t",$_);
   #       $gene2=$data2[1];
          $mir2=$data2[0];
		  $mir2=~s/>//;
	$h_wild{$mir2}="";
	$h_line2{$mir2}{$_}=$_;
  }
close IN2;
open(IN3,$infile3) or die $!;
 while(<IN3>){
          chomp;
          @data3=split("\t",$_);
    #      $gene3=$data3[0];
         $mir3=$data3[1];
		# ($mir3,$snp3)=split(/_/,$mirsnp3);
		 
	$h_snp{$mir3}="";
	$h_line3{$mir3}{$_}=$_;
 }       
close IN3;
 open(IN4,$infile4) or die $!;
  while(<IN4>){
	   if(/>>/){next;}
	   if(!/>/){netx;}
          chomp;
            @data4=split("\t",$_);
     #       $gene4=$data4[1];
            $mir4=$data4[0];
		#	($mir4,$snp4)=split(/_/,$mirsnp4);
			$mir4=~s/>//;
	$h_snp{$mir4}="";
	$h_line4{$mir4}{$_}=$_;

 }       
close IN4;
foreach $mir (keys %h_line1){
	if (exists $h_line1{$mir} && exists $h_line2{$mir} && ! exists $h_line3{$mir} && ! exists $h_line4{$mir}){
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

 foreach $mir (keys %h_line3){
			  if (!exists $h_line1{$mir} && !exists $h_line2{$mir} &&  exists $h_line3{$mir} &&  exists $h_line4{$mir}){
				   foreach $line1 (keys %{$h_line3{$mir}}){
				foreach $line2 (keys %{$h_line4{$mir}}){
($t_start,$t_end)=(split/\t/,$line1)[3,4];
 my  @data2=split(/\t/,$line2);
 $data2[5]=~/(\d+)\s+(\d+)/;
 $m_start=$1;
 $m_end=$2;

	  if($t_start>=$m_start && $t_end<=$m_end){
	     print OUT2 "$mir\t$t_start\t$t_end\t$m_start\t$m_end\t$data2[2]\t$data2[3]\n";

		 		   }
		   }
	   }
   }
   }
