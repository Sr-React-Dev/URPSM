function init_notif(){
	var LAST_NOTIF_URL  = "/" + window.LANGUAGE_CODE_JS + "/notifications/last/";
	var CHECK_NOTIF_URL = "/" + window.LANGUAGE_CODE_JS + "/notifications/check/";
	$("#notifications").on('click',function () {
	      $.ajax({
	        url: LAST_NOTIF_URL,
	        beforeSend: function () {
	          $('#notifs-list').dropdown('toggle');
	          $("#notifs-count").text('');
	          $("#notif-count").removeClass('notif_dot');
	        },
	        success: function (data) {
	          $("#notifs-list").html(data);
	        }
	      });
	    return false;
	  });
	//TODO: to Change by django-channels
	  
	  function check_notifications() {
	    $.ajax({
	      url: CHECK_NOTIF_URL,
	      cache: false,
	      success: function (data) {
	      	var notif=0;
	      	try{ notif=parseInt(data);}catch(e){notif=parseInt(data.innerHTML);}
	        if (notif > 0) {
	          $("#notifs-count").text(notif);
	          $("#notifs-count").addClass('notif_dot');
	          try{
	          	$('.notif-alert').text(notif);
	          	$('.notif-alert').show();
	          }catch(e){}
	        }
	        else {
	          $("#notifications").removeClass("notif_dot");
	          try{
	          	$('.notif-alert').hide();
	          }catch(e){}
	        }
	      },
	      complete: function () {
	        window.setTimeout(check_notifications, 30000);
	      }
	    });
	  };
  check_notifications();

}