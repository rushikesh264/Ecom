var updateBtns=document.getElementsByClassName('update-cart');

for(var i = 0; i < updateBtns.length; i++)
{
    updateBtns[i].addEventListener('click',function(){
        var productid = this.dataset.product
        var action=this.dataset.action
        if(user === 'AnonymousUser')
        {
            addCookieItem(productid,action)
        }
        else{
            additem(productid,action)
        }
    })
}

// #function for adding cookies
function addCookieItem(productid,action)
{
    if(action == 'add')
    {
        if(cart[productid] == undefined)
        {
            cart[productid] = {'quantity':1}
        }
        else{
            cart[productid]['quantity'] += 1
        }
    }
    else if(action == 'remove')
    {
        cart[productid]['quantity'] -= 1
        if(cart[productid]['quantity'] <= 0)
        {
            console.log('Cookie of item deleted')
            delete cart[productid]
        }
    }
    console.log("Cart:",cart)

    //setting updated cart into the cookie
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

    //reload page
    location.reload()
}

function  additem(productid,action)
{
    
    url = '/update_item/'
    fetch(url,
        {
            method:'POST',
            headers:{
                    'Content-Type':'application/json',
                    'X-CSRFToken':csrftoken
                   },
            body:JSON.stringify({'productID':productid,'Action':action})
        })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log("data:",data)
        location.reload()
    })
}