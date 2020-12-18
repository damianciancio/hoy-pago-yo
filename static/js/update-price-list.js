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

    function raise_percent() {
        var amount = $('#amount-to-raise').val();
        var multiplier = (amount / 100) + 1;
        $('#update-pricelist-table').find('tbody').find('tr').each((indx, obj) => {
            var price = $(obj).find('.price').find('input').val();
            $(obj).find('.price').find('input').val(Math.round((price * multiplier) * 100) / 100);
        });
    }

    function raise_number() {
        var amount = parseInt($('#amount-to-raise').val());
        $('#update-pricelist-table').find('tbody').find('tr').each((indx, obj) => {
            var price = $(obj).find('.price').find('input').val();
            price = parseInt(price);
            $(obj).find('.price').find('input').val(Math.round((price + amount) * 100) / 100);
        });
    }

    $('#btn-raise-percent').on('click', raise_percent);
    $('#btn-raise-number').on('click', raise_number);
    $('#btn-undo').on('click', () => location.reload());
    btn-undo

});
