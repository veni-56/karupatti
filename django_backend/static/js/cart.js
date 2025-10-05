document.addEventListener("click", async (e) => {
  const btn = e.target.closest('form[action*="/cart/add/"] button')
  if (!btn) return
  const form = btn.closest("form")
  if (!form) return
  e.preventDefault()
  const action = form.getAttribute("action")
  const formData = new FormData(form)
  try {
    const res = await fetch(action, {
      method: "POST",
      headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": formData.get("csrfmiddlewaretoken") },
      body: formData,
    })
    const data = await res.json()
    if (data.ok) {
      // Optionally, update a cart badge here
      // console.log("[v0] Cart count:", data.count);
      btn.textContent = "Added!"
      setTimeout(() => (btn.textContent = "Add to cart"), 1200)
    } else {
      window.location.href = action // fallback full POST
    }
  } catch {
    window.location.href = action // fallback
  }
})
