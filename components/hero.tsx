import { Button } from "@/components/ui/button"
import { ArrowRight, ChevronDown } from "lucide-react"

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-background">
      <div className="container relative z-10 px-4 py-32 md:py-40">
        <div className="max-w-5xl mx-auto text-center space-y-10">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-5 py-2 rounded-full bg-accent/10 border border-accent/20">
            <span className="text-sm font-medium text-accent uppercase tracking-wide">Pure & Natural</span>
          </div>

          <h1
            className="text-6xl md:text-7xl lg:text-8xl font-serif font-bold tracking-tight text-balance leading-[0.95]"
            style={{ fontFamily: "var(--font-playfair)" }}
          >
            <span className="block text-foreground">KARUPATTI</span>
            <span className="block text-accent mt-4 italic">Palm Jaggery</span>
          </h1>

          {/* Subheading */}
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto text-pretty leading-relaxed">
            Ancient sweetness from the heart of palm trees. A traditional, unrefined treasure that nourishes body and
            soul.
          </p>

          {/* CTA buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-6">
            <Button
              size="lg"
              className="text-base px-10 py-6 bg-primary hover:bg-primary/90 text-primary-foreground rounded-full"
            >
              Explore Products
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="text-base px-10 py-6 border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground bg-transparent rounded-full transition-all"
            >
              Our Story
            </Button>
          </div>

          {/* Hero image */}
          <div className="pt-16">
            <div className="relative rounded-xl overflow-hidden shadow-2xl">
              <img
                src="/traditional-karupatti-palm-jaggery-blocks-on-rusti.jpg"
                alt="Karupatti palm jaggery blocks"
                className="w-full h-auto object-cover"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
        <ChevronDown className="w-6 h-6 text-muted-foreground" />
      </div>
    </section>
  )
}
