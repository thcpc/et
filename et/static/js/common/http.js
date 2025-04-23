// app.js
export function httpGet(url, params={}) {
    return new Promise((resolve, reject)=>{
        axios.get(url, {params: params}).then(response=>{
            resolve(response.data)
        }).catch(err=>{
            reject(err)
        })
    });
}

export function httpPostJson(url, data={}) {
    return new Promise((resolve, reject)=>{
        axios.post(url, data, {headers:{'Content-Type':'application/json'}}).then(response=>{
            resolve(response.data)
        }).catch(err=>{
            reject(err)
        })
    });
}
