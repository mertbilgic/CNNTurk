 //Jquerynin temel mantığını anlamak için yazdığım basit jquery kodları 
 $(document).ready(function(){

    $(".searchbtn").click(function(){
        console.log("searchbtn")
        if($(".searchbar").is(":visible")){
            $(".searchbar").hide();
            $("#himg").css({ opacity: 1 });
            $(".tag").show();
        }
        else{
            $(".searchbar").show();
            $("#search").focus();
            $("#himg").css({ opacity: 0.5 });
            $(".tag").hide();
        }
    });

    $(".mobil_ddownbtn").click(function(){
        console.log("mobil_ddownbtn")
        if($(".mobil_ddown").is(":visible")){
            $(".mobil_ddown").hide();
        }
        else{
            $(".mobil_ddown").show();
        }
    });
    $(".statisticbtn").click(function(){
        if($(".statistic").is(":visible")){
            $(".statistic").hide();
        }
        else{
            $(".statistic").show();
        }
    });
});
//Temel mantığı anlamak için bir parçayı jquery kullanmadan yaptım
var result=false;
var tagList=[];
//Sitedeki butonların statisticleri  id ye gönderiliyor

function statistic(){
    var text="<ul>";
    for(var i=2;localStorage.getItem(i)!=null;i++){
        text+="<li>"+i+".slide "+localStorage.getItem(i)+" kez tıklandı.</li>";
    }
    text +="</ul>";
    document.getElementById("ist-1").innerHTML=text;
}

function statisticList2(){
    var text="<ul>";
    for(var i=0;localStorage.getItem(tagList[i])!=null;i++){
        if(tagList[i]!="")
        text+="<li>"+tagList[i]+" "+localStorage.getItem(tagList[i])+" kez tıklandı.</li>";
    }
    text +="</ul>";
    document.getElementById("ist-2").innerHTML=text;
}
//Menubar classının görünürlüğünü ayarlıyorz
function menuBar(){
    console.log("menuBar");
    if(!result){
        document.getElementById("menuBar").style.display="block";
        result=true;
    }
    else{
        document.getElementById("menuBar").style.display="none";
        result=false;
    }
}
//Slider işlemleri burada gerçekleşiyor
var slideIndex = [1,1,1];
var slideId =["mySlides","mySlides2","mySlides3"];
showSlides(1,0);
showSlides(1,1);
showSlides(1,2);

function currentSlide(n,no) {
  showSlides(slideIndex[no] = n,no);
}
var count;
function showSlides(n,no) {
  if(n!=1&&(typeof(Storage) !== "undefined")){

      var str_count=localStorage.getItem(n);
      if(str_count==null||str_count=="null"){
       count=0;
      }
      else{
        count = parseInt(str_count);
      }
      count++;
      localStorage.setItem(n, count);

      console.log(n+".index"+localStorage.getItem(n));
  }
  var i;
  var slides = document.getElementsByClassName(slideId[no]);
  if (n > slides.length) {slideIndex[no] = 1}    
  if (n < 1) {slideIndex[no] = slides.length}
  
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";  
  }
  slides[slideIndex[no]-1].style.display = "block";
  statistic(); 

}
slideButton(0);
slideButton(1);
slideButton(2);
function slideButton(slideno){
    
    var slideId =["mySlides","mySlides2","mySlides3"];
    var slides=document.getElementsByClassName(slideId[slideno]);
    var text ="<ul>";
    for(i= 0; i<slides.length; i++){
        text +="<li><a onmouseover='currentSlide("+(i+1)+','+slideno+")'>"+(i+1)+"</a></li>";
    }
    text +="</ul>";
    document.getElementById(slideId[slideno]).innerHTML=text;

}
//Navbardaki bazı buton isimlerni dinamik olarak listeye eklemeyi sağlıyor
listAdd();
function listAdd(){
    var element = document.getElementById("tagList");
    var count=element.getElementsByTagName("A").length;
    console.log("Number:"+count);
    for(var i=0;i<count;i++){
    var index =element.getElementsByTagName("a")[i].textContent;
        tagList.push(index);
        console.log(tagList[i]);   
    }
}
//navbardaki butonlar tıklandığıda header.htmlden onclik metoduyla buton isimleri gönderiliyor kayıt işlemi yapılıyor
function statistic2(btnName){
    if((typeof(Storage) !== "undefined")){

        var str_count=localStorage.getItem(btnName);
        if(str_count==null||str_count=="null"){
         count=0;
        }
        else{
          count = parseInt(str_count);
        }
        count++;
        localStorage.setItem(btnName, count);
        statisticList2();
        statistic();
    }
}
