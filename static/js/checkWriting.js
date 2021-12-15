// 글쓰기 폼 유효성 검사
function checkWriting(){
    var form = document.writeForm;
    var title = form.title.value;
    var content = form.content.value;

    if(title == ""){
        alert("제목을 입력해주세요.");
        form.title.focus();
        return false;
    }
    else if(content == ""){
        alert("내용을 입력해주세요.");
        form.content.focus();
        return false;
    }
    else{
        form.submit();
    }
}