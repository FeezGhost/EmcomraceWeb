let updateBtns = document.querySelectorAll('.update-cart');
for(let i = 0 ; i < updateBtns.length ; i++){
    updateBtns[i].addEventListener('click', () =>{
        let productId =updateBtns[i].dataset.product;
        let action = updateBtns[i].dataset.action;
        
        if( user === 'AnonymousUser'){
            console.log('Not Logged in');
        }
        else{
            updateUserOrder(productId,  action);
        }
    });
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


function updateUserOrder ( productId, action){
    console.log('User : ' ,user, 'is  logged in Sending data');
    const url = 'update_item/';
    fetch(url,{
        method : 'POST',
        headers : {
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action}),
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        console.log('data: ', data);
    });

}