const itemSizesData = document.getElementById("item-sizes-data");
const itemSizesQuantity = document.getElementById("items-size-quantity")
const defaultQuantity = document.getElementById("default-quantity")



addEventListener("change", e=>{
    console.log(e.target.value)
    const selectedSize = e.target.value



    $.ajax({
        type: 'GET',
        url: '/models-json/' + selectedSize,
        success: function(response){
            console.log(response)
            const QuantityData = response.data
            QuantityData.map(item => {
                let i = 1;
                while (i <= item.quantity){
                const option = document.createElement('option')
                option.setAttribute('value',i);
                option.textContent = i;
                itemSizesQuantity.appendChild(option);
                i++;
                }
            })},
        error: function(error){
            console.log(error)
            }
    })
});

