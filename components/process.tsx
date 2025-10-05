export function Process() {
  const steps = [
    {
      number: "01",
      title: "Tapping",
      description:
        "Skilled tappers carefully extract fresh sap from palm trees at dawn, when the sap is sweetest and most abundant.",
    },
    {
      number: "02",
      title: "Collection",
      description:
        "The precious sap is collected in earthen pots, preserving its natural properties and purity throughout the day.",
    },
    {
      number: "03",
      title: "Boiling",
      description:
        "The sap is slowly boiled in large vessels over wood fire, concentrating its natural sweetness and rich flavor.",
    },
    {
      number: "04",
      title: "Molding",
      description:
        "The thickened syrup is poured into traditional molds and allowed to cool, forming solid blocks of karupatti.",
    },
  ]

  return (
    <section className="py-32 bg-secondary/30">
      <div className="container px-4">
        <div className="max-w-6xl mx-auto">
          {/* Section header */}
          <div className="text-center space-y-4 mb-20">
            <p className="text-sm uppercase tracking-[0.3em] text-accent font-medium">Our Process</p>
            <h2
              className="text-5xl md:text-6xl font-serif font-bold text-primary text-balance"
              style={{ fontFamily: "var(--font-playfair)" }}
            >
              From Tree to Table
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-pretty leading-relaxed">
              Every block of karupatti is crafted through a time-honored process that has been perfected over
              generations.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-x-12 gap-y-12 mb-20">
            {steps.map((step, index) => (
              <div key={index} className="flex gap-6">
                <div className="flex-shrink-0">
                  <div className="w-14 h-14 rounded-full bg-accent text-accent-foreground flex items-center justify-center text-lg font-bold">
                    {step.number}
                  </div>
                </div>
                <div className="space-y-3 pt-1">
                  <h3 className="text-2xl font-bold text-foreground">{step.title}</h3>
                  <p className="text-muted-foreground leading-relaxed">{step.description}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Process image */}
          <div className="rounded-xl overflow-hidden shadow-2xl">
            <img
              src="/traditional-palm-sap-collection-and-karupatti-maki.jpg"
              alt="Karupatti making process"
              className="w-full h-auto object-cover"
            />
          </div>
        </div>
      </div>
    </section>
  )
}
