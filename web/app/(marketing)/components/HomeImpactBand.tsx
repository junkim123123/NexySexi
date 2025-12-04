export default function HomeImpactBand() {
  return (
    <section className="py-12 sm:py-16 md:py-20 bg-neutral-900 text-white">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8 lg:gap-12">
          {/* Left Card */}
          <div className="rounded-3xl bg-neutral-800 p-6 sm:p-8">
            <h2 className="text-3xl font-bold">
              Do good trade while you grow
            </h2>
            <p className="mt-4 text-base text-neutral-300 leading-relaxed">
              NexSupply was started to make cross-border trade fairer and more transparent for both importers and factories.
            </p>
          </div>

          {/* Right Card */}
          <div className="rounded-3xl bg-neutral-800 p-6 sm:p-8">
            <h2 className="text-3xl font-bold">
              Over 25 projects supported
            </h2>
            <p className="mt-4 text-base text-neutral-300 leading-relaxed">
              Even in alpha, NexSupply has helped projects understand landed cost, lead times, and compliance risks before buying.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}