$('document').ready(function(){
	$('.navOption').hover(
    function(){ //mouse over
      // $(this).css("background_color", "white");
      $(this).css('background-color', 'white');
    },
    function(){ //mouse away
      // $(this).css("background_color", "yellow");
      $(this).css('background-color', 'CCCCCC');
    }
    );
});