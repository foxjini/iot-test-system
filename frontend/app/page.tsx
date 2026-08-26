"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, type Device } from "@/lib/api";
import { DeviceStatusBadge } from "@/components/DeviceStatusBadge";

function relativeTime(iso: string | null): string {
  if (!iso) return "통신 기록 없음";
  const sec = Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 1000));
  if (sec < 60) return `${sec}초 전`;
  if (sec < 3600) return `${Math.floor(sec / 60)}분 전`;
  return `${Math.floor(sec / 3600)}시간 전`;
}

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
        <h1 className="text-2xl font-semibold tracking-tight text-ink-primary">디바이스</h1>
        <p className="mt-1 text-sm text-ink-secondary">
          라즈베리파이 5 대신 Mock 프로그램(또는 실제 Pi)이 연결할 팀별 디바이스를 등록하고 관리합니다.
        </p>
      </header>

      {error && (
        <p className="rounded-md border border-status-critical/30 bg-status-critical/10 px-3 py-2 text-sm text-status-critical">
          백엔드에 연결할 수 없습니다: {error}
        </p>
      )}

      <section>
        {loading ? (
          <p className="text-sm text-ink-muted">불러오는 중...</p>
        ) : devices.length === 0 ? (
          <p className="rounded-md border border-dashed border-line px-4 py-6 text-center text-sm text-ink-muted">
            아직 등록된 디바이스가 없습니다. 아래에서 첫 팀을 등록하세요.
          </p>
        ) : (
          <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {devices.map((d) => (
              <li key={d.id}>
                <Link
                  href={`/devices/${d.id}`}
                  className="block rounded-md border border-line bg-surface p-4 transition-colors hover:border-white/25"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-medium text-ink-primary">{d.team_name}</span>
                    <DeviceStatusBadge online={d.is_online} />
                  </div>
                  <p className="mt-2 text-xs text-ink-muted">
                    device_id {d.id} · {relativeTime(d.last_seen_at)}
                  </p>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="rounded-md border border-line bg-surface p-4">
        <h2 className="text-xs font-medium uppercase tracking-wide text-ink-muted">새 디바이스(팀) 등록</h2>
        <form onSubmit={handleCreate} className="mt-3 flex gap-2">
          <input
            className="flex-1 rounded-md border border-line bg-bg px-3 py-2 text-sm text-ink-primary placeholder:text-ink-muted"
            placeholder="팀 이름 (예: 1팀)"
            value={teamName}
            onChange={(e) => setTeamName(e.target.value)}
          />
          <button
            type="submit"
            className="rounded-md bg-sensor px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-sensor-soft"
          >
            등록
          </button>
        </form>
        {createdKey && (
          <p className="mt-3 rounded-md border border-status-warning/30 bg-status-warning/10 px-3 py-2 text-sm text-ink-primary">
            디바이스 #{createdKey.id} 등록 완료 — API Key:{" "}
            <code className="font-mono text-status-warning">{createdKey.api_key}</code>
            <br />
            <span className="text-ink-secondary">
              이 값을 mock_pi/.env의 DEVICE_ID={createdKey.id}, API_KEY에 입력하세요.
            </span>
          </p>
        )}
      </section>
    </main>
  );
}
