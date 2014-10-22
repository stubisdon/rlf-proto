var global = { firstH: $(window).height(), old: 0, oTop: 0, play: false, task: false, inputhover: false, lastIcon: null, closers: [], reqi: 0, req: false, reqspeed: 3000, fbcancel: false, fbloop: null, fbuser: 0, fbgender: null, fbat: null, incancel: false, inloop: null, inat: null, inuser: 0, inimage: null, inflag: false, anim: null, anim2: null  };
var types = [	["ь", "и", "ей"], // не редактировать
				["место", "места", "мест", "ходите в одно и то же место"], // 1
				["блюдо", "блюда", "блюд", "любите одно и то же блюдо"], // 2
				["фильм", "фильма", "фильмов", "смотрели один и тот же фильм"], //3
				["книга", "книги", "книг", "читали одну и ту же книгу"], //4
				["лайк", "лайка", "лайков", "лайкаете одно и то же"] //5
			];
Zepto(function($){

	OAuth.initialize('l_apl0rGv3ODyhXFCHLj16EdcyY');

	$(".iphone-black").removeClass("white");
	$("#second").hide().css("opacity", 1);

	var switcher = function (i, d) {
		if(i!==null && i!==global.old) {
			switch(i){
				case 0:
					$(".stripes").removeClass("zero").addClass("anim");
					setTimeout(function(){
						$(".stripes").removeClass("anim");
					}, 201);
					$(".stripes .yel").css("margin-top", 0);
					$(".stripes .blu").css("margin-top", 0);
					$(".stripes .gre").css("margin-top", 0);
				break;
				case 1:
					$(".stripes").addClass("zero");
					if(global.old === 2 && d==="up"){
						$("#main-video").show();
						$("#second").hide();
					}
				break;
				case 2:
					$(".stripes").addClass("fixed");
					if(global.old === 1 && d==="down"){
						$("#main-video").hide();
						$("#second").show();
					}else if(global.old === 3 && d==="up"){
						$("#main-video").show();
						$("#second").hide();
					}
				break;
				case 3:
					if(global.old === 2 && d==="down"){
						$("#main-video").hide();
						$("#second").show();
					}
				break;
				case 4:
					if(d==="up") $(".scroll-down").addClass("r").removeClass("w");
				break;
				case 5:
					if(d==="down") $(".scroll-down").addClass("w").removeClass("r");
				break;
				case 6:
					$(".d").removeClass("d");
				break;
			}
			global.old = i;

			//double check
			if(i!==0) {
				$("#main-video .data").removeClass("h");
				$("#main-video .dataH").addClass("h");
				$("#main-video .video").html('');
				$(".subscribe").removeClass("night");
			}
			if(i!==2) $(".stripes").removeClass("fixed");

			if(i!==3 && i!==4) $(".first-info").css("transform", "translateY(100%)");
			else $(".first-info").css("transform", "translateY(0%)");

			if(i!==6) {
				$(".nfl, .surf, .surf-shadow, .books").addClass("fast").addClass("d");
				setTimeout(function(){
					$(".nfl, .surf, .surf-shadow, .books").removeClass("fast");
				}, 101);
			}else{
				$(".iphone-black .screen").css("background-position", "0 -382px");
			}

			if(i!==12) cancelFacebook();

			if(i<5 || i>7) $(".sloganp").css("opacity", 0);

			if(i>4 && i<7) $(".scroll-down").css("opacity", 1);
			if(i>6 || i<4) $(".scroll-down").css("opacity", 0);
			if(i<4){$("#second").css("transform", "translateY(0)!important");
					$(".white-board").css("bottom", "-100%");
					$("#second .circles").css("opacity", 1);
					$(".iphone-black").css("transform", "translateY(150%)");}

			if(i>5) $(".white-board").css("bottom", "100%");
			if(i<5) $(".pink-board").css("bottom", "-200%");

			if(i>7){$(".pink-board").css("bottom", "200%");
					$(".iphone-black").css("right","50%");}

			if(i>2) { $("#main-video").hide(); $("#second").show(); }
			if(i<2) { $("#main-video").show(); $("#second").hide(); }

			if(i>4){$("#second").hide();
					$(".iphone-black").css("transform", "translateY(0%)");}

			if(i>10) $(".iphone-black .screen").css("background-position", "0 -1146px");

			if(i>11) {
				$(".iphone-black").css("transform", "translateY(-130%)");
				$(".loaders").css("top", 0);
			}

			if(i<11) $(".loaders").css("top", "100%");

			if(i<12) $(".container").removeClass("grey");
			else $(".container").addClass("grey");

			if(i<13) $(".footer").css("top", "100%");

			if(i<7) {
				$(".iphone-black").removeClass("white");
				$(".iphone-black").css("right","30%");
			}else {
				$(".iphone-black").addClass("white");
			}

			if(i>3 && i<8) $(".board").css("opacity", 1);
			else $(".board").css("opacity", 0);

			if(i<8 || i>11) $(".black-funeral-shit").css("opacity", 0);
			else $(".black-funeral-shit").css("opacity", 1);

		}
	}

	var scroll = function () {
		var top = $(window).scrollTop(),
			h = $(window).height(),
			c = null,
			d = top >= global.oTop ? 'down' : 'up',
			u = Math.ceil(top/h);

		global.oTop = top;
		switcher(u, d);

		$(".container").css("height", h*15+1+"px");

		if(top>0 && top<h) {
			var o = h-top;
			$(".stripes .yel").css("margin-top", (o/0.75)+"px");
			$(".stripes .blu").css("margin-top", (o/0.5)+"px");
			$(".stripes .gre").css("margin-top", (o/0.25)+"px");
		}

		if(top>=h && top<h*2){
			var o = h*2-top < h/4 ? (h*2-top)/(h/4) : 1;
			$(".stripes .red > *").css("opacity", o.toFixed(2));
			$(".stripes .yel > *").css("opacity", o.toFixed(2));
			$(".stripes .blu > *").css("opacity", o.toFixed(2));
			$(".stripes .gre > *").css("opacity", o.toFixed(2));
		}

		if(top>=h*2 && top<h*3){
			var o = h*2-top;
			$(".stripes .yel").css("margin-top", (o/0.75)+"px");
			$(".stripes .blu").css("margin-top", (o/0.5)+"px");
			$(".stripes .gre").css("margin-top", (o/0.25)+"px");
		}

		if(top>=h*3 && top<h*4){
			var o = (h*4-top)/(h/100);
			$(".iphone-black").css("transform", "translateY("+(o.toFixed(2)/100*150)+"%)");
		}

		if(top>=h*3 && top<h*5){
			var o = (h*4-top)/(h/100);
			$(".white-board").css("bottom", -o.toFixed(2)+"%");

			if(o>80) {
				$("#second").css("transform", "translateY(-"+(100-o.toFixed(2))+"%)!important");
			}else{
				$(".scroll-down").css("opacity", 1-o.toFixed(2)/80);
				$("#second").css("transform", "translateY(-20%)!important");
			}

			if(o>15){
				$("#second .circles").css({opacity: (o.toFixed(2)-15)/15});
			}else{
				$("#second .circles").css({opacity: 0});
			}
		}

		if(top>=h*4 && top<h*5){
			var o1 = h/2-150,
				o2 = h/2+224;

			o = top%h;
			if(o>=o1 && o<=o2){
				var r = (o-o1)/(o2-o1)*382;
				$(".iphone-black .screen").css("background-position", "0 -"+r+"px");
			}else if(o<o1){
				$(".iphone-black .screen").css("background-position", "0 0px");
			}else if(o>o2){
				$(".iphone-black .screen").css("background-position", "0 -382px");
			}
		}

		if(top>=h*6 && top<h*11){
			var o = top/h,
				r, t;
			if(o>7){
				r = (o.toFixed(2)-7)*382;
				t = 100-(o-7)/3*100;
			}else{
				r = 0;
				t = 100;
			}

			if(o>10) r = -1146;


			$(".black-funeral-shit .big").removeClass("h").addClass("h");
			if(o<8.4){
				$(".black-funeral-shit .b1").removeClass("h");
			}else if(o>=8.4 && o<=9.5) {
				$(".black-funeral-shit .b2").removeClass("h");
			}else{
				$(".black-funeral-shit .b3").removeClass("h");

			}

			$(".black-funeral-shit").css("top", t.toFixed(2)+"%");
			$(".iphone-black .screen").css("background-position", "0 -"+r+"px");
		}

		if(top>=h*10 && top<h*11){
			var o = (h*11-top)/h;
			$(".iphone-black").css("transform", "translateY(-"+(1-o.toFixed(2))*130+"%)");
			$(".loaders").css("top", o.toFixed(2)*100+"%");
		}

		if(top>=h*12 && top<h*14){
			var o = (h*13-top)/h;
			$(".loaders").css("top", -(1-o.toFixed(2))*100+"%");
			$(".footer").css("top", o.toFixed(2)*100+"%");
		}

		if(top>=h*13) $(".footer").css("top", 0);

		if(top>=h*4 && top<h*7){
			var o = (h*6-top)/(h/100);
			if(o<170) $(".sloganp").css("opacity", 1-(o-150)/20);
			if(o<0) $(".sloganp").css("opacity", (o+65)/65);
			$(".pink-board").css("bottom", -o.toFixed(2)+"%");
		}

		if(top>=h*6 && top<h*7){
			var o = (h*7-top)/(h/20);
			$(".iphone-black").css("right", 50-o.toFixed(2)+"%");
		}

		if(top>=h*2 && top<h*4){
			var o = Math.ceil((h*5-top)/h*180),
				d = 180-o,
				a = [0, 45, 90, 135, 180, 225, 270, 315],
				r = [315, 270, 225, 180, 135, 90, 45, 0];

			for (var i = 0; i < a.length; i++) {
				if(Math.abs(d) > a[i]-8 && Math.abs(d) < a[i]+8 && !$(".action-circle").hasClass("bounceIn")) {
					if(global.lastIcon!==a[i]){
						global.lastIcon = a[i];
						$(".action-circle").addClass("bounceIn").css({ backgroundColor: '#ff3b57' });
						$(".question").animate({opacity: 0.0001}, 100);
						$(".action-circle").one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
							$(".action-circle").removeClass("bounceIn").css({ backgroundColor: '#fff' });
							$(".question").animate({opacity: 1}, 100);
						});
					}
				}

				var x = a[i]+d>=360 ? a[i]+d-360 : a[i]+d;
					x = x<0 ? x+360 : x;
				$(".left-circle .n"+(i+1)).css("transform", "rotate("+x+"deg) translate(125px) rotate(-"+x+"deg)");
			}

			for (var i = 0; i < r.length; i++) {
				var x = r[i]-d<=0 ? r[i]-d+360 : r[i]-d;
				$(".right-circle .n"+(i+1)).css("transform", "rotate("+x+"deg) translate(125px) rotate(-"+x+"deg)");
			}
		}

		// dev

		$("#score").html(top);
		$("#score2").html(h);
		$("#score3").html(u);
	};
  
	$(window).on('scroll', scroll, true);

	$(".stripes > *").click(function(){
		var h = $(window).height();
		$(window).scrollToTop(h+1);
	});

	$("#main-video .dataH").click(function(){
		if(global.play){
			global.play = false;
			$(".close").click();
		}
	});

	$("#main-video").on("mouseenter", ".top-input", function(){
		global.inputhover = true;
	});

	$("#main-video").on("mouseleave", ".top-input", function(){
		global.inputhover = false;
	});

	var inputBtnAnimation = function(){
		if(!global.inputhover){
			$(".top-input .button").addClass("anim");
			setTimeout(function(){
				$(".top-input .button").removeClass("anim");
				setTimeout(function(){
					$(".top-input .button").addClass("anim");
					setTimeout(function(){
						$(".top-input .button").removeClass("anim");
						setTimeout(function(){
							$(".top-input .button").addClass("anim");
							setTimeout(function(){
								$(".top-input .button").removeClass("anim");
							},400);
						},400);
					},400);
				},400);
			},400);
		}
	}

	setInterval(inputBtnAnimation, 10000);
	inputBtnAnimation();

	$(".play").click(function(){
		$(window).scrollToTop(0);
		global.play = true;

		setTimeout(function(){
			$(".container").addClass("grey");
			$(".subscribe").addClass("night");
			$("#main-video .data").addClass("h");
			$("#main-video .dataH").removeClass("h");
			$("#main-video .video").html('<iframe src="//player.vimeo.com/video/107532259?byline=0&amp;portrait=0&amp;autoplay=1" width="100%" height="100%" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>');
		}, 200);
	});

	$(".close").click(function(){
		$(".container").removeClass("grey");
		$("#main-video .data").removeClass("h");
		$("#main-video .dataH").addClass("h");
		$(".subscribe").removeClass("night");
		$("#main-video .video").html('');
	});

	var skl = function(n){
		var c;
		if(n===1){
			c = 0;
		}else if(n>1 && n<10){
			c = 1;
		}else if(n>=10 && n<21){
			c = 2;
		}else{
			switch(n.toString().slice(-1)){
				case '0':
					c = 2;
				break;
				case '1':
					c = 0;
				break;
				case '2': case '3': case '4':
					c = 1;
				break;
				case '5': case '6': case '7': case '8': case '9':
					c = 2;
				break;
			};
		};

		return c;
	};

	var preloadImage = function(src){
		var img = new Image();
        img.src = src;
	};

	var startInstagram = function(){
		$(".loader-video .data").addClass("h");
		$(".loader-video .loader").css("transform", "scale(1)");
		$(".loader-video .status").html("Разрешите инстаграму общаться с Realfie во всплывающем окне");
		OAuth.popup('instagram').done(function(result) {
			global.inat = result.access_token;
			global.inimage = result.user.profile_picture;
			preloadImage(global.inimage);
			global.inuser = result.user.id;
		    global.reqi = 0;
		    global.req = false;
		    global.task = false;
			global.incancel = false;
			global.inloop = setInterval(function(){
				if(!global.fbreq){
					global.req = true;
					var url;

					if(global.task) url = '/fetch/?task_id='+global.task;
					else url = '/fetch/?source=instagram&access_token='+global.inat;

					$.getJSON(url, function(res){
						inComplete(res);
						if(res.task_id) global.task = res.task_id;
						global.reqi++;
						global.req = false;
					})
				}
			}, global.reqspeed);

			$(".loader-video .status").html("Поиск вот-вот начнется");
			startLoAnimation();
		});
	};

	var startFacebook = function(){
		$(".loader-video .loader").css("transform", "scale(1)");
		$(".loader-video .data").addClass("h");
		$(".loader-video .status").html("Разрешите фейсбуку общаться с Realfie во всплывающем окне");
		OAuth.popup('facebook').done(function(result) {
			global.fbat = result.access_token;
			result.get('/me')
		    .done(function (response) {
		        global.fbuser = response.id;
				preloadImage("https://graph.facebook.com/"+global.fbuser+"/picture?width=480&height=480");
		        global.fbgender = response.gender;
		        global.inflag = false;
				global.reqi = 0;
				global.req = false;
				global.task = false;
				global.fbcancel = false;
				global.fbloop = setInterval(function(){
					if(!global.req){
						global.req = true;
						var url;

						if(global.task) url = '/fetch/?task_id='+global.task;
						else url = '/fetch/?source=facebook&access_token='+global.fbat;

						$.getJSON(url, function(res){
							fbComplete(res);
							if(res.task_id) global.task = res.task_id;
							global.reqi++;
							global.req = false;
						})
					}
				}, global.reqspeed);

				$(".loader-video .status").html("Поиск вот-вот начнется");
				startLoAnimation();
		    })
		    .fail(function (err) {
		        cancelFacebook();
		    });
		}).fail(function (err) {
			alert(err);
		    cancelFacebook();
		});
	};

	/*var showonLoad = function(entries){
		var n = entries.length,
			e = entries[Math.floor(Math.random()*entries.length)];
		$(".ongoing").css("background-image", "url("+e.photo+")");
		$(".ongoing").addClass("fadeOutUp").removeClass("t");
		$(".ongoing").one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
			$(".ongoing").removeClass("fadeOutUp").addClass("t");
		});
	};*/

	var render = function(entries){
		var n = entries.length;

		global.closers = [];
		$(".fb-connect .entries").empty();
		$(".fb-connect .entries").removeClass("n1 n2 n3").addClass("n"+n);

		for (var i = 0; i < entries.length; i++) {
			if(i<3){
				var e = entries[i],
					tips = '',
					ams = [];

				global.closers.push(e);

				for (var ii = 0; ii < e.edges.length; ii++) {
					if(e.edges[ii].type < types.length) {
						ams[e.edges[ii].type] = ams[e.edges[ii].type] ? ams[e.edges[ii].type]+1 : 1;
					}
				};
				for (var ii = 1; ii < ams.length; ii++) {
					if(ams[ii]!==undefined) tips += '<div class="type t'+ii+'">'+ams[ii]+' '+types[ii][skl(ams[ii])]+'</div>';
				};

				$(".fb-connect .entries").append($('<div class="entry"><div class="image" style="background-image: url('+e.photo+')"></div><div class="semibold name">'+e.name+'</div><div class="arial info">Также как и вы любит '+e.edges[Math.floor(Math.random()*e.edges.length)].name+' и еще <span class="pseudo">'+(e.edges.length-1)+' вещ'+types[0][skl(e.edges.length-1)]+'</span><div class="tips">'+tips+'</div></div><div class="arial closer" data-id="'+i+'" data-prov="fb">Сблизиться<div class="icon"></div></div></div>'));
			}
		};
	};

	var addIn = function(entries){
		var type = ["место", "места", "мест"],
			e = entries[0];

		global.closers.push(e);
		global.inflag = true;

		$(".in-connect .entries").html($(".fb-connect .entries").html());
		$(".in-connect .entries").removeClass("n1 n2 n3 n4").addClass("n"+($(".fb-connect .entries .entry").length+1));
		$(".in-connect .image").append('<div class="soc-icon"></div>');
		$(".in-connect .entry").addClass("fb");

		$(".in-connect .entries").append($('<div class="entry in"><div class="image" style="background-image: url('+e.photo+')"><div class="soc-icon"></div></div><div class="semibold name">'+e.name+'</div><div class="arial info">Также как и ходит в '+e.edges[Math.floor(Math.random()*e.edges.length)].name+' и еще '+(e.edges.length-1)+' '+type[skl(e.edges.length-1)]+'</div><div class="arial closer" data-id="'+(global.closers.length-1)+'" data-prov="in">Сблизиться<div class="icon"></div></div></div>'));
	};

	var fbComplete = function(res){
		if(!global.fbcancel){
			if(res.status !== "null"){
				switch(res.status){
					case 'started':
						$(".loader-video .status").html("Поиск начался...");
					break;
					case 'ongoing':
						//if(res.entries.length>0) showonLoad(res.entries);
						$(".loader-video .status").html("Поиск завершен на "+(res.progress*100)+"%");
					break;
					case 'completed':
						clearInterval(global.fbloop);
						//disable_scroll();
						stopLoAnimation();

						if(res.entries.length>0){ 
							render(res.entries);
							setTimeout(function(){
								$(".fb-connect").css("left", 0);
							},100);
						}else{ $(".error span").html("потому что вы, видимо, слишком уникальны. Может в следующий раз повезет!"); $(".error").addClass("zoomIn"); };
					break;
					case 'failed':
						stopLoAnimation();
						$(".error span").html(res.reason);
						$(".error").addClass("zoomIn");
					break;
				};
			}
		}
	};

	var inComplete = function(res){
		if(!global.incancel){
			if(res.status !== "null"){
				switch(res.status){
					case 'started':
						$(".loader-video .status").html("Поиск начался...");
					break;
					case 'ongoing':
						if(res.entries.length>0) showonLoad(res.entries);
						$(".loader-video .status").html("Поиск завершен на "+(res.progress*100)+"%");
					break;
					case 'completed':
						clearInterval(global.inloop);
						//disable_scroll();
						stopLoAnimation();

						if(res.entries.length>0){ 
							addIn(res.entries);
							setTimeout(function(){
								$(".in-connect").css("left", 0);
							},100);
						};
					break;
					case 'failed':
						stopLoAnimation();
						$(".error span").html(res.reason);
						$(".error").addClass("zoomIn");
					break;
				};
			}
		}
	};

	var cancelFacebook = function(){
		if(!global.fbcancel){
			global.fbcancel = true;
			$(".error").css("opacity", 0);
			$(".loader-video .data").removeClass("h");
			clearInterval(global.fbloop);
			stopLoAnimation();
		}
	};

	var cancelInstagram = function(){
		if(!global.incancel){
			global.incancel = true;
			$(".error").css("opacity", 0);
			$(".loader-video .data").removeClass("h");
			clearInterval(global.inloop);
			stopLoAnimation();
		}
	};

	var startLoAnimation = function(){
		$(".loader-video .action").css("background-image", "none");
		$(".loader-video .action").css("background-image", "url(/static/images/loader-dbl-6.png)");
		var ianim = 1;
		global.anim = setInterval(function(){
			
			$(".loader-video .loader .left, .loader-video .loader .right").css("background-position", "50% center");
			$(".loader-video .action").css("background-image", "none");
			
			setTimeout(function(){
				$(".loader-video .loader .left, .loader-video .loader .right").css("opacity", 0);
				$(".loader-video .action").css("background-image", "url(/static/images/loader-dbl-"+ianim+".png)");
				$(".loader-video .action").addClass("bounceIn");
				$(".loader-video .action").one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
					$(".loader-video .action").removeClass("bounceIn");
					$(".loader-video .loader .left, .loader-video .loader .right").css("opacity", 1);
				});
				ianim++;
				ianim = ianim===7 ? 1 : ianim;
			},2000);

			setTimeout(function(){
				$(".loader-video .loader .left").css("background-position", "-10% center");
				$(".loader-video .loader .right").css("background-position", "110% center");
			},3000);

			setTimeout(function(){
				$(".loader-video .loader .left, .loader-video .loader .right").removeClass("l1 l2 l3 l4 l5 l6").addClass("l"+ianim);
			},4000);

		}, 5000);
			
	};

	var stopLoAnimation = function(){
		clearInterval(global.anim);
		clearInterval(global.anim2);
		$(".loader-video .loader").css("transform", "scale(0)");
	};

	$(".facebook").click(function(){
		var h = $(window).height();
		$(window).scrollToTop(12*h);
		startFacebook();
	});

	$(".ok").click(function(){
		$(".error").removeClass("zoomIn");
		cancelFacebook();
		//enable_scroll();
	});

	$(".first").click(function(){
		$(".connect").css("left", "100%");
		cancelFacebook();
		//enable_scroll();
	});

	$(".second").click(function(){
		$(".fb-connect").css("left", 0);
		if($(".in-connect").css("left")==="0px") $(".in-connect").css("left", "100%");
		else $(".closer-page").css("left", "100%");
	});

	$(".third").click(function(){
		$(".in-connect").css("left", 0);
		$(".closer-page").css("left", "100%");
	});

	$(".instagram").click(function(){
		$(".fb-connect").css("left", "-100%");
		startInstagram();
	});

	var validateEmail = function(email) { 
	    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	    return re.test(email);
	} 

	var sendEmail = function(email) {
		//$.ajax(email);
	}

	$("#main-video").on("keypress", "#top-input", function(){
		$("#top-input").removeClass("error");
	});

	$(".footer").on("keypress", "#foot-input", function(){
		$("#foot-input").removeClass("error");
	});

	$(".topbtn").click(function(){
		var v = $("#top-input").val();
		if(validateEmail(v)){
			$(".subscribe .thankyou").removeClass("h");
			$(".title, .top-input").addClass("h");
			sendEmail(v);
		}else{
			$("#top-input").addClass("error");
		}
	});

	$(".btmbtn").click(function(){
		var v = $("#foot-input").val();
		if(validateEmail(v)){
			$(".top .thankyou").removeClass("h");
			$(".foot-input").addClass("h");
			sendEmail(v);
		}else{
			$("#foot-input").addClass("error");
		}
	});

	$(".connect").on("click", ".closer", function(){
		var id = $(this).attr("data-id"),
			p = $(this).attr("data-prov"),
			himher = global.closers[id],
			pic,
			randEdge;

		do{ randEdge = himher.edges[Math.floor(Math.random()*himher.edges.length)].type; } while(randEdge===0);

		if(p==="in"){
			if(global.inimage!==null && global.inimage!==''){
				pic = global.inimage;
			}else{
				pic = "https://graph.facebook.com/"+global.fbuser+"/picture?width=480&height=480";
			}
			$(".closer-page").removeClass("fb in").addClass("in");
			$(".closer-page .tip span").html(types[1][3]);
		}else{
			pic = "https://graph.facebook.com/"+global.fbuser+"/picture?width=480&height=480";
			$(".closer-page").removeClass("fb in").addClass("fb");
			$(".closer-page .tip span").html(types[randEdge][3]);
		}

		$(".closer-page .paging .fourth").remove();
		if(global.inflag) $(".closer-page .paging").append('<div class="fourth"></div>');

		$(".connect").css("left", "-100%");

		$(".closer-page .you").css("background-image", "url("+pic+")");
		$(".closer-page .himher").css("background-image", "url("+himher.photo+")");
		$(".closer-page .h1 .y").html(global.fbgender==="male" ? "" : "а");
		$(".closer-page .h1 .hh").html(himher.sex==="m" ? "тот самый" : "та самая");
		$(".closer-page .h3 span").html(himher.sex==="m" ? "парень" : "девушка");

		$(".closer-page").css("left", 0);
	});

	preloadImage("/static/images/play-hover.png");
	preloadImage("/static/images/c-instagram-hover.png");
	preloadImage("/static/images/second-ss.png");
	preloadImage("/static/images/iphone-white.png");
	preloadImage("/static/images/close-hover.png");
	preloadImage("/static/images/closer-white.png");
	preloadImage("/static/images/loader-dbl-1.png");
	preloadImage("/static/images/loader-dbl-2.png");
	preloadImage("/static/images/loader-dbl-3.png");
	preloadImage("/static/images/loader-dbl-4.png");
	preloadImage("/static/images/loader-dbl-5.png");
	preloadImage("/static/images/loader-dbl-6.png");
	preloadImage("/static/images/loader-icon-1.png");
	preloadImage("/static/images/loader-icon-2.png");
	preloadImage("/static/images/loader-icon-3.png");
	preloadImage("/static/images/loader-icon-4.png");
	preloadImage("/static/images/loader-icon-5.png");
	preloadImage("/static/images/loader-icon-6.png");

})