function getid(id) {
    return document.getElementById(id);
}
function getName(name) {
    return document.getElementsByName(name);
}
function getClassName(cname) {
    return document.getElementsByClassName(cname);
}
function GetXmlHttp() {
    var xmlhtp ;
    if (window.XMLHttpRequest){
        xmlhtp =new XMLHttpRequest();
    }else{
        xmlhtp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xmlhtp;
}

// 发送评论
function sendcomment() {
    var textarea = getid('textarea');
    var code = getid('code');
    if (!textarea | !code){
        showmsg("请将数据补充完整");
        $('#myModal').modal('show');
        return ;
    }
    if (textarea.value.length > 300){
        showmsg("评论要求少于300字");
        $('#myModal').modal('show');
        return ;
    }
    var xmlhttp = GetXmlHttp();
    xmlhttp.open('POST', commetnurl, true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    var data = "csrfmiddlewaretoken=" + form_comment.csrfmiddlewaretoken.value;
    data += "&code=" + code.value;
    data += "&textarea=" + textarea.value;
    data += "&artid=" + getid('artid').value;
    xmlhttp.send(data);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
            var data = tojson(xmlhttp.responseText);
            switch (data['info']){
                case 0:
                    // 数据不完整
                    showmsg("请将数据补充完整");
                    $('#myModal').modal('show');
                    break;
                case 1:
                    // 验证码不正确
                    showmsg("验证码错误");
                    $('#myModal').modal('show');
                    break;
                case 2:
                    // 内容xss
                    break;
                case 3:
                    // 评论成功，返回此文下所有评论 或 重新验证
                    textarea.value = "";
                    code.value = "";
                    location.reload()
                    break;
                case 4:
                    // 内容长度限制
                    showmsg("评论要求少于300字");
                    $('#myModal').modal('show');
                    break;
            }
        }
    }
}

function tojson(str) {
     var json = (new Function("return"+str))();
     return json;
}

function showmsg(str) {
    getid('modalbody').innerText = "";
    getid('modalbody').innerText = str;
}
