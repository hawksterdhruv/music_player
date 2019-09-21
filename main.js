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

function create_player_panel(id,header,del=true) {
  $(id).append($(`<div  class="panel panel-default">
  <div class="panel-heading">
    `+header+ ((del) ? `<span class="glyphicon glyphicon-remove" onclick="$(this).parent().parent().remove(); resize_panels();"></span>` : ``) +
  `</div>
  <div class="panel-body">
    
    <div id="visual_panel">
      <div class="panel panel-default" style="width:83%;float:left;">
        <div class="panel-body">
          Panel Content
        </div>
      </div>
      
      <div class="panel panel-default" style="width:13%;float:left;">
        <div class="panel-body">
          <span class="glyphicon glyphicon-repeat" style=" clear: left; display: block;"></span>
          <span class="glyphicon glyphicon-random" style=" clear: left; display: block;"></span>
        </div>
      </div>


    </div>  
    </div><div style="clear:both;"></div>
    <div id="seek_panel">
      <span><input type="range" min="1" max="100" value="50" class="slider"/></span>
      <span><button id="library_button" class="btn btn-primary btn-xs">ML</button></span>
      <span><button id="playlist_button" class="btn btn-primary btn-xs">PL</button></span>
    </div><div style="clear:both;"></div>
    <div id="controls_panel">
      <span id="backward-button" class="glyphicon glyphicon-backward"></span>
      <span id="play-button" class="glyphicon glyphicon-play"></span>
      <span id="pause-button" class="glyphicon glyphicon-pause"></span>
      <span id="stop-button" class="glyphicon glyphicon-stop"></span> 
      <span id="forward-button" class="glyphicon glyphicon-forward"></span>
      <span class="glyphicon glyphicon-volume-up"></span>
      <span class="glyphicon glyphicon-volume-off"></span>
      <span><input type="range" min="1" max="100" value="50" class="slider"/></span>
    </div><div style="clear:both;"></div>
  </div>
</div>`));
  
};