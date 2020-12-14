jQuery(document).ready(() => {

    $('#update-price-list').on('click', (event) => {
        formData = JSON.stringify(getFormData());
        $.ajax(
            {
                url: '/productos/actualizar-lista',
                type: 'post',
                data: {
                    products: formData
                }
            }
        ).done(() => {
            location.reload()
        });
    });

    function getFormData() {
        var dataList = []
        $('#update-pricelist-table').find('tbody').find('tr').each((indx, obj) => {
            var id_product = $(obj).find('.id_product').attr('data-value');
            var price = $(obj).find('.price').find('input').val();
            dataList.push({
                id_product: id_product,
                price: price
            });
        });
        return dataList;
    }

});
