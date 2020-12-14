jQuery(document).ready(() => {
       jQuery.ajax('/rest/clients').done((resp) => console.log(resp));

        $('input[name="new_client"]').on('change', () => {
            var isChecked = $('input[name="new_client"]').prop('checked');
            $('input[name="id_client"]').val("")

        });

       new Vue({
            el: '#client-list',
            delimiters: ['{$','$}'],
            data() {
                return {
                    clients: [],
                    searchText: "",
                    clientsFiltered: []
                }
            },
            mounted() {
                var app = this;
                jQuery.ajax('/rest/clients').done((resp) => {
                    app.clients = JSON.parse(resp);
                    app.search();
                });
            },
            methods: {
                loadClient(client) {
                    $('input[name="new_client"]').prop('checked', false)
                    $('input[name="id_client"]').val(client.id_client)
                    $('input[name="name"]').val(client.name)
                    $('input[name="address"]').val(client.address)
                    $('input[name="telephone_number"]').val(client.telephone_number)

                },
                search() {
                    var searchText = this.searchText.toUpperCase();
                    this.clientsFiltered = this.clients.map((cli) => cli);
                    this.clientsFiltered = this.clients.filter((cli) => {
                        return cli.name.toUpperCase().includes(searchText) ||
                            cli.address.toUpperCase().includes(searchText) ||
                            cli.telephone_number.toUpperCase().includes(searchText);

                    });
                }
            }
       })
});
