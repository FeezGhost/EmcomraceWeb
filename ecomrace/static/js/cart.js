var updateBtns = document.getElementsByClassName('update-cart')
var cartItems = document.getElementById('cart-total')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product;
		var action = this.dataset.action;
		console.log('productId:', productId, 'Action:', action);
		console.log('USER:', user);

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action);
		}else{
			updateUserOrder(productId, action);
		}
	})
}

function updateUserOrder(productId, action){
    console.log('User is authenticated, sending data...');
    
    var url ='/update_item/';
    $.ajax({
        url: url,
        data: {
          productId: productId,
          action: action,
        },
        dataType: "json",
    
        success: function (data) {
          if (data.is_taken) {
            alert("A user with this username already exists.");
          }
          console.log(data);
        },
      });
      cartItems.innerText = (parseInt(cartItems.innerText) + 1);

      location.reload();

      console.log("productId:", productId, "action:", action);
      console.log("USER:", user);
      console.log(" User is logged in , Sending data...");
    
    
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}