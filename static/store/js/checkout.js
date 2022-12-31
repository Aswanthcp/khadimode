
$(document).ready(function () {
    $('.paywithrazorpay').click(function (e) {
        e.preventDefault();
        var last_name = $("[name='last_name']").val();
        var phone = $("[name='phone_number']").val();
        var email = $("[name='email']").val();
        var address_line_1 = $("[name='address_line_1']").val();
        var address_line_2 = $("[name='address_line_2']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var country = $("[name='country']").val();
        var pincode = $("[name='pincode']").val();
        var fname = $("[name='first_name']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();
        if (fname == "" || last_name == "" || phone == "" || email == "" || address_line_1 == "" || address_line_2 == "" || city == "" || state == "" || country == "" || pincode == "") {
            Swal.fire(
                'Alert!',
                'All fields are mandatory',
                'error'
              )
            return false
        } else {
            console.log(fname, phone)
            $.ajax({
                method: "GET",
                url: "/orders/proceed-to-pay",
                success: function (response) {
                    console.log('haidhfsdfhsadkfhkjasdhfkahsdf')
                    var options = {
                        "key": "rzp_test_tFIIQR8i8NPXJ4",
                        "amount": 1 * 100,
                        // response.total_price,
                        "currency": "INR",
                        "name": "Khadimode Corp",
                        "description": "Thank you for buying with us",
                        "image": "https://example.com/your_logo",
                        "handler": function (response_) {
                            // alert(response_.razorpay_payment_id);
                            data = {
                                'first_name': fname,
                                "last_name": last_name,
                                "phone_number": phone,
                                "email": email,
                                "address_line_1": address_line_1,
                                "address_line_2": address_line_2,
                                "city": city,
                                "state": state,
                                "country": country,
                                "pincode": pincode,
                                "fname": fname,
                                "payment_mode": "paid by razorpay",
                                "payment_id": response_.razorpay_payment_id,
                                csrfmiddlewaretoken: token
                            }
                            $.ajax({
                                method: "POST",
                                url: "/orders/place-order",
                                data: data,
                                // dataType: "dataType",
                                success: function (responsec) {
                                    Swal.fire(
                                        'Congratulations!',
                                        'Thank you to buying from us',
                                        'success'
                                      )
                                      setTimeout(()=>{
                                            window.location.href = '/orders/my-order';
                                      }, 3000)
                                }
                            });
                        },
                        "prefill": {
                            "name": fname + " " + last_name,
                            "email": email,
                            "contact": phone
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                    console.log('peipehdfsdhfhsdfkhskdfh')
                }
            });

        }
    });
});