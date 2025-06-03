(function ( $ ) {
	function pad(n) {
	    return (n < 10) ? ("0" + n) : n;
	}

	$.fn.showclock = function(intervalId) {
		let currentDate = new Date();
		let fieldDate = $(this).data('date').split('-');
		let fieldTime = [0, 0];

		if ($(this).data('time') !== undefined) {
			fieldTime = $(this).data('time').split(':');
		}

		let futureDate = new Date(fieldDate[0], fieldDate[1] - 1, fieldDate[2], fieldTime[0], fieldTime[1]);
		let seconds = futureDate.getTime() / 1000 - currentDate.getTime() / 1000;
		if(seconds<=0 || isNaN(seconds)){
	    	this.hide();
			let productId = $(this).data("id"),
				requestUrl = $(this).data("url");
			clearInterval(intervalId);
			$.ajax({
				url: requestUrl,
				type: "GET",
				data: {"product_id": productId},
				success: function (response) {
					if (response.status === 200) {
						Swal.fire({
							position: "top-start",
							text: `فروش ویژه محصول ${response.product_name} به پایان رسید`,
							showConfirmButton: false,
							timer: 2500,
						}).then(() => {
							window.location.reload();
						});
					} else if (response.status === 400) {
						console.log("Product countdown ended with status code 400");
					} else {
						console.log("Product countdown ended with an unknown error");
					}
				},
				error: function (error) {
					console.log(error);
				},
			});
	    	return this;
	    }

		let days = Math.floor(seconds / 86400);
		seconds=seconds%86400;
	    
	    let hours=Math.floor(seconds/3600);
	    seconds=seconds%3600;

	    let minutes=Math.floor(seconds/60);
	    seconds=Math.floor(seconds%60);
	    
	    let html="";
 

	    html+="<div class='countdown-container seconds'>"
		html+="<span class='countdown-value seconds-bottom'>"+pad(seconds)+"</span>";
	    	html+="<span class='countdown-heading seconds-top'>ثانیه</span>";
	    html+="</div>";

		html+="<div class='countdown-container minutes'>"
		html+="<span class='countdown-value minutes-bottom'>"+pad(minutes)+"</span>";
	    	html+="<span class='countdown-heading minutes-top'>دقیقه</span>";
	    html+="</div>";

		html+="<div class='countdown-container hours'>"
		html+="<span class='countdown-value hours-bottom'>"+pad(hours)+"</span>";
	    	html+="<span class='countdown-heading hours-top'>ساعت</span>";
	    html+="</div>";

		if(days!==0){
		    html+="<div class='countdown-container days'>"
			html+="<span class='countdown-value days-bottom'>"+pad(days)+"</span>";
		    	html+="<span class='countdown-heading days-top'>روز</span>";
		    html+="</div>";
		}

	    this.html(html);
	};

	$.fn.countdown = function() {
		const el = $(this);
		let intervalId = setInterval(function(){
			el.showclock(intervalId);
		},1000);
		el.showclock(intervalId);
	}

}(jQuery));

jQuery(document).ready(function(){
	if(jQuery(".countdown").length>0){
		jQuery(".countdown").each(function(){
			jQuery(this).countdown();	
		})
		
	}
})