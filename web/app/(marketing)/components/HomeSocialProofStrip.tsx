const quotes = [
  {
    quote: "Finally, a way to get landed-cost clarity without the back-and-forth.",
    author: "FBA Seller, CPG Category",
  },
  {
    quote: "The compliance check saved us from a potentially very expensive mistake.",
    author: "Retail Buyer, Hardlines",
  },
  {
    quote: "We used NexSupply to test a new snack product. The process was simple and fast.",
    author: "Brand Manager, Food & Beverage",
  },
];

export default function HomeSocialProofStrip() {
  return (
    <section className="py-16 sm:py-20 bg-neutral-50 border-y border-neutral-200">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-2xl font-semibold text-neutral-900 sm:text-3xl">
            See what importers are saying about NexSupply
          </h2>
          <div className="mt-8">
            <div className="inline-block rounded-xl bg-white p-6 shadow-md text-center">
              <p className="text-2xl font-bold text-neutral-900">4.8 / 5</p>
              <p className="mt-1 text-sm text-neutral-600">
                from early beta projects
              </p>
            </div>
            <p className="mt-4 text-base text-neutral-700 max-w-2xl mx-auto">
              Faster landed-cost clarity, fewer surprises at customs.
            </p>
          </div>
        </div>
        <div className="mt-12 grid grid-cols-1 gap-8 md:grid-cols-3">
          {quotes.map((item) => (
            <blockquote key={item.author} className="text-center">
              <p className="text-lg text-neutral-800">"{item.quote}"</p>
              <footer className="mt-4 text-sm text-neutral-600">
                — {item.author}
              </footer>
            </blockquote>
          ))}
        </div>
      </div>
    </section>
  );
}