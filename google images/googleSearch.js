google.load('search', '1');

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
    }
  }
}
function searchComplete() {
  if (imageSearch.results && imageSearch.results.length > 0) {
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
}

google.setOnLoadCallback(function(){
  createTable();
  $('button').click(function(){
     OnLoad($('input').val());
     $('input').text("");
    $('#count').text(str);
  });
});

      