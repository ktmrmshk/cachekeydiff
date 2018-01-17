$(document).ready(function(){
  var g_ret=123;
  $('[data-toggle="tooltip"]').tooltip();

  $('#get_server_names').click(function(){
    //alert( $("#hostname").val());
    //$("#serverA").val( $("#hostname").val() );
    var dp = $("#hostname").val();
    var path = '/' + dp + '/edgehostname/';
    $.get(path, function(data, status){
      //alert(data.edgehostname.prod + ':' + status);
      $("#serverA").val(data.edgehostname.stg);
      $("#serverB").val(data.edgehostname.prod);
    });
  });

  $('#get_urls').click(function(){
      var basepage = $("#protocol").val() + $("#hostname").val();
      var path =  '/cdiff/urllist/?basepage=' + encodeURIComponent(basepage);
      //alert(path);
      $.get(path,  function(data, status){
        g_ret=data;
        for(var p in data){
          console.log(data[p]);
          $("#urllist").val( $("#urllist").val() + data[p] + "\n" );
        }  
      });
  });

  $("#dodiff").click(function(){ 
    //alert(g_ret);
    var txt = $("#urllist").val();
    var urllist = txt.split("\n");
    console.log(urllist);

  });

});
