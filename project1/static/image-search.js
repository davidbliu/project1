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
var index=0;
var formsWrappers=document.getElementsByClassName("iBox");

function searchComplete() {
  if (imageSearch.results && imageSearch.results.length > 0) {
    var results = imageSearch.results;
    for (var i = 0; i < results.length; i++) {
      var result = results[i];
      var newImg = document.createElement('img');
      newImg.className='image';
      newImg.src=result.unescapedUrl;
      newImg.height=size;
      newImg.width=size;
      if (formsWrappers[index]) {
        formsWrappers[index].appendChild(newImg);
        var input=document.getElementById('id_image');
        input.value=newImg.src;
        input.id='n'+input.id;
        var b=document.createElement('input');
        b.type='submit';
        b.value='add to db';
        b.name='submit';
        formsWrappers[index].appendChild(b);
        // formsWrappers[index].innerHTML=newImg.src;
        index++;
      }
    }
    if(index < numForms){
      page+=1;
      imageSearch.gotoPage(page);
    }
  }//end of if results
 }//end of search complete

function OnLoad(term) {
  imageSearch = new google.search.ImageSearch();
  imageSearch.setResultSetSize(8);
  imageSearch.setSearchCompleteCallback(this, searchComplete, null);
  imageSearch.execute(term);
}

google.setOnLoadCallback(function(){

  // $('#id_image').val('fuck1');

  $('#search').click(function(){
    index=0;
    searchTerm=$('input').val();
     OnLoad(searchTerm);
     $('input').text("");
  });
  

}); //end of the google thing

      