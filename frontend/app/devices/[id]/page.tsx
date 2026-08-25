"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { api, type CatalogComponent, type Component, type Device } from "@/lib/api";
import { DeviceStatusBadge } from "@/components/DeviceStatusBadge";
import { ConfigSection } from "@/components/ConfigSection";
import { SensorCard } from "@/components/SensorCard";
import { ActuatorControl } from "@/components/ActuatorControl";

export default function DeviceDetailPage() {
  const params = useParams<{ id: string }>();
  const deviceId = Number(params.id);

  const [device, setDevice] = useState<Device | null>(null);
  const [components, setComponents] = useState<Component[]>([]);
  const [catalog, setCatalog] = useState<CatalogComponent[]>([]);
  const [error, setError] = useState<string | null>(null);

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

  if (!device) {
    return <p className="text-sm text-gray-500">{error ?? "불러오는 중..."}</p>;
  }

  const sensors = components.filter((c) => c.category === "sensor");
  const actuators = components.filter((c) => c.category === "actuator");

  return (
    <main className="space-y-8">
      <div>
        <Link href="/" className="text-sm text-gray-500 hover:underline">
          ← 디바이스 목록
        </Link>
        <div className="mt-1 flex items-center justify-between">
          <h1 className="text-2xl font-bold">{device.team_name}</h1>
          <DeviceStatusBadge online={device.is_online} />
        </div>
        <p className="mt-1 text-xs text-gray-500">
          device_id: {device.id} · API Key: <code className="font-mono">{device.api_key}</code>
        </p>
      </div>

      {error && <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">연결 오류: {error}</p>}

      <ConfigSection catalog={catalog} components={components} onAdd={addComponent} onRemove={removeComponent} />

      <section className="space-y-4">
        <h2 className="font-semibold">센서 모니터링</h2>
        {sensors.length === 0 ? (
          <p className="text-sm text-gray-500">등록된 센서가 없습니다. 위 구성 관리에서 추가하세요.</p>
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
        <h2 className="font-semibold">액추에이터 제어</h2>
        {actuators.length === 0 ? (
          <p className="text-sm text-gray-500">등록된 액추에이터가 없습니다. 위 구성 관리에서 추가하세요.</p>
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
    </main>
  );
}
