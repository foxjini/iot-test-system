"use client";

import { useEffect, useState } from "react";
import { api, type CatalogComponent, type Component, type Reading } from "@/lib/api";

function formatValue(value: unknown, field: CatalogComponent["fields"][number]): string {
  if (value === undefined) return "-";
  if (field.type === "bool") return value ? "예" : "아니오";
  if (field.type === "color" && Array.isArray(value)) return `rgb(${value.join(", ")})`;
  if (typeof value === "number") return field.unit ? `${value}${field.unit}` : `${value}`;
  return String(value);
}

export function SensorCard({
  deviceId,
  component,
  catalogType,
}: {
  deviceId: number;
  component: Component;
  catalogType: CatalogComponent;
}) {
  const [history, setHistory] = useState<Reading[]>([]);

  useEffect(() => {
    let cancelled = false;
    async function poll() {
      try {
        const rows = await api.listReadings(deviceId, component.id, 8);
        if (!cancelled) setHistory(rows);
      } catch {
        // 폴링 중 일시 오류는 다음 주기에 재시도하므로 무시
      }
    }
    poll();
    const timer = setInterval(poll, 2000);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [deviceId, component.id]);

  const latest = history.length ? history[history.length - 1] : null;
  const primaryField = catalogType.fields[0];

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4">
      <div className="flex items-center justify-between">
        <span className="font-medium">{component.label}</span>
        <span className="text-xs text-gray-400">{catalogType.label_ko}</span>
      </div>

      {latest ? (
        <dl className="mt-3 space-y-1">
          {catalogType.fields.map((f) => (
            <div key={f.key} className="flex justify-between text-sm">
              <dt className="text-gray-500">{f.label_ko}</dt>
              <dd className="font-mono">{formatValue(latest.value[f.key], f)}</dd>
            </div>
          ))}
        </dl>
      ) : (
        <p className="mt-3 text-sm text-gray-400">아직 수신된 값이 없습니다.</p>
      )}

      {history.length > 1 && primaryField && (
        <p className="mt-3 truncate text-xs text-gray-400">
          최근 {primaryField.label_ko}:{" "}
          {history.map((r) => String(r.value[primaryField.key] ?? "-")).join(", ")}
        </p>
      )}
    </div>
  );
}
