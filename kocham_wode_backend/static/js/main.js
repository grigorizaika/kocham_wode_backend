function formatJson() {
    var ta = $("#results textarea");
    
    let raw = JSON.parse(ta.val())

    // for (var key in raw) {
        // raw[key] = JSON.parse(raw[key])
    // }

    var textedJson = JSON.stringify(raw, undefined, 4);
    
    ta.text(textedJson);
}

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute(
        'href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text)
    );
    element.setAttribute('download', filename);
  
    element.style.display = 'none';
    document.body.appendChild(element);
  
    element.click();
  
    document.body.removeChild(element);
}


formatJson()