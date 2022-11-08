
var Common = {
    //获取cookie
    GetCookie: function (c_name) {
        if (document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=")
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1
                c_end = document.cookie.indexOf(";", c_start)
                if (c_end == -1) c_end = document.cookie.length
                return unescape(document.cookie.substring(c_start, c_end))
            }
        }
        return ""
    },
    //添加cookie（记住我）
    SetCookie: function (name, value, days, path) {   /**添加设置cookie**/
        var name = escape(name);
        var value = escape(value);
        var expires = new Date();
        expires.setTime(expires.getTime() + days * 3600000 * 24);

        path = path == "" ? "" : ";path=" + path;

        var _expires = (typeof days) == "string" ? "" : ";expires=" + expires.toUTCString();
        document.cookie = name + "=" + value + _expires + path;
    },
    //获取url参数
    Request: function (paras) {
        var url = location.href;
        var paraString = url.substring(url.indexOf("?") + 1, url.length).split("&");
        var paraObj = {}
        for (i = 0; j = paraString[i]; i++) {
            paraObj[j.substring(0, j.indexOf("=")).toLowerCase()] = j.substring(j.indexOf("=") + 1, j.length);
        }
        var returnValue = paraObj[paras.toLowerCase()];
        if (typeof (returnValue) == "undefined") {
            return "";
        } else {
            return returnValue;
        }
    },
    /*用正则表达式实现html转码*/
    htmlEncodeByRegExp: function (str) {
        var s = "";
        if (str.length == 0) return "";
        s = str.replace(/&/g, "&amp;");
        s = s.replace(/</g, "&lt;");
        s = s.replace(/>/g, "&gt;");
        s = s.replace(/ /g, "&nbsp;");
        s = s.replace(/\'/g, "&#39;");
        s = s.replace(/\"/g, "&quot;");
        return s;
    },
    /*用正则表达式实现html解码*/
    htmlDecodeByRegExp: function (str) {
        var s = "";
        if (str.length == 0) return "";
        s = str.replace(/&amp;/g, "&");
        s = s.replace(/&lt;/g, "<");
        s = s.replace(/&gt;/g, ">");
        s = s.replace(/&nbsp;/g, " ");
        s = s.replace(/&#39;/g, "\'");
        s = s.replace(/&quot;/g, "\"");
        return s;
    },
    //带区域日期类型（T）转换
    TDateByDate: function (str) {

        if (str.indexOf("T") != -1) {
            var str = str.replace(str.substring(10, 11), " ");
            return str;
        }
        return str;
    },
    TDateByFirst: function (str) {

        if (str.indexOf("T") != -1) {
            var str = str.split("T");
            return str[0];
        }
        return str;
    },
    TDateByLast: function (str) {

        if (str.indexOf("T") != -1) {
            var str = str.split("T");
            return str[1];
        }
        return str;
    },
    //处理错误信息
    ErrorDispose: function (ErrorInfo) {
        if (ErrorInfo == "登录状态失效！请重新登录！") {

            // 占时不提示
            //alert(ErrorInfo);
            // 跳转到登录页面，登录后自动跳转回当前页面
            window.location.href = "/login.html?target=" + window.location.href;
            return;
        }

        alert(ErrorInfo);
    },
    // 返回网站地址
    serverUrl: function () {

        // 链接到正式服务器
        // return "http://www.aishang67.cn";
        // 链接到测试环境
        return "http://localhost:8080/";
    },
    //创建分页
    createAPage: function (pageSize,  IsCallBack) {
       
        $("#" + Id).pagination(total, {
            num_edge_entries: 1,
            num_display_entries: 10,
            callback: IsCallBack, //回调函数
            items_per_page: pageSize,
            prev_text: "前一页",
            next_text: "后一页"
        });
    }
}

$.extend({
    /** 
    1. 设置cookie的值，把name变量的值设为value   
    example $.cookie(’name’, ‘value’);
    2.新建一个cookie 包括有效期 路径 域名等
    example $.cookie(’name’, ‘value’, {expires: 7, path: ‘/’, domain: ‘jquery.com’, secure: true});
    3.新建cookie
    example $.cookie(’name’, ‘value’);
    4.删除一个cookie
    example $.cookie(’name’, null);
    5.取一个cookie(name)值给myvar
    var account= $.cookie('name');
    **/
    cookieHelper: function (name, value, options) {
        if (typeof value != 'undefined') { // name and value given, set cookie
            options = options || {};
            if (value === null) {
                value = '';
                options.expires = -1;
            }
            var expires = '';
            if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
                var date;
                if (typeof options.expires == 'number') {
                    date = new Date();
                    date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
                } else {
                    date = options.expires;
                }
                expires = '; expires=' + date.toUTCString(); // use expires attribute, max-age is not supported by IE
            }
            var path = options.path ? '; path=' + options.path : '';
            var domain = options.domain ? '; domain=' + options.domain : '';
            var secure = options.secure ? '; secure' : '';
            document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
        } else { // only name given, get cookie
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    }
});
//原生ajax设置title
function setAjaxTitle(titleName){
	if(window.Webview){
		if(window.Webview.showInfoFromJs){
			window.Webview.showInfoFromJs(titleName);
		}
	}
	if(window.webkit){
		if(window.webkit.messageHandlers){
			if(window.webkit.messageHandlers.showInfoFromJs){
				window.webkit.messageHandlers.showInfoFromJs.postMessage(titleName);
			}
		}
	}
}

//验证是否有数据
function haveContent(parent,content,apply){
	var html="";
	if($('.'+content+'').length==0&&$('.'+parent+' .noContent').length==0){
		html+='<p class="noContent" style="text-align: center;line-height:70px;font-size:16px;color:#323232;clear:both;background: #f0f0f0;">'+apply+'</p>'
		$(".mui-pull").hide();
		$('.'+parent+'').append(html);
	}
	if($('.'+parent+' .noContent').length==0){
		html+='<p class="nojilu">没有更多数据了</p>';
		$('.'+parent+'').append(html);
	}
}
//等待框
function appendLoad(){
	con="";
	 con+='<div id="checkLoading" class="hide"><img src="../img/checkLoad.png"></div>';
	$("body").append(con);
}
function checkLoad(){
	var degnum=0;
	$("#checkLoading").show();
	degFunc=setInterval(function(){
		degnum+=6;
		$("#checkLoading img").css({"transform":"rotate("+degnum+"deg)","-ms-transform":"rotate("+degnum+"deg)"," -webkit-transform":"rotate("+degnum+"deg)"});
		if($("#checkLoading").css("display")=="none"){
			clearInterval(degFunc);
		}
	},10);
}

//-------------------------点击关闭按钮返回到主页-----------------------

function ifnull(elem){
	if(!elem) elem="";
	else elem;
	return elem;
}

//-------------------------点击关闭按钮返回到主页-----------------------
//验证输入框去掉空格是否为空
function isFilled(field){
	if(field.val().replace(' ','').length==0)return false;
	var placeholder=field.placeholder||field.attr('placeholder');
	return(field.val()!=placeholder);
}

