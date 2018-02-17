const request = require('request')
const fs = require('fs')
const co = require('co')

const result = JSON.parse(fs.readFileSync("./urls.json"))

const rq = (url) => {
    return new Promise((resolve, reject) => {
        request(url, (error, response, body) => {
            if (!error && response.statusCode == 200) {
                resolve(body)
            } else {
                console.log('connect fail, code !== 200')
                console.log('error url:' + url)
                reject(error)
            }
        })
    })
}

const jsdom = require("jsdom")
const { JSDOM } = jsdom

function trim(str){
    return str.replace(/(^\s*)|(\s*$)/g, '')
}

const deal_with_content = (content) => {
    const dom = new JSDOM(content)
    const scripts = dom.window.document.getElementsByTagName('script')
    for (let i = scripts.length - 1; i >= 0; i--) {
        let script = scripts[i]
        script.innerHTML = ''
    }
    const newContent = dom.window.document.querySelector("#js_article").textContent
    return newContent
}

const load_content = (url,ind) => {
    co(function*() {
        let content = yield rq(url)
        const text = deal_with_content(content)
        fs.writeFileSync(`./result/${ind}.txt`,  text)// decodeURI(encodeURI(
    })
}

result.forEach((el,ind)=>{
    console.log(`正在请求第${ind}篇文章...`)
    load_content(el,ind)
})
