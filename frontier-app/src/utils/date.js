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

// change 'Date' struct to the short-ISO form: YYYY-MM-DDTHH:MM:SS
export function toISO(date) {
    const dateList = getFullDate(date);
    const month = dateList.month.toString().padStart(2, '0')
    const day = dateList.day.toString().padStart(2, '0')
    const hour = dateList.hour.toString().padStart(2, '0')
    const minute = dateList.minute.toString().padStart(2, '0')
    const second = dateList.second.toString().padStart(2, '0')
    return `${dateList.year}-${month}-${day}T${hour}:${minute}:${second}`
}

// change 'Date' struct to the short-ISO form without T: YYYY-MM-DD HH:MM:SS
export function toFormal(date) {
    const iso = toISO(date)
    return iso.replace('T', '')
}

function changeDateWeek(week) {
    const weekList = ['天', '一', '二', '三', '四', '五', '六']
    return weekList[week]
}