<?php
  $filename=$_GET['file'];
  if(file_exists($filename)==false)
  {
    echo $filename." not found!";
  }
  else
  {
    echo file_get_contents($filename);  
  }
?>
