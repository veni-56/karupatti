"use client"

import type React from "react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useState } from "react"

export function Newsletter() {
  const [email, setEmail] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Handle newsletter signup
    console.log("Newsletter signup:", email)
    setEmail("")
  }

  return (
    <section className="py-32 bg-primary text-primary-foreground">
      <div className="container px-4">
        <div className="max-w-3xl mx-auto text-center space-y-8">
          <div className="space-y-4">
            <p className="text-sm uppercase tracking-[0.3em] text-primary-foreground/70 font-medium">Newsletter</p>
            <h2
              className="text-4xl md:text-5xl lg:text-6xl font-serif font-bold text-balance"
              style={{ fontFamily: "var(--font-playfair)" }}
            >
              Join Our Sweet Community
            </h2>
          </div>
          <p className="text-lg md:text-xl text-primary-foreground/80 text-pretty leading-relaxed max-w-2xl mx-auto">
            Subscribe to receive exclusive recipes, health tips, and special offers on our premium karupatti products.
          </p>

          <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto pt-6">
            <Input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="flex-1 bg-primary-foreground text-foreground border-0 h-12 rounded-full px-6"
            />
            <Button
              type="submit"
              size="lg"
              className="bg-accent hover:bg-accent/90 text-accent-foreground h-12 px-8 rounded-full"
            >
              Subscribe
            </Button>
          </form>

          <p className="text-sm text-primary-foreground/60">We respect your privacy. Unsubscribe at any time.</p>
        </div>
      </div>
    </section>
  )
}
