window.onresize = function(event) {
    resizeAll();
};

window.onload = function(event) {
    resizeAll();
}

function resizeAll(){
    // console.log('.documentElement.scrollHeight = ' + document.documentElement.scrollHeight);
    // console.log('.body.clientHeight = ' + document.body.clientHeight);
    // console.log('window.outerHeight = ' + window.outerHeight);
    if (document.documentElement.scrollHeight > document.body.clientHeight + 41){
        document.querySelector('footer').style.position = 'relative'
    }else{
        document.querySelector('footer').style.position = 'absolute'
    }
}