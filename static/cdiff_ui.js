
$(document).ready(function(){




  function add_retrow(idx, url, hdrs){
  var row = document.createElement("tr");
  row.innerHTML = col_num(idx) + col_url(url) + col_headers(hdrs);
  $("#retable").append(row);
}

function col_num(idx){
  return '<td>' + idx + '</td>';
}

function col_url(url){
  return '<td class="small">' + url + '</td>';
}

function col_headers(hdrs){
  var ret='<td>';
  
  for(var k in hdrs){
    if( k == 'diff' || k == 'etag'){
      continue;
    }
    ret += header_budge(k, hdrs[k]);
    console.log(hdrs[k].prod);
  }
  
  ret += '</td>';
  return ret;
}

function header_budge(hdrkey, hdr){
//  hdrkey: cache-control
//  hdr: {
//      "match": true, 
//      "prod": "public", 
//      "stg": "public"
//       }
  var ret = "";
  var color = "badge-success";
  if( ! hdr.match ){
    color = "badge-danger";
  }
  ret += tooltip_pre(hdr);
  ret += '<span class="badge ' + color + '">';
  ret += hdrkey;
  ret += '</span>';
  ret += '</a>';
  return ret;
}

function tooltip_pre(hdr){
  var ret='<a href="#" data-toggle="tooltip" data-container="body" data-html="true" data-placement="bottom" title="';
  ret += '<tr>';
  ret += '<td><b>ServerA:</b> </td>';
  ret += '<td>' + hdr.prod + '</td>';
  //ret += '<td>' + hdr.prod.replace(/"/g, "") + '</td>';
  ret += '</tr>';
  ret += '<tr>';
  ret += '<td><b>ServerB:</b> </td>';
  ret += '<td>' + hdr.stg + '</td>';
  ret += '</tr>';
  ret += '">';
  return ret;
}


  
  
  
  
  
  var g_ret=123;
  $('[data-toggle="tooltip"]').tooltip();

  $('#get_server_names').click(function(){
    //alert( $("#hostname").val());
    //$("#serverA").val( $("#hostname").val() );
    var dp = $("#hostname").val();
    var path = '/' + dp + '/edgehostname/';
    $.get(path, function(data, status){
      //alert(data.edgehostname.prod + ':' + status);
      $("#serverB").val(data.edgehostname.stg);
      $("#serverA").val(data.edgehostname.prod);
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


  function makeGetProc(idx, url){
    return function(data, status){
      add_retrow(idx, url, data);
      $('[data-toggle="tooltip"]').tooltip();
      $("#stat_console").text("done...");
    };
  }


  $("#dodiff").click(function(){ 
    var txt = $("#urllist").val();
    var urllist = txt.split("\n");
    var j=0;
    for(var i=0; i<urllist.length; i++){
      var re = new RegExp("^(http|https):\/\/" + $("#hostname").val() + "\/.*");// /(http|https):\/\/www.jins.com\/.*/
      if( ! re.test(urllist[i]) ){
        console.log('passed');
        continue;
      }

      console.log("u=" + urllist[i]);

      var url = encodeURIComponent( urllist[i] );
      var servera = encodeURIComponent( $("#serverA").val() );
      var serverb = encodeURIComponent( $("#serverB").val() );
      var query = '?url=' + url + '&serverA=' + servera + '&serverB=' + serverb;
      var path = '/cdiff/diff/' + query;
      
      var getProc=makeGetProc(++j, urllist[i]);
      //var bs= ( function(url){ 
      //  return function(){$("#stat_console").text(url);}; 
      //}(urllist[i]));
      $.get( path, getProc);
      //$.ajax({
      //  url: path,
      //  complete: getProc,
      //  beforeSend: bs,
      //  async: false
      //});
    }


  });

});
