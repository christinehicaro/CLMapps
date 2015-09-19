$(document).ready(function(){

  {
     var watermark = 'City, State';
     $('#searchbarlocation').blur(function(){
      if ($(this).val().length == 0)
        $(this).val(watermark).addClass('watermark');
     }).focus(function(){
      if ($(this).val() == watermark)
        $(this).val('').removeClass('watermark');
     }).val(watermark).addClass('watermark');
  }

  {
     var watermark = 'Business Type';
     $('#searchbartype').blur(function(){
      if ($(this).val().length == 0)
        $(this).val(watermark).addClass('watermark');
     }).focus(function(){
      if ($(this).val() == watermark)
        $(this).val('').removeClass('watermark');
     }).val(watermark).addClass('watermark');
  }
}
