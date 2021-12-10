// 회원가입 유효성(validation) 검사

function checkMember(){
    var form = document.regForm;
    var id = form.mid.value;    // id는 5글자
    var pwd1 = form.passwd.value;    // pw 8글자, 영문자, 숫자, 특수문자 포함
    var pwd2 = form.passwd_confirm.value;
    var name = form.name.value;


    // 비밀번호 정규 표현식 생성
    var pwd_pat1 = /[0-9A-Za-z]/    // 영문자, 숫자
    var pwd_pat2 = /[~!@#$%^&*]/      // 특수문자

    if(id.length != 5){
        alert("아이디는 5자만 가능합니다.");
        form.mid.select()
        return false;
    }
    else if(pwd1.length != 8 || !pwd_pat1.test(pwd1) || !pwd_pat2.test(pwd1)){
        alert("비밀번호는 영문자, 숫자, 특수문자 포함 8자리입니다.")
        form.passwd.select()
        return false;
    }
    else if(pwd1 != pwd2){
        alert("비밀번호를 동일하게 입력해주세요.")
        form.passwd_confirm.select()
        return false;
    }
    else if(name == ""){
        alert("이름은 필수 입력 사항입니다.")
        form.name.select()
        return false;
    }
    else{
        form.submit();
    }
}