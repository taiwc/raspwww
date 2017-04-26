<h1>Position 2D Count</h1>
<?php

  $x=$_GET['x'];
  $y=$_GET['y'];
  $d=$_GET['d'];

  if($x=="") {$r="200";}
  if($y=="") {$c="200";}
  if($d=="") {$d="Calibration";}


  $cmd="sudo python3 /var/www/Python/poscount.py";
  $args=" -x ".$x." -y ".$y." -d ".$d;
  
  $cmdall=$cmd.$args;
  echo '<h1>'.$cmdall.'</h1>';
  
  echo shell_exec($cmdall); 


?>
