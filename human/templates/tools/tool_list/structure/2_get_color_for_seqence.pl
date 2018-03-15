#!/usr/bin/perl
#2010-7-16,gongj used to color the snp location;
use File::Basename;
($infile)=@ARGV;
open (IN,$infile) or die "cant open $infile\n";

while (<IN>){
my @score="";
chomp;
@data=split("\t",$_);
$data_file = dirname(__FILE__)."/";
$outfile=$data_file.$data[0];
$length=length $data[1];
$seq=$data[1];
$s=$data[2];

for ($i=0;$i<$length;$i++){
$i == $s? push @score, (1):push @score ,(0.4);
}


$snew=join (",",@score);
$m=$data[0];
$snew=~s/^\,//;
`python $data_file/plot.py -o $outfile -s $snew  $seq`;
}

