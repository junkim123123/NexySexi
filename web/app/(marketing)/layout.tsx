import { MainHeader } from '@/components/site/main-header';
import { MainFooter } from '@/components/site/main-footer';

export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen flex-col">
      <MainHeader />
      <main className="flex-1">{children}</main>
      <MainFooter />
    </div>
  );
}

