import { httpGet, httpPostJson } from 'http://127.0.0.1:8000/static/js/common/http.js'

export default {
    delimiters: ["[[", "]]"],
    data() {
        return {paragraphs: []}
    },
    mounted() {
        this.fetchData()
    },
    methods: {
        fetchData() {
            httpGet("api/page", {"docID":1, "pageId":1}).then((resp)=>{
                this.paragraphs = resp;
            })
        },
    }
}