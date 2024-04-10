// const loggings = document.querySelector('.buy-tickets')
const buyBtns = document.querySelectorAll('.js-buy-ticket')
const closeBtn = document.querySelector('.modal-close')
const modalContainer = document.querySelector('.js-modal-container')
const closeBtn2 = document.querySelector('.modal-close2')
const modalContainer2 = document.querySelector('.js-modal-container2')
const modal = document.querySelector('.js-modal')
const modal2 = document.querySelector('.js-modal2')
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

// modal.addEventListener('click', hideBuyTickets)

// modal2.addEventListener('click', hideBuyTickets)

modalContainer.addEventListener('click', function (event) {
    event.stopPropagation()
})

modalContainer2.addEventListener('click', function (event) {
    event.stopPropagation()
})

function convertToVND(money) {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(money);
}

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
        productPriceElement.innerHTML = convertToVND(parseFloat(newPrice));
    }
}

function updateProductPriceSale(newPriceSale) {
    const productPriceSaleElement = document.querySelector('.product-pricesale');
    if (productPriceSaleElement) {
        productPriceSaleElement.innerHTML = convertToVND(parseFloat(newPriceSale));
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

function countTotalBill(data) {
    let totalAmount = 0;

    data.forEach(item => {
        const quantity = item?.quantity;
        const product = item?.product;

        // Use sale price if available, otherwise use regular price
        const price = parseFloat(product?.pricesale) || parseFloat(product?.price);

        totalAmount += quantity * price;
    });

    return totalAmount;
}

function countTotalItems(data) {
    let totalAmount = 0;

    data.forEach(item => {
        const quantity = item?.quantity;

        totalAmount += quantity;
    });

    return totalAmount;
}

// Hàm cập nhật số lượng sản phẩm trong giỏ hàng
function updateCartItemCount(product_id, quantity) {
    console.log('11111111111111111111111111')
    document.getElementById("messageContainer").innerHTML = '';
    var message = $('<div id="messageContainer2" class="alert alert-success d-flex align-items-center alert-dismissible fade show" role="alert" data-bs-autohide="false"></div>')
                .append('<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill" /></svg>')
                .append('<div>Thêm vào giỏ hàng thành công!</div>')
                .append('<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>');
    // Thêm phần tử thông báo mới vào messageContainer
    $("#messageContainer").html(message);

    setTimeout(function() {
        $("#messageContainer2").removeClass('show').addClass('fade');
        $("#messageContainer").html('');
    }, 3000);

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
            // console.log('Dữ liệu giỏ hàng:', data);
            // Xử lý dữ liệu giỏ hàng nếu cần
        })
        .catch(error => {
            console.error('Lỗi khi lấy dữ liệu giỏ hàng:', error);
        });
}

// Hàm fetch chi tiết giỏ hàng
function fetchCartDetails(cartId) {
    return fetch(`/api/cart-details/${cartId}`, {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            // console.log('Dữ liệu chi tiết giỏ hàng:', data);
            // Xử lý dữ liệu chi tiết giỏ hàng nếu cần
            return data;
        })
        .catch(error => {
            console.error('Lỗi khi lấy dữ liệu chi tiết giỏ hàng:', error);
            throw error; // Rethrow the error to be handled by the caller
        });
}

// Hàm fetch đơn hàng
function fetchOrders() {
    fetch('/orders/', {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            // console.log('Dữ liệu đơn hàng:', data);
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
            // console.log('Dữ liệu chi tiết đơn hàng:', data);
            // Xử lý dữ liệu chi tiết đơn hàng nếu cần
        })
        .catch(error => {
            console.error('Lỗi khi lấy dữ liệu chi tiết đơn hàng:', error);
        });
} 

function getAllProductsWithImages() {
    return fetch('/api/products/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Process the retrieved data with images as needed
        console.log('All products with images:', data);
        return data;
    })
    .catch(error => {
        console.error('Error fetching all products with images:', error);
    });
}

async function getAllProductsWithImages() {
    try {
      const response = await fetch('/api/product-with-type/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log('All products with images:', data);
      return data;
    } catch (error) {
      console.error('Error fetching all products with images:', error);
    }
  }
  
  function renderProductTypes(productTypes) {
    const productTypeList = document.getElementById('product-type-list');
    
    productTypes.forEach((type,index) => {
      const listItem = document.createElement('li');
      listItem.classList.add('nav-item', 'me-2');
  
      const link = document.createElement('a');
      index == 0 ? link.classList.add('btn', 'btn-outline-primary', 'border-2', 'active') : link.classList.add('btn', 'btn-outline-primary', 'border-2');
      
      link.setAttribute('data-bs-toggle', 'pill');
      link.setAttribute('href', `#tab-${type.type.product_type_id}`);
      link.textContent = type.type.name;
  
      listItem.appendChild(link);
      productTypeList.appendChild(listItem);
    })
  }
  
  function renderProducts(productsWithImages) {
    const productContainerList = document.getElementById('product-container-list');
    
    productsWithImages.forEach((productTypeInfo, index) => {
      const tabPane = document.createElement('div');
      index == 0 ? tabPane.classList.add('tab-pane', 'fade', 'show', 'p-0', 'active') : tabPane.classList.add('tab-pane', 'fade', 'show', 'p-0');
      tabPane.setAttribute('id', `tab-${productTypeInfo.type.product_type_id}`);
  
      if (productTypeInfo.type.product_type_id === 1) {
        tabPane.classList.add('active');
      }
  
      const row = document.createElement('div');
      row.classList.add('row', 'g-4');
  
      productTypeInfo.products.forEach((productInfo, index2) => {
        const col = document.createElement('div');
        col.classList.add('col-xl-3', 'col-lg-4', 'col-md-6', 'wow', 'fadeInUp', 'my-4');
        col.setAttribute('data-wow-delay', '0.1s');

        const productItem = document.createElement('div');
        productItem.classList.add('product-item', 'rounded-3', 'border', 'box-shadow-custom');

        const positionRelative = document.createElement('div');
        positionRelative.classList.add('position-relative', 'bg-light', 'overflow-hidden');
        
        const productImage = document.createElement('img');
        for (const imageInfo of productInfo.images) {
        productImage.classList.add('card-img-top', 'w-100');
        productImage.setAttribute('alt', 'Product Image');
        if (imageInfo) {
            productImage.setAttribute('src', imageInfo.url);
        } else {
            productImage.setAttribute('src', '/static/img/product-1.jpg'); // Đường dẫn mặc định cho hình ảnh sản phẩm
        }
        }

        const carrotBgcolor = document.createElement('div');
        carrotBgcolor.classList.add('carrot-bgcolor', 'rounded', 'text-white', 'position-absolute', 'start-0', 'top-0', 'm-2', 'py-1', 'px-1');
        carrotBgcolor.textContent = 'New';

        positionRelative.appendChild(productImage);
        positionRelative.appendChild(carrotBgcolor);

        const textCenter = document.createElement('div');
        textCenter.classList.add('text-center', 'p-4');

        const productLink = document.createElement('a');
        productLink.classList.add('d-block', 'h5', 'text-decoration-none', 'text-dark', 'text-lora', 'mb-2', 'text-start', 'text-truncate');
        productLink.setAttribute('href', `/products/${productInfo.product_id}`);
        productLink.textContent = productInfo.name || ' ';

        // Move the declaration here
        const textDetails = document.createElement('div');
        textDetails.classList.add('text-details');

        const productDetails = document.createElement('div');
        productDetails.classList.add('product-details', 'd-flex', 'align-items-center', 'justify-content-start');

        const textBody1 = document.createElement('div');
        textBody1.classList.add('text-body', 'text-decoration-line-through', 'text-truncate', 'text-start', 'p-0', 'convert-to-vnd');
        textBody1.textContent = productInfo.price || ' ';

        const textDanger = document.createElement('div');
        textDanger.classList.add('text-danger', 'fw-bold', 'h5', 'text-truncate', 'text-start', 'my-3', 'convert-to-vnd');
        textDanger.textContent = productInfo.pricesale || ' ';

        textDetails.appendChild(textBody1);
        textDetails.appendChild(textDanger);

        productDetails.appendChild(textDetails);

        if (productInfo.pricesale < productInfo.price) {
        const bigSaleIcon = document.createElement('img');
        bigSaleIcon.classList.add('bigsale-icon', 'mx-auto');
        bigSaleIcon.setAttribute('src', '/static/img/bigsale.gif'); // Đường dẫn mặc định cho biểu tượng giảm giá lớn
        bigSaleIcon.setAttribute('alt', 'bigsale');
        productDetails.appendChild(bigSaleIcon);
        }

        textCenter.appendChild(productLink);
        textCenter.appendChild(productDetails);

        productItem.appendChild(positionRelative);
        productItem.appendChild(textCenter);

        if (is_staff) {
        const borderTop1 = document.createElement('div');
        borderTop1.classList.add('border-top', 'd-flex');

        const small1 = document.createElement('small');
        small1.classList.add('w-50', 'text-center', 'border-end', 'py-2');

        const editLink = document.createElement('a');
        editLink.classList.add('text-body', 'text-decoration-none');
        editLink.setAttribute('href', `/products/edit/${productInfo.product_id}`);
        editLink.innerHTML = '<i class="fa fa-pen greentea-color me-2"></i>Edit';

        small1.appendChild(editLink);

        const small2 = document.createElement('small');
        small2.classList.add('w-50', 'text-center', 'py-2');

        const deleteLink = document.createElement('a');
        deleteLink.classList.add('text-body', 'text-decoration-none');
        deleteLink.setAttribute('href', `/products/delete/${productInfo.product_id}`);
        deleteLink.innerHTML = '<i class="fa fa-trash carrot-color me-2"></i>Delete';

        small2.appendChild(deleteLink);

        borderTop1.appendChild(small1);
        borderTop1.appendChild(small2);

        productItem.appendChild(borderTop1);
        } else {
        const borderTop2 = document.createElement('div');
        borderTop2.classList.add('border-top', 'd-flex');

        const small3 = document.createElement('small');
        small3.classList.add('w-50', 'text-center', 'border-end', 'py-2');

        const viewDetailButton = document.createElement('button');
        viewDetailButton.setAttribute('type', 'button');
        viewDetailButton.classList.add('btn', 'btn-transparent', 'btn-sm');

        const viewDetailLink = document.createElement('a');
        viewDetailLink.classList.add('text-body', 'text-decoration-none', 'view-detail');
        viewDetailLink.setAttribute('href', `/products/${productInfo.product_id}`);
        viewDetailLink.innerHTML = '<i class="fa fa-eye greentea-color me-2"></i>View detail';

        viewDetailButton.appendChild(viewDetailLink);
        small3.appendChild(viewDetailButton);

        const small4 = document.createElement('small');
        small4.classList.add('w-50', 'text-center', 'py-2');

        const addToCartButton = document.createElement('button');
        addToCartButton.setAttribute('type', 'button');
        addToCartButton.classList.add('btn', 'btn-transparent', 'btn-sm');

        const addToCartLink = document.createElement('a');
        addToCartLink.classList.add('text-body', 'text-decoration-none', 'pe-auto', 'add-to-cart');
        addToCartLink.setAttribute('data-product-id', productInfo.product_id);
        addToCartLink.setAttribute('onclick', `updateCartItemCount('${productInfo.product_id}', 1)`);
        addToCartLink.innerHTML = '<i class="fa fa-shopping-bag greentea-color me-2"></i>Add to cart';

        addToCartButton.appendChild(addToCartLink);
        small4.appendChild(addToCartButton);

        borderTop2.appendChild(small3);
        borderTop2.appendChild(small4);

        productItem.appendChild(borderTop2);
        }

        col.appendChild(productItem);
        row.appendChild(col);
    
      });
  
      // const col12 = document.createElement('div');
      // col12.classList.add('col-12', 'text-center', 'wow', 'fadeInUp');
      // col12.setAttribute('data-wow-delay', '0.1s');
  
      // const browseMoreLink = document.createElement('a');
      // browseMoreLink.classList.add('btn', 'btn-primary', 'rounded-pill', 'py-3', 'px-5');
      // browseMoreLink.setAttribute('href', '/products');
      // browseMoreLink.textContent = 'Browse More Products';
  
      // col12.appendChild(browseMoreLink);
      // row.appendChild(col12);
  
      tabPane.appendChild(row);
      productContainerList.appendChild(tabPane);
    });
  }
  

ZALOPAY_KEY_1='sdngKKJmqEMzvh5QQcdD2A9XBSKUNaYn'
ZALOPAY_APP_ID=2554
ZALOPAY_CALLBACK_URL='https://c056-2405-4802-90a4-50f0-64ee-63ac-8d18-fd9.ngrok-free.app/api/payment-status/'

const generateAppTransId = (orderId, createdAt) => {
  return `${createdAt.format('YYMMDD')}_${orderId}`
};

const generateCreatedAt = () => {
  return moment().utcOffset(420);
};

const generateEmbedData = (provider) => {
  const preferredPaymentMethod = [];
//   switch (provider) {
//     case ZalopaySupportedProvider.DOMESTIC_CARD:
//       preferredPaymentMethod.push('domestic_card', 'account');
//       break;
//     case ZalopaySupportedProvider.WALLET:
//       preferredPaymentMethod.push('zalopay_wallet');
//       break;
//     case ZalopaySupportedProvider.VIETQR:
//       preferredPaymentMethod.push('vietqr');
//       break;
//     case ZalopaySupportedProvider.INTERNATIONAL_CARD:
//       preferredPaymentMethod.push('international_card');
//       break;
//     case ZalopaySupportedProvider.ZALOPAY_GATEWAY:
//     default:
//       break;
//   }
  const embedData = {
    preferred_payment_method: preferredPaymentMethod,
    redirecturl: 'https://c056-2405-4802-90a4-50f0-64ee-63ac-8d18-fd9.ngrok-free.app/order/payment/success'
  };
  return JSON.stringify(embedData);
};

const generateItemData = (items) => {
  return JSON.stringify(items || []);
};

const generateMacForOrderCreation = (payload) => {
  const payloadData = [
    payload.app_id.toString(),
    payload.app_trans_id,
    payload.app_user,
    payload.amount.toString(),
    payload.app_time.toString(),
    payload.embed_data,
    payload.item
  ].filter(value => value !== undefined && value !== null && value !== "");
  
  return hashMacByKey1(payloadData.join('|'));
};


// const generateMacForOrderCreation = (payload) => {
//   const payloadData = remove(Array.of(payload.app_id.toString(),
//     payload.app_trans_id,
//     payload.app_user,
//     payload.amount.toString(),
//     payload.app_time.toString(),
//     payload.embed_data,
//     payload.item), value => value);
//   return hashMacByKey1(join(payloadData, '|'));
// };

const hashMacByKey1 = (data) => {
  return hashMac(ZALOPAY_KEY_1, data);
};

const hashMac = (key, data) => {
    const hmac = CryptoJS.HmacSHA256(data, key);
    const mac = hmac.toString(CryptoJS.enc.Hex);
    return mac;
};

// Create Order ZaloPay:
function createOrder({
    customerFullName,
    totalAmount,
    order,
    providerId,
    items,
  }) {
    const createdTime = generateCreatedAt();
    console.log("🚀 ~ createdTime:", createdTime)
    const payload = {
      key1: ZALOPAY_KEY_1,
      app_id: parseInt(ZALOPAY_APP_ID),
      app_user: customerFullName,
      app_time: createdTime.valueOf(),
      app_trans_id: generateAppTransId(order.id, createdTime),
      amount: totalAmount,
      bank_code: "",
      embed_data: generateEmbedData(providerId),
      item: generateItemData(items),
      description: `DoubleTBad - Thanh toán đơn hàng #${order.displayId}`,
      callback_url: ZALOPAY_CALLBACK_URL,
    };
    payload.mac = generateMacForOrderCreation(payload);
    console.log("🚀 ~ payload:", payload)

    fetch('https://sb-openapi.zalopay.vn/v2/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Processed image:', data);
        setResponseData(data);
      })
      .catch(error => {
        console.error('Error when processing image:', error);
      })
  }
