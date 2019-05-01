// function sendLink(aTag) {
    
//     theLink = aTag.dataset.link;
//     console.log(theLink);
//     $.ajax({
//         url:'/reviews',
//         type:"POST",
//         data: JSON.stringify({"link": theLink}),
//         contentType:"application/json; charset=utf-8",
//         dataType:"json",
//         success: function(){
//            alert("success!");
//         }
//     });
// }

function sendLink(aTag) {
    
    theLink = aTag.dataset.link;
    alert(theLink);

    data = {
        link: theLink
    };
    
    fetch(`${window.origin}/reviews`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(data),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    });
}





$.ajaxSetup({
  contentType: "application/json; charset=utf-8"
});