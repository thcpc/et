// app.js
import { httpGet, httpPostJson } from 'http://127.0.0.1:8000/static/js/common/http.js'

export default {
    delimiters: ["[[", "]]"],
    data() {
        return {books: [], name: "et",image_base64: ""}
    },
    mounted() {
        this.fetchData()
    },
    methods: {
        fetchData() {
            httpGet("api/books").then((resp)=>{
                this.books = resp;
            })
            httpGet("api/plantumls").then((resp)=>{
                this.image_base64 = resp;
            })

        },
        newBook(){
            httpPostJson("api/newBook", {title: "cpc"}).then((resp)=>{
                console.log(resp)
            })
        }
    }
}