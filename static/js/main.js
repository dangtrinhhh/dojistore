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

modalContainer.addEventListener('click', function(event) {
    event.stopPropagation()
})

modalContainer2.addEventListener('click', function(event) {
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

document.querySelectorAll('.add-to-cart').forEach(function (button) {
    button.addEventListener('click', function (event) {
        event.preventDefault();

        // Lấy id sản phẩm từ thuộc tính data
        var productId = button.getAttribute('data-product-id');

        // Thực hiện các thao tác thêm sản phẩm vào giỏ hàng ở đây
        // ...

        // Cập nhật số lượng sản phẩm trong giỏ hàng
        updateCartItemCount();
    });
});

// Hàm cập nhật số lượng sản phẩm trong giỏ hàng
function updateCartItemCount() {
    // Thực hiện logic để lấy số lượng sản phẩm trong giỏ hàng (tùy thuộc vào cách bạn triển khai giỏ hàng)
    var cartItemCount = 10; // Đổi số này bằng số lượng thực tế trong giỏ hàng

    // Cập nhật số lượng trên giao diện
    document.getElementById('cart-item-count').innerText = cartItemCount;
}