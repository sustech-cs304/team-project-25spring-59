import axios from 'axios'

const request = axios.create({

    // baseURL: 'https://m1.apifoxmock.com/m1/6156254-5848272-default'
    baseURL: 'http://localhost:8000'
})

export default request