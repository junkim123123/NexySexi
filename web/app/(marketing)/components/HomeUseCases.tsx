const useCases = [
  {
    title: 'Launch a new FBA brand',
    body: 'You have a new product idea and need to check landed-cost and risk before committing to a large order.',
  },
  {
    title: 'Re-source an existing SKU',
    body: 'Your current supplier is too expensive or risky, and you want to find qualified alternatives.',
  },
  {
    title: 'Test a higher-risk category',
    body: 'Compliance, duties, or AD/CVD risk needs to be checked by an expert before you import.',
  },
];

export default function HomeUseCases() {
  return (
    <section id="home-use-cases" className="py-12 sm:py-16 md:py-20 bg-white">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-6 sm:gap-8 md:grid-cols-3">
          {useCases.map((useCase) => (
            <div
              key={useCase.title}
              className="rounded-3xl bg-neutral-50 p-8 shadow-sm hover:shadow-lg transition-shadow duration-300"
            >
              <h3 className="text-xl font-semibold text-neutral-900">
                {useCase.title}
              </h3>
              <p className="mt-3 text-base text-neutral-600">
                {useCase.body}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}