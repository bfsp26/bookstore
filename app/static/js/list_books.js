(function () {
    const btnsBuyBook = document.querySelectorAll('.btnBuyBook');
    let isbnSelectedBook = null;
    const csrf_token = document.querySelector("[name='csrf-token']").value;

    btnsBuyBook.forEach((btn) => {
        btn.addEventListener('click', function () {
            isbnSelectedBook = this.id;
            confirmPurchase();
        });
    });

    const confirmPurchase = () => {

        Swal.fire({
            title: 'Are you sure you want to buy this book?',
            inputAttributes: {
                autocapitalize: 'off'
            },
            showCancelButton: true,
            confirmButtonText: 'Buy',
            showLoaderOnConfirm: true,
            preConfirm: async () => {
                console.log(window.origin)
                return await fetch(`${window.origin}/buyBook`, {
                    method: 'POST',
                    mode: 'same-origin',
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': csrf_token
                    },
                    body: JSON.stringify({
                        'isbn': isbnSelectedBook
                    })
                }).then(response => {
                    if (!response.ok) {
                        notifications('Error!', response.statusText, 'error', 'Close')
                    }
                    return response.json();
                }).then(data => {
                    if (data.success) {
                        notifications('Success', "Successfully purchased book", 'success', 'OK!')
                    } else {
                        notifications('Warning', data.message, 'warning', 'OK')
                    }
                }).catch(error => {
                    notifications('Error!', error, 'error', 'Close')
                });
            },
            allowOutsideClick: () => false,
            allowEscapeKey: () => false
        });
    };
})();

