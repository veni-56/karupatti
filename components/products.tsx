import { Button } from "@/components/ui/button"
import { ShoppingCart } from "lucide-react"

const products = [
  {
    name: "Classic Blocks",
    weight: "500g",
    price: "₹250",
    image: "/karupatti-palm-jaggery-blocks-in-traditional-packa.jpg",
    description: "Traditional solid blocks, perfect for cooking and beverages",
  },
  {
    name: "Powder Form",
    weight: "500g",
    price: "₹280",
    image: "/karupatti-palm-jaggery-powder-in-glass-jar.jpg",
    description: "Finely ground powder for easy mixing and baking",
  },
  {
    name: "Premium Gift Box",
    weight: "1kg",
    price: "₹550",
    image: "/premium-karupatti-gift-box-with-elegant-packaging.jpg",
    description: "Beautifully packaged gift set with assorted forms",
  },
]

export function Products() {
  return (
    <section className="py-32 bg-background">
      <div className="container px-4">
        <div className="max-w-6xl mx-auto">
          {/* Section header */}
          <div className="text-center space-y-4 mb-20">
            <p className="text-sm uppercase tracking-[0.3em] text-accent font-medium">Our Products</p>
            <h2
              className="text-5xl md:text-6xl font-serif font-bold text-primary text-balance"
              style={{ fontFamily: "var(--font-playfair)" }}
            >
              Choose Your Sweetness
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-10">
            {products.map((product, index) => (
              <div key={index} className="group space-y-6">
                <div className="aspect-square overflow-hidden rounded-lg bg-card">
                  <img
                    src={product.image || "/placeholder.svg"}
                    alt={product.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                </div>
                <div className="space-y-3">
                  <div className="flex justify-between items-start">
                    <h3 className="text-2xl font-bold text-foreground">{product.name}</h3>
                    <span className="text-sm text-muted-foreground font-medium">{product.weight}</span>
                  </div>
                  <p className="text-muted-foreground leading-relaxed">{product.description}</p>
                  <div className="flex items-center justify-between pt-2">
                    <p className="text-3xl font-bold text-accent">{product.price}</p>
                    <Button size="sm" className="bg-primary hover:bg-primary/90 text-primary-foreground rounded-full">
                      <ShoppingCart className="mr-2 h-4 w-4" />
                      Add
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
