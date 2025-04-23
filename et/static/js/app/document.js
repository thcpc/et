import { httpGet, httpPostJson } from 'http://127.0.0.1:8000/static/js/common/http.js'

export default {
    delimiters: ["[[", "]]"],
    data() {
        return { pages: []}
    },
    mounted() {
        this.fetchData()
    },
    methods: {
        fetchData() {
            httpGet("api/document", {"docId":1}).then((resp)=>{
                this.pages = resp;
            })
        },
    }
}