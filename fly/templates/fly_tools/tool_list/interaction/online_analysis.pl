#!/usr/bin/perl
#gongjing 2013-06-11 used to get the target gain and loss;
use File::Basename;

$seq1=$ARGV[0];
if($ARGV[2]){
$seq2=$ARGV[1];
$uniq_code=$ARGV[2];
}else{
$seq2="";
$uniq_code=$ARGV[1];
}

$datafile = dirname(__FILE__);
$resultfile = dirname(dirname($datafile)) . "/tool_result/interaction_result/";
$mir_m="$datafile/fly_miR_for_M";
$mir_t="$datafile/fly_miR_for_T";
$data_file=$resultfile;
$targetscan="$datafile/targetscan_60.pl";
$target_G_L_pl="$datafile/get_target_G_L_online.pl";
$get_join_targets="$datafile/get_join_targets.pl";
$seq1_for_M=$data_file."seq1_for_M";
$seq1_for_T=$data_file."seq1_for_T";
$seq2_for_M=$data_file."seq2_for_M";
$seq2_for_T=$data_file."seq2_for_T";
$seq_target_loss=$data_file."seq_target_loss.".$uniq_code;
$seq_target_gain=$data_file."seq_target_gain.".$uniq_code;
$seq1_target=$data_file."seq1_target.".$uniq_code;
$seq2_target=$data_file."seq2_target.".$uniq_code;



open(OUT1,">$seq1_for_M") ;
open(OUT2,">$seq1_for_T") ;
open(OUT3,">$seq2_for_M") ;
open(OUT4,">$seq2_for_T") ;

$seq1=~s/[^ACTGUactgu]//;
$seq2=~s/[^ACTGUactgu]//;
print OUT1 ">SEQ1\n$seq1\n";
print OUT2 "SEQ1\t9606\t$seq1\n";
print OUT3 ">SEQ2\n$seq2\n";
print OUT4 "SEQ2\t9606\t$seq2\n";

$seq1_Targetsccan_re=$data_file."seq1_re_T";
$seq2_Targetsccan_re=$data_file."seq2_re_T";
$seq1_Miranda_re=$data_file."seq1_re_M";
$seq2_Miranda_re=$data_file."seq2_re_M";

`perl $targetscan $mir_t $seq1_for_T  $seq1_Targetsccan_re` or die 1;
`$datafile/miranda $mir_m $seq1_for_M -en -10 > $seq1_Miranda_re`;
if($ARGV[2]){
`perl $targetscan $mir_t  $seq2_for_T  $seq2_Targetsccan_re` or die '3';
`$datafile/miranda $mir_m  $seq2_for_M -en -10 >$seq2_Miranda_re`;
`perl $target_G_L_pl $seq1_Targetsccan_re $seq1_Miranda_re $seq2_Targetsccan_re $seq2_Miranda_re $seq_target_loss $seq_target_gain` and die '5';
`perl $get_join_targets $seq1_Targetsccan_re $seq1_Miranda_re $seq1_target`;
`perl  $get_join_targets $seq2_Targetsccan_re $seq2_Miranda_re $seq2_target`;
}else{
`perl $get_join_targets $seq1_Targetsccan_re $seq1_Miranda_re $seq1_target`;
}
`chmod 777 $data_file/*`
#`find ../online_result/ -type f -mtime +0.1 -exec rm -f {} \;`
