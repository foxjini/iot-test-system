"use client";

import { useEffect, useState } from "react";
import { api, type CatalogComponent, type Component, type Reading } from "@/lib/api";
import { Sparkline, StateDots } from "@/components/Sparkline";

type CatalogField = CatalogComponent["fields"][number];

function formatValue(value: unknown, field: CatalogField): string {
  if (value === undefined || value === null) return "-";
  if (field.type === "bool") return value ? "예" : "아니오";
  if (field.type === "color" && Array.isArray(value)) return `rgb(${value.join(", ")})`;
  return String(value);
}

function relativeTime(iso: string): string {
  const sec = Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 1000));
  if (sec < 60) return `${sec}초 전`;
  if (sec < 3600) return `${Math.floor(sec / 60)}분 전`;
  return `${Math.floor(sec / 3600)}시간 전`;
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
        const rows = await api.listReadings(deviceId, component.id, 12);
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
  const secondaryFields = catalogType.fields.slice(1);
  const isNumericPrimary = primaryField?.type === "float" || primaryField?.type === "int";

  const numericTrend = isNumericPrimary
    ? history
        .map((r) => Number(r.value[primaryField.key]))
        .filter((v) => Number.isFinite(v))
    : [];
  const boolTrend =
    primaryField?.type === "bool" ? history.map((r) => Boolean(r.value[primaryField.key])) : [];

  return (
    <div className="rounded-md border-y border-r border-line border-l-2 border-l-sensor bg-surface p-4">
      <div className="flex items-start justify-between gap-2">
        <span className="text-sm font-medium text-ink-primary">{component.label}</span>
        <span className="shrink-0 text-xs text-ink-muted">{catalogType.label_ko}</span>
      </div>

      {latest && primaryField ? (
        <>
          <div className="mt-3 flex items-end justify-between gap-3">
            <div className="flex items-baseline gap-1">
              <span className="text-3xl font-semibold tabular-nums text-ink-primary">
                {formatValue(latest.value[primaryField.key], primaryField)}
              </span>
              {primaryField.unit && <span className="text-base text-ink-secondary">{primaryField.unit}</span>}
            </div>
            <div className="text-sensor">
              {isNumericPrimary && numericTrend.length > 1 && <Sparkline values={numericTrend} />}
              {boolTrend.length > 0 && <StateDots values={boolTrend} />}
            </div>
          </div>

          {secondaryFields.length > 0 && (
            <dl className="mt-3 space-y-1 border-t border-line pt-2">
              {secondaryFields.map((f) => (
                <div key={f.key} className="flex justify-between text-xs">
                  <dt className="text-ink-secondary">{f.label_ko}</dt>
                  <dd className="tabular-nums text-ink-primary">{formatValue(latest.value[f.key], f)}</dd>
                </div>
              ))}
            </dl>
          )}

          <p className="mt-3 text-xs text-ink-muted">{relativeTime(latest.recorded_at)} 갱신</p>
        </>
      ) : (
        <p className="mt-4 text-sm text-ink-muted">아직 수신된 값이 없습니다.</p>
      )}
    </div>
  );
}
