<h1>Pi Camera Triggle</h1>
<?php

  $cmd="sudo python3 /var/www/Calibration/picameraChess00.py";
  
  $cmdall=$cmd;
  echo '<h1>'.$cmdall.'</h1>';
  
  echo shell_exec($cmdall);
  
?>
