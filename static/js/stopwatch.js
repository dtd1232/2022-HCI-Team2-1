let timerId;
let time = 0;
const stopwatch = document.getElementById("stopwatch");
let  hour, min, sec;
let score;


function printTime() {
    time++;
    stopwatch.innerText = getTimeFormatString();
}

//시계 시작 - 재귀호출로 반복실행
function startClock() {
    printTime();
    stopClock();
    timerId = setTimeout(startClock, 1000);
    score = Math.random() * 100;
    console.log(score)
    var obj = document.getElementById("cameraContent");
    var obj2 = document.getElementById("current_status")
    if(score > 80) {
        obj.style.border = "10px solid greenyellow";
        obj2.style.color = "greenyellow";
        obj2.innerHTML = "Perfect!"
    }
    else if(score > 60) {
        obj.style.border = "10px solid darkorange";
        obj2.style.color = "darkorange";
        obj2.innerHTML = "Good"
    }
    else {
        obj.style.border = "10px solid red";
        obj2.style.color = "red";
        obj2.innerHTML = "Bad..."
    }
}

//시계 중지
function stopClock() {
    if (timerId != null) {
        clearTimeout(timerId);
    }
}

// 시계 초기화
function resetClock() {
    stopClock()
    stopwatch.innerText = "00:00:00";
    time = 0;
}

// 시간(int)을 시, 분, 초 문자열로 변환
function getTimeFormatString() {
    hour = parseInt(String(time / (60 * 60)));
    min = parseInt(String((time - (hour * 60 * 60)) / 60));
    sec = time % 60;

    return String(hour).padStart(2, '0') + ":" + String(min).padStart(2, '0') + ":" + String(sec).padStart(2, '0');
}