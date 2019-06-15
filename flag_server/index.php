<?php

require 'config.php';

if(!isset($_REQUEST['post']) || empty($_REQUEST['post'])){
  $score_str = file_get_contents($record);
  $score_arr = explode('|', $score_str);
  arsort($score_arr);
  $result = [];
  foreach($score_arr as $k=>$row){
    $result_temp = [];
    $result_temp['id'] = $k;
    $result_temp['name'] = array_search($k, $token_list);
    $result_temp['ip'] = array_search($k, $ip_list);
    $result_temp['score'] = $row;
    $logarr = file('./logs.txt', FILE_IGNORE_NEW_LINES);
    array_push($result, $result_temp);
  }
  require 'assets/rote.html';
}else if($_REQUEST['post'] == 'listenlog'){
  $logs = [];
  $logarr = file('./log_temp.txt', FILE_IGNORE_NEW_LINES);
  foreach($logarr as $row){
    array_push($logs, json_decode($row));
  }
  file_put_contents('./log_temp.txt', "");
  if(!empty($logs)){
    echo json_encode($logs);
  }else{
    echo 'error';
  }
}
// var_dump($result);

?>
