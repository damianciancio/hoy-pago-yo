jQuery(document).ready(() => {


       new Vue({
            el: '#products-list',
            delimiters: ['{$','$}'],
            data() {
                return {
                    products: [],
                    searchText: "",
                    productsFiltered: []
                }
            },
            mounted() {
                var app = this;
                jQuery.ajax('/rest/products').done((resp) => {
                    app.products = JSON.parse(resp);
                    app.search();
                });
            },
            methods: {
                loadProduct(product) {
                    $('input[name="id_product"]').val(product.id_product)
                    $('input[name="product_description"]').val(product.description)

                },
                search() {
                    var searchText = this.searchText.toUpperCase();
                    this.productsFiltered = this.products.map((product) => product);
                    this.productsFiltered = this.products.filter((product) => {
                        return product.description.toUpperCase().includes(searchText);
                    });
                }
            }
       })
});
