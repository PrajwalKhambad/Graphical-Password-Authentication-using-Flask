// $("bt").click(function() {
//     var fired_button = $(this).val();
//     document.getElementById("value").value+=fired_button;
// });

const buttons = document.querySelectorAll('.bt');
val=document.getElementById("value")
buttons.forEach((button) => {
  button.addEventListener('click', () => {
    const value = button.value;
    console.log(value);
    // val.value=value;
    val.value+=value;
  });
});
