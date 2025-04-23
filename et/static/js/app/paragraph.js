
export default {
    delimiters: ["[[", "]]"],
    data() {
        return {content: []}
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