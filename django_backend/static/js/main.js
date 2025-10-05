;(() => {
  // Update year
  var y = document.getElementById("year")
  if (y) {
    y.textContent = new Date().getFullYear()
  }

  // Minimal "add to cart" demo interaction
  document.addEventListener("click", (e) => {
    var btn = e.target.closest(".add-to-cart")
    if (!btn) return
    var id = btn.getAttribute("data-id")
    console.log("[v0] add_to_cart_clicked:", id)
    btn.textContent = "Added!"
    btn.disabled = true
    setTimeout(() => {
      btn.textContent = "Add to cart"
      btn.disabled = false
    }, 1200)
  })
})()
