const date = new Date()

// split the 'Date' struct into specific readable data
export function getFullDate(date) {
    const dateList = {}
    dateList.year = date.getFullYear();
    dateList.month = date.getMonth()+1;
    dateList.day = date.getDate();
    dateList.week = changeDateWeek(date.getDay());
    dateList.hour = date.getHours()
    dateList.minute = date.getMinutes()
    dateList.second = date.getSeconds()
    return dateList
}

function changeDateWeek(week) {
    const weekList = ['天', '一', '二', '三', '四', '五', '六']
    return weekList[week]
}