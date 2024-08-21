function song_time(time) {
    time =parseInt(time/1000)
    minute = parseInt(time / 60)
    second = time % 60
    return minute + ':' + String(second).padStart(2,"0");
}

function plyy_time(time) {
    time =parseInt(time/60000)
    hour = parseInt(time / 60)
    minute = time % 60
    if (hour) {
        hour = hour + '시간 '
    } else {
        hour = ''
    }
    return hour + String(minute).padStart(2,"0") + '분';
}