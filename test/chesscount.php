<h1>Chess Count</h1>
<?php
  $r=$_GET['r'];
  $c=$_GET['c'];
  $g=$_GET['g'];
  $d=$_GET['d'];
  $f=$_GET['f'];

  if($r=="") {$r="9";}
  if($c=="") {$c="6";}
  if($g=="") {$g="20.0";}
  if($d=="") {$d="Calibration";}
  if($f=="") {$f="Triggle??.jpg";}

  $cmd="sudo python3 /var/www/Python/chesscount.py";
  $args=" -r ".$r." -c ".$c." -g ".$g." -d ".$d." -f ".$f;
  
  $cmdall=$cmd.$args;
  echo '<h1>'.$cmdall.'</h1>';
  
  echo shell_exec($cmdall); 

  $calf= $d;
  $d0= $d."/"."ChessImg";
  $d1= $d."/"."UndistImg";
  $appUrl = $_SERVER['HTTP_HOST'];
  
  $pathcal ='dirimageshow.php'."?"."dir=".$calf;
  $appcal = 'http://'.$appUrl.'/'.$pathcal;
  echo '<h1>';
  echo '<a href='.$appcal.'>'.' Calibration Source Image'.'</a>';
  echo '</h>';

  $path0 = 'dirimageshow.php'."?"."dir=".$d0;
  $app0 = 'http://'.$appUrl.'/'.$path0;
  echo '<h1>';
  echo '<a href='.$app0.'>'.' Draw Chess Corner Image '.'</a>';
  echo '</h>';

  //header("Refresh:10;Location: ".$app0);

  $path1 = 'dirimageshow.php'."?"."dir=".$d1;
  $app1 = 'http://'.$appUrl.'/'.$path1;
  echo '<h1>';
  echo '<a href='.$app1.'>'.' Undistoretion Chess Image'.'</a>';
  echo '</h>';
  //header("Location: ".$app1);


?>
