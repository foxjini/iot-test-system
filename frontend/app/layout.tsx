import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "IoT 테스트 시스템",
  description: "라즈베리파이 5 팀용 범용 센서/액추에이터 테스트 대시보드",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>
        <div className="mx-auto max-w-5xl px-4 py-6">{children}</div>
      </body>
    </html>
  );
}
