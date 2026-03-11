//åå®¹é¡µè®¾ç½®
function readconf(type) {
    var huyan = document.getElementById("huyan");
    var light = document.getElementById("light");
    if (type == "huyan") {
        var value = (huyan.className == "button huyan-on") ? 'huyan' : 'no';
        store.set('setting_light', value);
        set("light", value);
    }
    if (type == "light") {
        var value = (light.innerHTML == "å³ç¯") ? 'yes' : 'no';
        store.set('setting_light', value)
        set("light", value);
    }
    var font_size = 'middle';
    if (type == "big") {
        font_size = 'big';
    } else if (type == 'small') {
        font_size = 'small';
    }
    store.set('setting_font', font_size)
    set("font", font_size);
}

//åå®¹é¡µè¯»åè®¾ç½®
function getset() {
    //å³ç¯åæ¤ç¼éç½®
    light = store.get('setting_light') || 'no';
    set("light", light);

    //å­ä½éç½®
    font = store.get('setting_font') || 'middle';
    set("font", font);
}

//åå®¹é¡µåºç¨è®¾ç½®
function set(type, p) {
    var nr_body = document.getElementById("read"); //é¡µé¢body
    var huyan = document.getElementById("huyan"); //æ¤ç¼div
    var light = document.getElementById("light"); //ç¯ådiv
    var fontfont = document.getElementById("fontfont"); //å­ä½div
    var fontbig = document.getElementById("fontbig"); //å¤§å­ä½div
    var fontmiddle = document.getElementById("fontmiddle"); //ä¸­å­ä½div
    var fontsmall = document.getElementById("fontsmall"); //å°å­ä½div
    var content = document.getElementById("content"); //åå®¹div

    //ç¯å
    if (type == "light") {
        if (p == "yes") {
            //å³ç¯
            light.innerHTML = "å¼ç¯";
            light.className = "button light-on";
            nr_body.style.backgroundColor = "#000";
            huyan.className = "button huyan-on";
            content.style.color = "#999";
        } else if (p == "no") {
            //å¼ç¯
            light.innerHTML = "å³ç¯";
            light.className = "button light-off";
            nr_body.style.backgroundColor = "#fff";
            content.style.color = "#000";
            huyan.className = "button huyan-on";
        } else if (p == "huyan") {
            //æ¤ç¼
            light.innerHTML = "å³ç¯";
            light.className = "button light-off";
            huyan.className = "button huyan-off";
            nr_body.style.backgroundColor = "#DCECD2";
            content.style.color = "#000";
        }
    }
    //å­ä½
    if (type == "font") {
        fontbig.className = "sizebg";
        fontmiddle.className = "sizebg";
        fontsmall.className = "sizebg";
        if (p == "big") {
            fontbig.className = "button size-on";
            content.style.fontSize = "25px";
        }
        if (p == "middle") {
            fontmiddle.className = "button size-on";
            content.style.fontSize = "20px";
        }
        if (p == "small") {
            fontsmall.className = "button size-on";
            content.style.fontSize = "14px";
        }
    }
}

function getQuery(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        if(pair[0] == variable){return pair[1];}
    }
    return(false);
}

function getSelectedCheckbox(div,name){
    var checks = "";
    var val = "";
    $("#"+div+" input[name='"+name+"']").each(function(){
        if($(this).prop("checked")){
            val = $(this).val();
            if("" == checks){
                checks += val;
            }else{
                checks += ","+val;
            }
        }
    });
    return checks;
}

//æç¤ºä¿¡æ¯æ¡
function toast(msg, timeout) {
    timeout = timeout || 3000;
    if (!document.getElementsByClassName('toast-wrap').length) {
        var div = document.createElement('div');
        div.className = 'toast-wrap';
        div.innerHTML = '<span class="toast-msg"></span>';
        document.getElementsByTagName("body")[0].appendChild(div);
    }
    document.getElementsByClassName('toast-wrap')[0].getElementsByClassName('toast-msg')[0].innerHTML = msg;
    var toastTag = document.getElementsByClassName('toast-wrap')[0];
    toastTag.style.display = "block";
    setTimeout(function () {
        toastTag.style.display = 'none';
    }, timeout);
}

function page() {
    var $pagenum ;
    var $pagenum2 = 0;
    $('.page_txt').focus(function(){
        if($pagenum2 == ""){
            $pagenum = $(this).val();
        }
        $(this).val("");
        $(this).next().text('è½¬ãå°');
        $(this).next().addClass('goto');
    });
    $('.page_txt').blur(function(){
        if($(this).val() == ""){
            if($pagenum2 == ""){
                $(this).val($pagenum);
            }else{
                $(this).val($pagenum2);
            }
            $(this).next().text('ä¸ä¸é¡µ');
            $(this).next().removeClass('goto');
        }else{
            $pagenum2 = $pagenum;
            $page = $(this).val();
            var url = decodeURI($(".goto").attr("href"));
            if($page != ""){
                url = url.split("/");
                var urllength = url.length;
                var lasturl = url[urllength-1];
                lasturl = lasturl.replace(/[0-9]/ig,$page);
                url[urllength-1] = lasturl;
                url = url.join("/");
                $(".goto").attr("href",encodeURI(url));
            }
        }
        if($("#nextPage").attr("class")=="goto"){
            var url=$("#nextPage").attr("href");
            url=url.replace(/page\=\d+/,"page="+$("#txtPage").val());
            $("#nextPage").attr("href",url);
        }
    });
}

function login_page() {
    var html = '';
    var isLogin = Object.keys(store.get('user_info') || {}).length ? true : false;
    if (isLogin) {
    	var user_info = store.get('user_info') || {};
    	html = '<a href="/user/userinfo.html" class="userin">' + user_info.username + '</a>';
    } else {
    	html = '<a class="user" href="/user/login.html">ç»å½</a>' +
        '<a href="/user/register.html" class="user">æ³¨å</a>';
    }
    document.writeln(html);
}

function search_page() {
    var html = '<form method="get" class=\"searchForm\" accept-charset=\"UTF-8\" action="/user/search.html">\n' +
        '<input id="q" name="q" type="text" class="searchForm_input" onclick="this.value=\'\'" value="è¾å¥ä¹¦åæä½è"/>\n' +
        '<input type="submit" value=\"æç´¢\" class="searchForm_btn">\n' +
        '</form>';
    document.writeln(html);
}

function search_before() {
	if (document.cookie != "") {
		bgt=bgt.slice(0, bgt.length-1);
	}
	$("#loading").css('display', 'block');
}

function search_after() {
	$("#loading").css('display', 'none');
}

function header() {
}

function read_header() {
}

function read_top() {
}

function read_middle() {
 
}

function read_bottom() {
}


function footer() {
}

function tongji() {
}

function Book() {
    this.user_info = store.get('user_info') || {};
    this.token = Object.keys(this.user_info).length ? this.user_info.token : '';
}

Book.prototype = {
    addBook: function (book_id) {
        this.checkLogin();
        var url = '/api/addBook';
        var params = {'token': this.token, 'bid': book_id};
        $.post(url, params, function (json) {
            if (json.code == 0) {
                toast('æ­åæ¨å·²æåå å¥å°ä¹¦æ¶ä¸­ï¼');
                $("#saveBookBtn").html("<font color=red>å·²å å¥ä¹¦æ¶</font>");
            } else {
                toast(json.msg);
            }
        }, 'json');
    },
    getBook: function () {
    	this.checkLogin();
        var url = '/api/findBook';
        var params = {'token': this.token};
        $.post(url, params, function (json) {
            var bookList = json.data;
            if (json.code == 0) {
                var interText = doT.template($("#tpl-bookcase").text());
                $("#main").html(interText(bookList));
            } else if (json.code == 201) {
                location.href = '/user/login.html';
            }
        }, 'json');
    },
    delBook: function (book_id) {
    	this.checkLogin();
        var url = '/api/delBook';
        var params = {'token': this.token, 'bid': book_id};
        $.post(url, params, function (json) {
            if (json.code == 0) {
                $('#book' + book_id).remove();
                toast('å é¤æåï¼');
            } else {
                toast(json.msg);
            }
        }, 'json');
    },
    getBookcase: function (site_book_id) {
    	if (this.token == '' || this.token == undefined) {
    		return ;
    	}
        var url = '/api/getBookMark';
        var params = {'token': this.token, 'bid': site_book_id};
        $.get(url, params, function (json) {
            if (json.code == 0) {
            	if (json.data.id > 0) {
                    $("#saveBookBtn").html("<font color=red>å·²å å¥ä¹¦æ¶</font>");
                }
            }
        }, 'json');
    },
    getBookMark: function (site_book_id, site_chapter_id) {
    	if (this.token == '' || this.token == undefined) {
    		return ;
    	}
        var url = '/api/getBookMark';
        var params = {'token': this.token, 'bid': site_book_id};
        $.get(url, params, function (json) {
            if (json.code == 0) {
                if (json.data.site_chapter_id == site_chapter_id) {
                	$("#saveMarkBottomBtn").html("<font color=red>å·²å å¥ä¹¦ç­¾</font>");
                }
            }
        }, 'json');
    },
    readLog: function (type) {
        type = parseInt(type) || 0;
        if (type == 1) {
            bookList = store.get('book_readlog') || [];
            if (bookList.length) {
                if (bookList.length >= 10) {
                    bookList.pop();
                }
                for (var i in bookList) {
                    if (parseInt(bookList[i].book_id) == parseInt(info.book_id)) {
                        bookList.splice(i, 1);
                        break;
                    }
                }
            }
            bookList.unshift(info);
            store.set('book_readlog', bookList);
        } else if (typeof (doT) == 'object') {
            bookList = store.get('book_readlog') || [];
            var interText = doT.template($("#tpl-readlog").text());
            $("#main").html(interText(bookList));
        }
    },
    removeLog: function(book_id) {
        bookList = store.get('book_readlog') || [];
        for (var i in bookList) {
            if (parseInt(bookList[i].book_id) == book_id) {
                bookList.splice(i, 1);
                break;
            }
        }
        store.set('book_readlog', bookList);
        $("#log" + book_id).remove();
    },
    chapterSort: function () { //ç« èæåº
        var oUl = document.getElementById('chapter-list');
        var oLi = oUl.getElementsByTagName('li');
        for (var i = 0, arr = []; i < oLi.length; i++) {
            arr[i] = oLi[i];
        }
        arr.reverse();
        for (var i = 0; i < arr.length; i++) {
            oUl.appendChild(arr[i]);
        }
        var text = document.getElementById('order').innerText;
        document.getElementById('order').innerText = (text == '[ååº]') ? '[æ­£åº]' : '[ååº]';
    },
    checkLogin: function () { //éªè¯ç»å½
        if (this.token == '' || this.token == undefined) {
        	var referer = window.location.href;
            location.href = '/user/login.html?referer='+encodeURIComponent(referer);
        }
    },
    userLogin: function () { //ç¨æ·ç»å½
        var username = $("#loginForm #username").val();
        var password = $("#loginForm #password").val();
        //var expire = $("#loginForm #usecookie").find('option:checked').val();
        if (username == '') {
            toast('è¯·è¾å¥ç¨æ·åï¼');
            return false;
        }
        if (password == '') {
            toast('è¯·è¾å¥å¯ç ï¼');
            return false;
        }
        var referer = getQuery('referer');
        var url = '/api/login';
        var params = {'username': username, 'password': password};
        $.post(url, params, function (json) {
            if (json.code == 0) {
                store.set('user_info', json.data);
                if ("" != referer && false != referer) {
                	location.href = decodeURIComponent(referer);
                }else{
                	location.href = '/';
                }
            } else {
                toast(json.msg);
            }
        }, 'json');
        return false;
    },
    userRegister: function () {
        var username   = $("#regForm #username").val();
        var password   = $("#regForm #password").val();
        var repassword = $("#regForm #repassword").val();
        var email      = $("#regForm #email").val();

        var xarg = /^[a-z0-9][a-z0-9@\-._]{5,31}$/i;
        if (username == '' || !xarg.test(username)) {
            toast('ç¨æ·åæ ¼å¼æè¯¯ï¼6-32ä½å­æ¯ãæ°å­æ_.-@ç»æï¼');
            return false;
        }
        if (password == '' || !xarg.test(password)) {
            toast('å¯ç æ ¼å¼æè¯¯ï¼6-32ä½å­æ¯ãæ°å­æ_.-@ç»æï¼');
            return false;
        }
        if (repassword == '') {
            toast('è¯·è¾å¥ç¡®è®¤å¯ç ï¼');
            return false;
        }
        if (password != repassword) {
            toast('è¾å¥çä¸¤æ¬¡å¯ç ä¸ä¸è´ï¼');
            return false;
        }
        var url = '/api/register';
        var params = {'username': username, 'password': password, 'email': email};
        $.post(url, params, function (json) {
            if (json.code == 0) {
                store.set('user_info', json.data);
                location.href = '/';
            } else {
                toast(json.msg);
            }
        }, 'json');
        return false;
    },
    editPassword: function () {
    	this.checkLogin();
        var password = $("#password").val();
        var repassword = $("#repassword").val();

        var xarg = /^[a-z0-9][a-z0-9@\-._]{5,31}$/i;
        if (password == '' || !xarg.test(password)) {
            toast('å¯ç æ ¼å¼æè¯¯ï¼6-32ä½å­æ¯ãæ°å­æ_.-@ç»æï¼');
            return false;
        }
        if (repassword == '') {
            toast('è¯·è¾å¥ç¡®è®¤å¯ç ï¼');
            return false;
        }
        if (password != repassword) {
            toast('è¾å¥çä¸¤æ¬¡å¯ç ä¸ä¸è´ï¼');
            return false;
        }
        var url = '/api/editPassword';
        var params = {'token': this.token, 'password': password};
        $.post(url, params, function (json) {
            if (json.code == 0) {
                toast('å¯ç ä¿®æ¹æå');
            } else {
                toast(json.msg);
            }
        }, 'json');
    },
    logout: function () {
        store.remove('user_info');
        location.href = '/';
    },
    userInfo: function () {
        if (this.token) {
            document.writeln(this.user_info.username);
        } else {
            location.href = '/user/login.html';
        }
    },
    addMark: function (bid, cid, cname) {
        this.checkLogin();
        //cname = encodeURIComponent(cname || '');
        var url = '/api/mark';
        var params = {'token': this.token, 'bid': bid, 'cid': cid, 'cname': cname};
        $.post(url, params, function (json) {
            if (json.code == 0) {
                toast('ä¹¦ç­¾å å¥æåï¼');
                $("#saveMarkBottomBtn").html("<font color=red>å·²å å¥ä¹¦ç­¾</font>");
            } else {
                toast(json.msg);
            }
        }, 'json');
    },
    userVote: function (bid) {
        this.checkLogin();
        var url = '/api/vote';
        var params = {'token': this.token, 'bid': bid};
        $.post(url, params, function (json) {
            if (json.code == 0) {
                toast('æç¥¨æåï¼');
            } else {
                toast(json.msg);
            }
        }, 'json');
    },
    bookStats: function (bid) {
        var url = '/api/access';
        $.post(url, {'bid': bid}, function (json) {}, 'json');
    },
    search: function () {
    	if ("" == vw) {
    		return ;
    	}
    	if ("" == abw) {
    		return ;
    	}
    	if ("" == ru) {
    		return ;
    	}
    	if ("" == jrt) {
    		return ;
    	}
    	if ("" == van) {
    		return ;
    	}
    	if ("" == fw) {
    		return ;
    	}
    	if ("" == cwl) {
    		return ;
    	}
    	if ("" == gpr) {
    		return ;
    	}
    	if ("" == uyoo) {
    		return ;
    	}
    	if ("" == tz) {
    		return ;
    	}
    	if ("" == euu) {
    		return ;
    	}
    	if ("" == tsn) {
    		return ;
    	}
    	if ("" == eju) {
    		return ;
    	}
    	if ("" == um) {
    		return ;
    	}
    	if ("" == fp) {
    		return ;
    	}
    	if ("" == dvm) {
    		return ;
    	}
    	if ("" == jpk) {
    		return ;
    	}
    	if ("" == deblkx) {
    		return ;
    	}
    	if ("" == ht) {
    		return ;
    	}
    	if ("" == azy) {
    		return ;
    	}
    	if ("" == sna) {
    		return ;
    	}
    	if ("" == wqx) {
    		return ;
    	}
    	if ("" == fpp) {
    		return ;
    	}
    	if ("" == rup) {
    		return ;
    	}
    	if ("" == jwj) {
    		return ;
    	}
    	if ("" == bgt) {
    		return ;
    	}
    	if ("" == qp) {
    		return ;
    	}
    	if ("" == yf) {
    		return ;
    	}
    	if ("" == cw) {
    		return ;
    	}
    	if ("" == wq) {
    		return ;
    	}
        var keyword = decodeURIComponent(getQuery('q'));
        if ("" == keyword) {
        	bookList = new Array();
            bookList['search'] = new Array();
            bookList['keyword'] = keyword || '';
            var interText = doT.template($("#tpl-search").text());
            $("#main").html(interText(bookList));
        	return ;
        }
        search_before();
        var url = '/api/search';
        var params = {'q':keyword,'vw':vw,'abw':abw,'ru':ru,'jrt':jrt,'van':van,'fw':fw,'cwl':cwl,'gpr':gpr,'uyoo':uyoo,'tz':tz,'euu':euu,'tsn':tsn,'eju':eju,'um':um,'fp':fp,'dvm':dvm,'jpk':jpk,'deblkx':deblkx,'ht':ht,'azy':azy,'sna':sna,'wqx':wqx,'fpp':fpp,'rup':rup,'jwj':jwj,'bgt':bgt,'qp':qp,'yf':yf,'cw':cw,'wq':wq,'sign':sign};
        $.post(url, params, function (json) {
        	search_after();
        	if (json.code == 0) {
        		bookList = json.data;
                bookList['keyword'] = keyword || '';
                var interText = doT.template($("#tpl-search").text());
                $("#main").html(interText(bookList));
        	} else {
        		toast(json.msg);
        	}
        }, 'json');
    },
    report: function () {
        var url = '/api/report';
        var referer = getQuery('referer');
        var bid     = $("#reportForm #bid").val();
        var cid     = $("#reportForm #cid").val();
        var content = $("#reportForm #content").val();
        var report_types = getSelectedCheckbox('reportForm', 'report_type');
        if ("" == report_types) {
        	toast('è¯·éæ©ä¸é¡¹éè¯¯ç±»å');
            return false;
        }
        var params = {'token': this.token, 'bid': bid, 'cid': cid, 'type': report_types, 'content': content};
        $.post(url, params, function (json) {
            refreshVcode('img_vcode');
            if (json.code == 0) {
                toast('åé¦æåï¼');
                if ("" != referer && false != referer) {
                	location.href = decodeURIComponent(referer);
                } else {
                	location.href = '/';
                }
            } else {
                toast(json.msg);
            }
        }, 'json');
    }
}

function Chapter() {
}

Chapter.prototype = {
    detail: function (bid) {
        var url = '/api/detail';
        var params = {'bid': bid};
        $.get(url, params, function (json) {
            var interText = doT.template($("#tpl-chapter-detail").text());
            $("#chapter-detail").html(interText(json.data));
        }, 'json');
    },
    list: function (bid, page_num) {
        var url = '/api/list';
        var params = {'bid': bid,'page_num': page_num};
        $.get(url, params, function (json) {
            var interText = doT.template($("#tpl-chapter-list").text());
            $("#chapter-list").html(interText(json.data));

            if ("" != json.data.page_style3) {
            	var interTextPage = doT.template($("#tpl-chapter-list-page").text());
                $("#chapter-list-page").html(interTextPage(json.data));
            }
        }, 'json');
    },
    content: function (cid) {
        var url = '/api/content';
        var params = {'cid': cid};
        $.get(url, params, function (json) {
            var interText = doT.template($("#tpl-chapter-content").text());
            $("#chapter-content").html(interText(json.data));
        }, 'json');
    }
}

window.book = new Book();
window.chapter = new Chapter();

