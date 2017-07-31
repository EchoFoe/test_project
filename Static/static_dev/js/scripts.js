$(document).ready(function () {
  var form=$('#form_buying_product');
  console.log(form);
  
  function basketUpdating (product_id, nmb, is_delete) {
      var data = {};
      data.product_id = product_id;
      data.nmb = nmb;
      var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
      data ["csrfmiddlewaretoken"] = csrf_token;

      if (is_delete){
          data["is_delete"] = true;

      }

      var url = form.attr("action");

      console.log(data);
      $.ajax({
          url: url,
          type: 'POST',
          data: data,
          cache: true,
          success: function (data) {
              console.log("OK");
              console.log(data.products_total_nmb);

              if (data.products_total_nmb || data.products_total_nmb == 0) {
                  $('#basket_total_nmb').text("(" + data.products_total_nmb + ")");
                  console.log(data.products);
                  $('.basket-items ul').html("");
                  $.each(data.products, function (k, v) {
                      $('.basket-items ul').append('<li>' + v.name + ', ' + v.nmb + ' шт. ' + 'по ' + v.price_per_item + 'руб  ' +
                          '<a class="delete-item" href="" data-product_id="'+v.id+'"> ' +
                          '<span class="glyphicon glyphicon-remove" aria-hidden="true"></span> ' +
                          '</a>'+
                          '</li>');
                  })
              }
          },
          error: function () {
              console.log("Error")
          }
      });

  };

  
  form.on('submit', function (e) {
      e.preventDefault();
      console.log('123');
      var nmb = $('#number').val();
      console.log(nmb);
      var submit_btn = $('#submit_btn');
      var product_id = submit_btn.data("product.id");
      var product_name = submit_btn.data("product.name");
      var product_price = submit_btn.data("product.price");
      console.log(product_id);
      console.log(product_name);
      basketUpdating(product_id, nmb, is_delete=false)

      });


// (function(){
//
//   $("#cart").on("click", function() {
//     $(".shopping-cart").fadeToggle( "fast");
//   });
//
// })();

  function showingBasket() {
      $('.basket-items').removeClass('hidden');
  };

      $('.basket-container').on('click', function (e) {
        e.preventDefault();
        showingBasket();
      });

      $('.basket-container').mouseover(function () {
        showingBasket();
      });

      // $('.basket-container').mouseout(function () {
      //   showingBasket();
      // });

      $(document).on('click', '.delete-item', function (e) {
          e.preventDefault();
          product_id = $(this).data("product_id");
          nmb = 0;
          basketUpdating(product_id, nmb, is_delete=true)
      });

      function calculatingBasketAmount(){
          // console.log("calculatingBasketAmount");
          var total_order_amount = 0;
        $('.total-product-in-basket-amount').each(function () {
            console.log(parseFloat($(this).text()));
            total_order_amount = total_order_amount + parseFloat($(this).text());
        });
        console.log(total_order_amount);
        $('#total_order_amount').text(total_order_amount.toFixed(2));
    };
      $(document).on('change', ".product-in-basket-nmb", function () {
         var current_nmb = $(this).val();
         console.log(current_nmb);
         var current_tr = $(this).closest('tr');
         var current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2);
         var total_amount = parseFloat(current_nmb*current_price).toFixed(2);
         current_tr.find('.total-product-in-basket-amount').text(total_amount);
         calculatingBasketAmount();
      });
      // console.log("123");
      calculatingBasketAmount();



});

$(function () {
/* set variables locally for increased performance */
var scroll_timer;
var displayed = false;
var $message = $('#message a');
var $window = $(window);
var top = $(document.body).children(0).position().top;
/* react to scroll event on window */
$window.scroll(function () {
window.clearTimeout(scroll_timer);
scroll_timer = window.setTimeout(function () {
if($window.scrollTop() <= top)
{
displayed = false;
$message.fadeOut(500);
}
else if(displayed == false)
{
displayed = true;
$message.stop(true, true).show().click(function () { $message.fadeOut(500); });
}
}, 100);
});
});

function myFunction() {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}