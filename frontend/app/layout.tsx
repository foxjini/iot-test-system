import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "IoT 테스트 시스템",
  description: "라즈베리파이 5 팀용 범용 센서/액추에이터 테스트 대시보드",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>
        <div className="min-h-screen">
          <header className="border-b border-line">
            <div className="mx-auto flex max-w-6xl items-center px-4 py-3 sm:px-6">
              <Link href="/" className="flex items-center gap-2 text-sm font-semibold tracking-tight">
                <span className="h-2 w-2 rounded-full bg-sensor" aria-hidden="true" />
                IoT 테스트 시스템
              </Link>
            </div>
          </header>
          <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6">{children}</div>
        </div>
      </body>
    </html>
  );
}
