<?php  
  $dirname=$_GET['dir'];
  if($dirname=="")
   $dir='/var/www';
  else
    $dir='/var/www/'.$dirname;
  $file_display=array('jpg','jpeg','png','gif');
  if(file_exists($dir)==false)
  {
    echo 'Directory \'',$dir,'\' not found!';
  }

  else
  {
    $dir_contents=scandir($dir);
    foreach($dir_contents as $file)
    {
      $file_type=strtolower(end( explode('.',$file)));
      if(($file!=='.') && ($file!=='..') && (in_array($file_type,$file_display)))
      {
        echo '<img src="file_viewer.php?file=',base64_encode($dir.'/'.$file),'" alt="',$file,'"/>';             
      }
      else
      {
        echo '<h1> "'.$file.'" is not image file!'.'</h1>';
      }
    }
  }
?>
