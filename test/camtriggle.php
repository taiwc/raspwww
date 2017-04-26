<h1>Pi Camera Triggle</h1>
<?php
  $w=$_GET['w'];
  $h=$_GET['h'];
  $s=$_GET['s'];
  $i=$_GET['i'];
  $d=$_GET['d'];

  if($w=="") {$w="0";}
  if($h=="") {$h="0";}
  if($i=="") {$i="1";}
  if($s=="") {$s="0";}
  if($d=="") {$d="image";}

  //$cmd="sudo python3 /var/www/Python/picCam_Triggle.py";
  $cmd="sudo /var/www/Python/dist/picCam_Triggle";
  $args=" -w ".$w." -h ".$h." -s ".$s." -d ".$d." -i ".$i;
  
  $cmdall=$cmd.$args;
  echo '<h1>'.$cmdall.'</h1>';
  
  echo shell_exec($cmdall);
  
?>
