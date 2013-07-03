google.load('search', '1');
<<<<<<< HEAD
var searchTerm;
var page=0;
var tableRows=3;
var tableCols=7;
var numAdded=0;
var row=0;
var col=0;
var imageSearch;
var size=80;
function createButtons(){
  var div=document.createElement('div');
  div.className='buttonDiv';
  for(var i=1;i<6;i++){
    var b=document.createElement('button');
    b.className='rateButton';
    b.innerHTML=i;
    div.appendChild(b);
  }
  return div;
}
function createTable(){
  var table=document.getElementById('table');
  for(var i=0;i<tableRows;i++){
    var row=table.insertRow(0);
    for(var j=0;j<tableCols;j++){
      var cell=row.insertCell(j);
      cell.height=size;
      cell.width=size;
      cell.className='imageContainer';
=======

var imageSearch;
function createTable(){
  var table=document.getElementById('table');
  for(var i=0;i<5;i++){
    var row=table.insertRow(0);
    for(var j=0;j<7;j++){
      var cell=row.insertCell(j);
      cell.height=100;
      cell.width=100;
      cell.innerHTML="blank";
>>>>>>> 153b7a5afd833f10d501235c03ccc98730f91d89
    }
  }
}
function searchComplete() {
  if (imageSearch.results && imageSearch.results.length > 0) {
<<<<<<< HEAD
    var results = imageSearch.results;
    var table=document.getElementById('table');
    for (var i = 0; i < results.length; i++) {
      var result = results[i];
      var newImg = document.createElement('img');
      newImg.src=result.unescapedUrl;
      newImg.height=size;
      newImg.width=size;
      if(numAdded<tableCols*tableRows){
        addToTable(row, col, newImg);
        numAdded++;
        col=col+1;
        if(col>=tableCols){
          col=0;
          row=row+1;
        }
      }
      
    }
    if(row < tableRows){
      page+=1;
      imageSearch.gotoPage(page);
    }
  }
}
function addToTable(r, c, image){
  var table=document.getElementById('table');
  var rows=table.getElementsByTagName('tr');
  var row=rows[r];
  var cols=row.getElementsByTagName('td');
  var cell=cols[c];
  cell.innerHTML="";
  cell.appendChild(image);
}
function OnLoad(term) {
  imageSearch = new google.search.ImageSearch();
  imageSearch.setResultSetSize(8);
  imageSearch.setSearchCompleteCallback(this, searchComplete, null);
  imageSearch.execute(term);
=======
    var contentDiv = document.getElementById('content');
    var results = imageSearch.results;
    for (var i = 0; i < results.length; i++) {
      var result = results[i];
      var imgContainer = document.createElement('div');
      var newImg = document.createElement('img');
      newImg.src=result.url;
      newImg.height=100;
      newImg.width=100;
      imgContainer.appendChild(newImg);
      contentDiv.appendChild(imgContainer);
    }
  }
}

function OnLoad(a) {
  imageSearch = new google.search.ImageSearch();
  imageSearch.setSearchCompleteCallback(this, searchComplete, null);
  imageSearch.execute(a);
>>>>>>> 153b7a5afd833f10d501235c03ccc98730f91d89
}

google.setOnLoadCallback(function(){
  createTable();
<<<<<<< HEAD

  $('#search').click(function(){
    col=0;
    row=0;
    numAdded=0;
    searchTerm=$('input').val();
     OnLoad(searchTerm);
     $('input').text("");
  });
  $('.test').click(function(){
    alert();
  });//end of the testdiv thing
  $('.imageContainer').hover(
    function(){
      $(this).stop(true,true).animate({
        height:'+=50px',
        width:'+=100px'
        // $('#buttons').clone().appendTo(this);
      });
      var buttons=createButtons();
      buttons.id="asdf"
      $(this).append(buttons);
    },
    function(){
      $(this).stop(true,true).height(size);
      $(this).stop(true,true).width(size);
      $('#asdf').remove();
    });
  $('li').hover(
    function(){ //mouse over
      // $(this).css("background_color", "white");
      $(this).css('background-color', 'white');
    },
    function(){ //mouse away
      // $(this).css("background_color", "yellow");
      $(this).css('background-color', 'CCCCCC');
    }
    );
  

}); //end of the google thing
=======
  $('button').click(function(){
     OnLoad($('input').val());
     $('input').text("");
    $('#count').text(str);
  });
});
>>>>>>> 153b7a5afd833f10d501235c03ccc98730f91d89

      