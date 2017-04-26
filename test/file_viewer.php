<?php
  $filename=base64_decode($_GET['file']);
  echo file_get_contents($filename);  
?>
