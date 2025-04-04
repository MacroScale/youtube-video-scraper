function isJsonString(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

let fs = require('fs')

fs.readFile('../out/youtube_data.json', 'utf8', (err, data) => {
    if (err) {throw err}
    let validJson = isJsonString(data.toString())

    console.log("is valid json: ", validJson)
    if (validJson){
        let jData= JSON.parse(data)
        console.log("Length", jData.length)
        //console.log("First entry:", jData[0]);
        //console.log("Last entry:", jData[jData.length - 1]);
    }
});


