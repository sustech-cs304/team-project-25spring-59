import axios from 'axios'

export const baseurl = 'http://10.12.184.92:8000'
export const remoteurl = 'http://10.32.65.173'
const request = axios.create({

    // baseURL: 'https://m1.apifoxmock.com/m1/6156254-5848272-default'
    baseURL: baseurl
    // baseURL: remoteurl
})

export default request