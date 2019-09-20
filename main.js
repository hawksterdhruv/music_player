function resize_panels(){
  console.log('resize got called');
  current_panels = $(".resizable_panels");
  count = 0;
  current_panels.each(function(){count += (($(this).children().length > 0)?1:0)});
  console.log("width",95/count+"%")
  $(".resizable_panels").css("width",95/count+"%");
};

function create_panel(id,header,del=true) {
  $(id).append($(`<div  class="panel panel-default">
  <div class="panel-heading">
    `+header+ ((del) ? `<span class="glyphicon glyphicon-remove" onclick="$(this).parent().parent().remove(); resize_panels();"></span>` : ``) +
  `</div>
  <div class="panel-body">Panel Content</div>
</div>`));
  
};