"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, type Device } from "@/lib/api";
import { DeviceStatusBadge } from "@/components/DeviceStatusBadge";

export default function HomePage() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [teamName, setTeamName] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [createdKey, setCreatedKey] = useState<{ id: number; api_key: string } | null>(null);

  async function refresh() {
    try {
      setDevices(await api.listDevices());
      setError(null);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
    const timer = setInterval(refresh, 3000);
    return () => clearInterval(timer);
  }, []);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!teamName.trim()) return;
    const device = await api.createDevice(teamName.trim());
    setTeamName("");
    setCreatedKey({ id: device.id, api_key: device.api_key });
    refresh();
  }

  return (
    <main className="space-y-8">
      <header>
        <h1 className="text-2xl font-bold">IoT 테스트 시스템</h1>
        <p className="mt-1 text-sm text-gray-500">
          라즈베리파이 5 대신 Mock 프로그램(또는 실제 Pi)이 연결할 디바이스를 팀별로 등록하고
          관리합니다.
        </p>
      </header>

      {error && (
        <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">
          백엔드에 연결할 수 없습니다: {error}
        </p>
      )}

      <section className="rounded-lg border border-gray-200 bg-white p-5">
        <h2 className="font-semibold">새 디바이스(팀) 등록</h2>
        <form onSubmit={handleCreate} className="mt-3 flex gap-2">
          <input
            className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm"
            placeholder="팀 이름 (예: 1팀)"
            value={teamName}
            onChange={(e) => setTeamName(e.target.value)}
          />
          <button
            type="submit"
            className="rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-700"
          >
            등록
          </button>
        </form>
        {createdKey && (
          <p className="mt-3 rounded-md bg-amber-50 px-3 py-2 text-sm text-amber-800">
            디바이스 #{createdKey.id} 등록 완료 — API Key:{" "}
            <code className="font-mono">{createdKey.api_key}</code>
            <br />이 값을 mock_pi/.env의 DEVICE_ID={createdKey.id}, API_KEY에 입력하세요.
          </p>
        )}
      </section>

      <section>
        <h2 className="mb-3 font-semibold">등록된 디바이스</h2>
        {loading ? (
          <p className="text-sm text-gray-500">불러오는 중...</p>
        ) : devices.length === 0 ? (
          <p className="text-sm text-gray-500">아직 등록된 디바이스가 없습니다.</p>
        ) : (
          <ul className="grid gap-3 sm:grid-cols-2">
            {devices.map((d) => (
              <li key={d.id}>
                <Link
                  href={`/devices/${d.id}`}
                  className="block rounded-lg border border-gray-200 bg-white p-4 hover:border-gray-400"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium">{d.team_name}</span>
                    <DeviceStatusBadge online={d.is_online} />
                  </div>
                  <p className="mt-1 text-xs text-gray-500">device_id: {d.id}</p>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
