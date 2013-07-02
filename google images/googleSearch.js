google.load('search', '1');

      var imageSearch;

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
        $('button').click(function(){
           OnLoad($('input').val());
           $('input').text("");
          $('#count').text(str);
        });
        // var con=document.getElementById('content');
        // con.innerHTML='lksjdflksjld';
      });

      