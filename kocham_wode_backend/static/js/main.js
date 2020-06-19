function formatJson() {
    var ta = $("#results textarea");
    
    let raw = JSON.parse(ta.val())
    
    for (var key in raw) {
        raw[key] = JSON.parse(raw[key])
    }

    var textedJson = JSON.stringify(raw, undefined, 4);
    
    ta.text(textedJson);
}

formatJson()

