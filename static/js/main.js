// const loggings = document.querySelector('.buy-tickets')
const buyBtns = document.querySelectorAll('.js-buy-ticket')
const closeBtn = document.querySelector('.modal-close')
const modalContainer = document.querySelector('.js-modal-container')
const closeBtn2 = document.querySelector('.modal-close2')
const modalContainer2 = document.querySelector('.js-modal-container2')
const modal = document.querySelector('.js-modal')
const modal2 = document.querySelector('#modal2')
const loginBtns = document.querySelectorAll('.btn-login')
const registerBtns = document.querySelectorAll('.btn-register')

for (const loginBtn of loginBtns) {
    loginBtn.addEventListener('click', () => {
        modal2.classList.remove("open")
        modal.classList.add("open")
        modal.classList.add("animated")
        modal.classList.add("FadeIn")
    })
}

for (const registerBtn of registerBtns) {
    registerBtn.addEventListener('click', () => {
        modal.classList.remove("open")
        modal2.classList.add("open")
        modal2.classList.add("animated")
        modal2.classList.add("FadeIn")
    })
}

for (const buyBtn of buyBtns) {
    buyBtn.addEventListener('click', showBuyTickets)
}


function hideBuyTickets() {
    modal.classList.remove("open")
}

function hideBuyTickets2() {
    modal2.classList.remove("open")
}

// loggings.addEventListener('click', hideBuyTickets)

closeBtn.addEventListener('click', hideBuyTickets)
closeBtn2.addEventListener('click', hideBuyTickets2)

modal.addEventListener('click', hideBuyTickets)

modal2.addEventListener('click', hideBuyTickets)

modalContainer.addEventListener('click', function (event) {
    event.stopPropagation()
})

modalContainer2.addEventListener('click', function (event) {
    event.stopPropagation()
})

// Product Handle Function

function updateProductName(newName) {
    const productNameElement = document.querySelector('.product-name');
    if (productNameElement) {
        productNameElement.textContent = newName;
    }
}

function updateProductPrice(newPrice) {
    const productPriceElement = document.querySelector('.product-price');
    if (productPriceElement) {
        productPriceElement.textContent = newPrice + " VND";
    }
}

function updateProductPriceSale(newPriceSale) {
    const productPriceSaleElement = document.querySelector('.product-pricesale');
    if (productPriceSaleElement) {
        productPriceSaleElement.textContent = newPriceSale + " VND";
    }
}

function updateProductImage(inputElement) {
    const productImageElement = document.getElementById('product-image');
    if (productImageElement && inputElement.files && inputElement.files[0]) {
        const newImage = URL.createObjectURL(inputElement.files[0]);
        productImageElement.src = newImage;
    }
}

function updateSaleIcon() {
    const priceInput = document.querySelector('input[name="price"]');
    const pricesaleInput = document.querySelector('input[name="pricesale"]');
    const bigsaleIcon = document.querySelector('.bigsale-icon');

    if (priceInput && pricesaleInput && bigsaleIcon) {
        const price = parseFloat(priceInput.value);
        const pricesale = parseFloat(pricesaleInput.value);

        updateProductPrice(priceInput.value);
        updateProductPriceSale(pricesaleInput.value);

        if (!isNaN(price) && !isNaN(pricesale) && pricesale < price) {
            bigsaleIcon.style.display = 'block';
        } else {
            bigsaleIcon.style.display = 'none';
        }
    }
}

// Blog Handle Function:


function updateBlogTitle(newTitle) {
    const blogTitleElement = document.getElementById('id_title');
    if (blogTitleElement) {
        blogTitleElement.textContent = newTitle;
    }
}

function updateBlogContent(newContent) {
    const blogContentElement = document.getElementById('id_content');
    if (blogContentElement) {
        blogContentElement.textContent = newContent;
    }
}

function updateBlogImage(inputElement) {
    const blogImageElement = document.getElementById('id_image');
    if (blogImageElement && inputElement.files && inputElement.files[0]) {
        const newImage = URL.createObjectURL(inputElement.files[0]);
        blogImageElement.src = newImage;
    }
}

// Profile > Password Function
function togglePasswordFields() {
    const passwordFields = document.getElementById("password-fields");
    passwordFields.style.display = passwordFields.style.display === "none" ? "block" : "none";
}


// Handle API

// Hàm cập nhật số lượng sản phẩm trong giỏ hàng
// function updateCartItemCount(product_id, quantity) {
//   const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

//   console.log("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
//   console.log(csrfToken)
//   // Thực hiện logic để lấy số lượng sản phẩm trong giỏ hàng (tùy thuộc vào cách bạn triển khai giỏ hàng)
//   var cartItemCount = 10; // Đổi số này bằng số lượng thực tế trong giỏ hàng

//   // Cập nhật số lượng trên giao diện
//   document.getElementById('cart-item-count').innerText = cartItemCount;

//   const productId = 1; // ID của sản phẩm
//   const quantity = 2; // Số lượng sản phẩm

//   fetch('/api/add-to-cart/', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//       'X-CSRFToken': csrfToken, // Điền CSRF token nếu bạn đang sử dụng CSRF protection
//     },
//     body: JSON.stringify({ product_id: productId, quantity }),
//   })
//     .then(response => response.json())
//     .then(data => {
//       console.log('Giỏ hàng đã được cập nhật:', data);
//       // Xử lý dữ liệu giỏ hàng nếu cần
//     })
//     .catch(error => {
//       console.error('Lỗi khi thêm vào giỏ hàng:', error);
//     });

// }
// Hàm cập nhật số lượng sản phẩm trong giỏ hàng
function updateCartItemCount(product_id, quantity) {
    // Lấy giá trị của CSRF token từ trang web
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    // Thực hiện fetch với CSRF token lấy từ trang web
    fetch('/api/add-to-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ product_id: product_id, quantity: quantity }), // Sử dụng tham số truyền vào
    })
        .then(response => response.json())
        .then(data => {
            // Xử lý dữ liệu giỏ hàng nếu cần
            console.log('Giỏ hàng đã được cập nhật:', data);
            // Cập nhật số lượng trên giao diện
            var cartItemCount = parseInt(document.getElementById('cart-item-count').innerText);
            document.getElementById('cart-item-count').innerText = cartItemCount + quantity;
        })
        .catch(error => {
            console.error('Lỗi khi thêm vào giỏ hàng:', error);
        });
}

// Hàm fetch giỏ hàng
function fetchCart() {
    fetch('/api/carts/', {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            console.log('Dữ liệu giỏ hàng:', data);
            // Xử lý dữ liệu giỏ hàng nếu cần
        })
        .catch(error => {
            console.error('Lỗi khi lấy dữ liệu giỏ hàng:', error);
        });
}

// Hàm fetch chi tiết giỏ hàng
function fetchCartDetails(cartId) {
    fetch(`/api/cart-details/${cartId}`, {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            console.log('Dữ liệu chi tiết giỏ hàng:', data);
            // Xử lý dữ liệu chi tiết giỏ hàng nếu cần
        })
        .catch(error => {
            console.error('Lỗi khi lấy dữ liệu chi tiết giỏ hàng:', error);
        });
}

// Hàm fetch đơn hàng
function fetchOrders() {
    fetch('/orders/', {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            console.log('Dữ liệu đơn hàng:', data);
            // Xử lý dữ liệu đơn hàng nếu cần
        })
        .catch(error => {
            console.error('Lỗi khi lấy dữ liệu đơn hàng:', error);
        });
}

// Hàm fetch chi tiết đơn hàng
function fetchOrderDetails(orderId) {
    fetch(`/order-details/?order=${orderId}`, {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            console.log('Dữ liệu chi tiết đơn hàng:', data);
            // Xử lý dữ liệu chi tiết đơn hàng nếu cần
        })
        .catch(error => {
            console.error('Lỗi khi lấy dữ liệu chi tiết đơn hàng:', error);
        });
}  