var inter = null
,   LIMIT = 500000;

function setStat() {
    var $this      = $('textarea')
    ,   text = tooMuch($this);

    var columnLine = text.substring(0, $this.prop('selectionStart'))
    ,   s          = columnLine.split(/\r*\n/)
    ,   lineNo     = s.length
    ,   colPos     = s[lineNo-1].length;

    $('.line-no.active').removeClass('active error');
    $('#stats-column span').html(colPos+1);

    if (lineNo) {
      $('#line-no-' + lineNo).addClass('active');
      $('#stats-line span').html(lineNo);
    }
    
    scrolling = false;
    $('.line-no').show();

    return {
      'lineNo'  : lineNo,
      'columnNo': colPos+1 
    }
}

function goto(lineNo, isError) {
  var lineNo = lineNo || 1
  ,   perH = $('.line-no:first').height()
  ,   sTop = Math.floor((perH * lineNo)-10);

  $('textarea').scrollTop(sTop); 
  
  setTimeout(function(){
      $('.line-no.active').removeClass('active');
      $('#line-no-'+ lineNo).addClass('active ' + (isError ? 'error' : ''));
  }, 10);
  
}

function tooMuch($this) 
{
  var text = $this.val();
  if (text.length > LIMIT) {

    alert('Warning: Too much length of data...'+ text.length +' chars (> '+ LIMIT +') ' + "\r\n" + 'Some data are truncated...'); 
    text = text.substring(0, LIMIT);
    $this.val(text);
  }

  return text;
}

function scroll() 
{

  scrolling = true;

  var $this = $('textarea')
  ,   text  = tooMuch($this);

  var   lines = text.split(/\r*\n/)
  ,   linesCount = lines.length
  ,   startLine = 1;


  var H    = $this.height()
  ,   perH = $('.line-no:first').height()
  ,   maxLines = Math.floor(H/perH)
  ,   sTop = $this.prop('scrollTop');

  if ($('.line-no:first').length > 0 && (sTop > perH) ) {
      // Overflow
      startLine = Math.floor(sTop/perH)+1;
      linesCount = startLine + maxLines;
      
  }else if(linesCount > maxLines) {
      linesCount = maxLines;
  }

  $('#line-nos').html('');
  for (var i = startLine; i <= linesCount; i++) {
    $('#line-nos').append('<div id="line-no-'+ i +'" class="line-no">'+ i +'</div>');
  }

  setStat($this);
}


$(document).on('ready', function(){

  $.fn.scrollStop = function(callback, timeout) {
    $(this).scroll(function(){
      var $this = $(this);
      if ($this.data('scrollTimeout')) {
        clearTimeout($this.data('scrollTimeout'));
        scrolling = false;
      }
      $this.data('scrollTimeout', setTimeout(callback, timeout));
    });
  }

  $('textarea').html($('#parsed-data').html());

  $('#stats-goto input').on('keyup', function(){
      var lineNo = $(this).val() || "";
      if (lineNo != '') {
        goto(lineNo);
      }
  });

  $('[name="stats_tab_select"]').on('change', function(){
    $('form').submit();
  })
  
  $('#clear-btn').on('click', function(){
    $('#json_inp').val('').html('').focus();
    $('.msg-box').remove();
    scroll();

  });

  $('textarea').on('keyup', function(e){
    var key = e.keyCode;
    clearInterval(inter);
    inter = window.setInterval(function(){
      clearInterval(inter);
      if ((key == 13 || key == 8 || key == 46 || key == 38 || key == 40) && !scrolling) { 
        // Enter        Backspace    Delete       Up           Down
        scroll();
      } else {  
        setStat();
      }
    }, 0);
    
  });

  /*$('textarea').scrollStop(function(){
      if (!scrolling) {
        scroll();
      }
  }, 50);*/

  $('textarea').on('scroll', function(){
    scroll();
  })

  $('#json-inp-block').on('click', function(){
    setStat();
  })

  scroll();

  /** Mark down the error line **/
  if ($('#err-line-no').val() > 0) {
    goto($('#err-line-no').val(), true);
  }

})