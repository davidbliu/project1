google.load('search', '1');
var searchTerm;
var page=0;
var tableRows=3;
var tableCols=7;
var numAdded=0;
var row=0;
var col=0;
var imageSearch;
var size=80;
var numForms=10;

function createTable(){
  var table=document.getElementById('table');
  for(var i=0;i<tableRows;i++){
    var row=table.insertRow(0);
    for(var j=0;j<tableCols;j++){
      var cell=row.insertCell(j);
      cell.height=size;
      cell.width=size;
      cell.className='imageContainer';
    }
  }
}
function searchComplete() {
  if (imageSearch.results && imageSearch.results.length > 0) {
    var results = imageSearch.results;
    var table=document.getElementById('table');
    for (var i = 0; i < results.length; i++) {
      var result = results[i];
      // var imgContainer=document.createElement('div');
      // imgContainer.className='imgContainer';
      var newImg = document.createElement('img');
      newImg.src=result.unescapedUrl;
      newImg.height=size;
      newImg.width=size;
      // imgContainer.appendChild(newImg);
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
function addToTable(r, c, object){
  var table=document.getElementById('table');
  var rows=table.getElementsByTagName('tr');
  var row=rows[r];
  var cols=row.getElementsByTagName('td');
  var cell=cols[c];
  cell.innerHTML="";
  cell.appendChild(object);
}
function OnLoad(term) {
  imageSearch = new google.search.ImageSearch();
  imageSearch.setResultSetSize(8);
  imageSearch.setSearchCompleteCallback(this, searchComplete, null);
  imageSearch.execute(term);
}

google.setOnLoadCallback(function(){
  createTable();

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
        height:'+=25px',
        width:'+=25px',
        // $('#buttons').clone().appendTo(this);
      });
      var b=document.createElement('input');
      b.type='submit';
      b.id='asdf';
      b.name='submit';
      b.value='add';
      $(this).append(b);
    },
    function(){
      $(this).stop(true,true).height(size);
      $(this).stop(true,true).width(size);
      $('#asdf').remove();
    });
  

}); //end of the google thing

      