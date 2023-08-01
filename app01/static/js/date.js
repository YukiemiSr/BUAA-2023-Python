function date() {
    var _date = document.getElementById("date");
    var _day = document.getElementById("day")
    var _time = document.getElementById("time")
    let cha = new Date();//获取当前时间
    var year = cha.getFullYear(); //获取当前年份
    var mon = cha.getMonth() + 1; //获取当前月份
    var da = cha.getDate(); //获取当前日期
    var day = cha.getDay(); //获取当前星期几
    var h = cha.getHours(); //获取小时
    var m = cha.getMinutes(); //获取分钟
    var s = cha.getSeconds(); //获取秒
    //假如hours小于12字符串am，大于12pm  hours-12
    var nam = "";
    if (h > 12) {
        h -= 12;
        nam = "pm"
    } else {
        nam = "am"
    }
    //day是多少值就是相应的字符串
    if (day == 0) {
        day = "日"
    }
    if (day == 1) {
        day = "一"
    }
    if (day == 2) {
        day = "二"
    }
    if (day == 3) {
        day = "三"
    }
    if (day == 4) {
        day = "四"
    }
    if (day == 5) {
        day = "五"
    }
    if (day == 6) {
        day = "六"
    }
    // 拼+0
    if (h < 10) {
        h = `0${h}`
    }
    // if(h<0){
    //   h=`0${h}`
    // }
    if (m < 10) {
        m = `0${m}`
    }
    if (s < 10) {
        s = `0${s}`
    }
    //算出日期
    _date.innerHTML = `${year}年${mon}月${da}日`
    _day.innerHTML = `星期${day}`
    _time.innerHTML = `${h}:${m}:${s} ${nam}`
}