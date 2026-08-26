"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { api, type CatalogComponent, type Component, type Device } from "@/lib/api";
import { DeviceStatusBadge } from "@/components/DeviceStatusBadge";
import { ConfigSection } from "@/components/ConfigSection";
import { SensorCard } from "@/components/SensorCard";
import { ActuatorControl } from "@/components/ActuatorControl";

function SectionLabel({ children }: { children: React.ReactNode }) {
  return <h2 className="text-xs font-medium uppercase tracking-wide text-ink-muted">{children}</h2>;
}

export default function DeviceDetailPage() {
  const params = useParams<{ id: string }>();
  const deviceId = Number(params.id);

  const [device, setDevice] = useState<Device | null>(null);
  const [components, setComponents] = useState<Component[]>([]);
  const [catalog, setCatalog] = useState<CatalogComponent[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const refresh = useCallback(async () => {
    try {
      const [d, comps] = await Promise.all([api.getDevice(deviceId), api.listComponents(deviceId)]);
      setDevice(d);
      setComponents(comps);
      setError(null);
    } catch (e) {
      setError((e as Error).message);
    }
  }, [deviceId]);

  useEffect(() => {
    api.listCatalog().then(setCatalog);
  }, []);

  useEffect(() => {
    refresh();
    const timer = setInterval(refresh, 2000);
    return () => clearInterval(timer);
  }, [refresh]);

  async function addComponent(typeKey: string, label: string) {
    await api.createComponent(deviceId, typeKey, label);
    refresh();
  }

  async function removeComponent(componentId: number) {
    await api.deleteComponent(deviceId, componentId);
    refresh();
  }

  async function copyApiKey() {
    if (!device) return;
    await navigator.clipboard.writeText(device.api_key);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  if (!device) {
    return <p className="text-sm text-ink-muted">{error ?? "불러오는 중..."}</p>;
  }

  const sensors = components.filter((c) => c.category === "sensor");
  const actuators = components.filter((c) => c.category === "actuator");

  return (
    <main className="space-y-10">
      <div>
        <Link href="/" className="text-sm text-ink-muted hover:text-ink-secondary">
          ← 디바이스 목록
        </Link>
        <div className="mt-2 flex items-center justify-between gap-2">
          <h1 className="text-2xl font-semibold tracking-tight text-ink-primary">{device.team_name}</h1>
          <DeviceStatusBadge online={device.is_online} />
        </div>
        <p className="mt-2 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-ink-muted">
          <span>device_id {device.id}</span>
          <span aria-hidden="true">·</span>
          <span>
            API Key <code className="font-mono text-ink-secondary">{device.api_key}</code>
          </span>
          <button
            onClick={copyApiKey}
            className="rounded border border-line px-1.5 py-0.5 text-ink-secondary transition-colors hover:border-white/25 hover:text-ink-primary"
          >
            {copied ? "복사됨" : "복사"}
          </button>
        </p>
      </div>

      {error && (
        <p className="rounded-md border border-status-critical/30 bg-status-critical/10 px-3 py-2 text-sm text-status-critical">
          연결 오류: {error}
        </p>
      )}

      <section className="space-y-4">
        <SectionLabel>센서 모니터링</SectionLabel>
        {sensors.length === 0 ? (
          <p className="rounded-md border border-dashed border-line px-4 py-6 text-center text-sm text-ink-muted">
            등록된 센서가 없습니다. 아래 구성 관리에서 추가하세요.
          </p>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {sensors.map((c) => {
              const ctype = catalog.find((x) => x.type_key === c.type_key);
              return ctype ? <SensorCard key={c.id} deviceId={deviceId} component={c} catalogType={ctype} /> : null;
            })}
          </div>
        )}
      </section>

      <section className="space-y-4">
        <SectionLabel>액추에이터 제어</SectionLabel>
        {actuators.length === 0 ? (
          <p className="rounded-md border border-dashed border-line px-4 py-6 text-center text-sm text-ink-muted">
            등록된 액추에이터가 없습니다. 아래 구성 관리에서 추가하세요.
          </p>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {actuators.map((c) => {
              const ctype = catalog.find((x) => x.type_key === c.type_key);
              return ctype ? (
                <ActuatorControl key={c.id} deviceId={deviceId} component={c} catalogType={ctype} />
              ) : null;
            })}
          </div>
        )}
      </section>

      <ConfigSection catalog={catalog} components={components} onAdd={addComponent} onRemove={removeComponent} />
    </main>
  );
}
