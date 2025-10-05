export function About() {
  return (
    <section className="py-32 bg-card">
      <div className="container px-4">
        <div className="max-w-4xl mx-auto text-center space-y-10">
          <div className="space-y-4">
            <p className="text-sm uppercase tracking-[0.3em] text-accent font-medium">The Story</p>
            <h2
              className="text-5xl md:text-6xl lg:text-7xl font-serif font-bold text-primary text-balance leading-tight"
              style={{ fontFamily: "var(--font-playfair)" }}
            >
              Nature's Golden Nectar
            </h2>
          </div>

          {/* Description */}
          <div className="space-y-6 max-w-3xl mx-auto">
            <p className="text-lg md:text-xl text-foreground leading-relaxed text-pretty">
              Karupatti is a traditional South Indian sweetener crafted from the sap of palm trees. For centuries, this
              unrefined treasure has been celebrated for its rich, complex flavor and remarkable health benefits.
            </p>
            <p className="text-lg md:text-xl text-muted-foreground leading-relaxed text-pretty">
              Unlike refined sugar, karupatti retains all its natural minerals, vitamins, and antioxidants, making it a
              wholesome choice for conscious living. Each block tells a story of sustainable harvesting, traditional
              craftsmanship, and the timeless wisdom of our ancestors who understood the healing power of nature's
              gifts.
            </p>
          </div>

          {/* Decorative divider */}
          <div className="pt-8">
            <div className="w-24 h-px bg-accent mx-auto"></div>
          </div>
        </div>
      </div>
    </section>
  )
}
