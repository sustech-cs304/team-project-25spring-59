import axios from 'axios'

export const baseurl = 'http://localhost:8000'
// export const baseurl = 'http://10.26.63.155:8000'  // shuyang
// export const baseurl = 'http://10.12.184.92:8000'  // shiyansong
const request = axios.create({

    // baseURL: 'https://m1.apifoxmock.com/m1/6156254-5848272-default'
    baseURL: baseurl
})

export default request