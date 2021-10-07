let itemSizesData = document.getElementById("item-sizes-data");
const itemSizesQuantity = document.getElementById("items-size-quantity")


itemSizesData.addEventListener("click", e=>{
    console.log(e.target.value)
    const selectedSize = e.target.value
    itemSizesQuantity.innerHTML = ""

    $.ajax({
        type: 'GET',
        url: '/models-json/' + selectedSize,
        success: function(response){
            const QuantityData = response.data
            QuantityData.forEach(function(item) {
                let i = 1;
                while (i <= item.quantity){
                    const option = document.createElement('option');
                    option.setAttribute('value', i);
                    option.setAttribute('parent_id', item.product_id)
                    option.textContent = i;
                    itemSizesQuantity.appendChild(option);
                    i++;


                };
                $("#price").empty().append(item.price);
                $("#total_price").empty().append(item.price);

            })},
        error: function(error){
            console.log(error)
            }
    })
});


itemSizesQuantity.addEventListener("click", e=>{
    const selectedSize = e.target.value
    const price = document.getElementById("price")

    $("#total_price").empty().append(selectedSize * price.textContent);
    })