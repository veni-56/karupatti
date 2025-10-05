import { Hero } from "@/components/hero"
import { About } from "@/components/about"
import { Benefits } from "@/components/benefits"
import { Process } from "@/components/process"
import { Products } from "@/components/products"
import { Newsletter } from "@/components/newsletter"
import { Footer } from "@/components/footer"

export default function Home() {
  return (
    <main className="min-h-screen">
      <Hero />
      <About />
      <Benefits />
      <Process />
      <Products />
      <Newsletter />
      <Footer />
    </main>
  )
}
