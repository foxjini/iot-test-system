"use client";

import { useEffect, useState } from "react";
import { api, type CatalogComponent, type Command, type Component } from "@/lib/api";
import { StatusChip } from "@/components/StatusChip";

type FieldValue = boolean | number | string | number[];
type CatalogField = CatalogComponent["fields"][number];

function defaultValueFor(field: CatalogField): FieldValue {
  if (field.type === "bool") return false;
  if (field.type === "color") return [0, 0, 0];
  if (field.type === "float" || field.type === "int") return field.min ?? 0;
  return field.options?.[0] ?? "";
}

function rgbToHex([r, g, b]: number[]): string {
  return `#${[r, g, b].map((v) => v.toString(16).padStart(2, "0")).join("")}`;
}

function hexToRgb(hex: string): number[] {
  const n = parseInt(hex.slice(1), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}

function formatState(state: Record<string, unknown>, fields: CatalogField[]): string {
  return fields
    .filter((f) => f.key in state)
    .map((f) => {
      const v = state[f.key];
      if (f.type === "bool") return `${f.label_ko} ${v ? "ON" : "OFF"}`;
      if (f.type === "color" && Array.isArray(v)) return `${f.label_ko} rgb(${v.join(",")})`;
      return `${f.label_ko} ${v}${f.unit ?? ""}`;
    })
    .join(" · ");
}

export function ActuatorControl({
  deviceId,
  component,
  catalogType,
}: {
  deviceId: number;
  component: Component;
  catalogType: CatalogComponent;
}) {
  const [values, setValues] = useState<Record<string, FieldValue>>(() =>
    Object.fromEntries(catalogType.fields.map((f) => [f.key, defaultValueFor(f)]))
  );
  const [lastCommand, setLastCommand] = useState<Command | null>(null);
  const [sending, setSending] = useState(false);

  useEffect(() => {
    let cancelled = false;
    async function poll() {
      try {
        const cmd = await api.latestCommand(deviceId, component.id);
        if (!cancelled && cmd) setLastCommand(cmd);
      } catch {
        // 무시하고 다음 주기 재시도
      }
    }
    poll();
    const timer = setInterval(poll, 2000);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [deviceId, component.id]);

  function updateField(key: string, value: FieldValue) {
    setValues((prev) => ({ ...prev, [key]: value }));
  }

  async function apply() {
    setSending(true);
    try {
      setLastCommand(await api.sendCommand(deviceId, component.id, values));
    } finally {
      setSending(false);
    }
  }

  const tone =
    lastCommand?.status === "acked" ? "good" : lastCommand?.status === "failed" ? "critical" : "warning";
  const label =
    lastCommand?.status === "acked" ? "실행 완료" : lastCommand?.status === "failed" ? "실패" : "대기 중";

  return (
    <div className="rounded-md border-y border-r border-line border-l-2 border-l-actuator bg-surface p-4">
      <div className="flex items-start justify-between gap-2">
        <span className="text-sm font-medium text-ink-primary">{component.label}</span>
        <span className="shrink-0 text-xs text-ink-muted">{catalogType.label_ko}</span>
      </div>

      {lastCommand && (
        <div className="mt-2 flex items-center gap-2">
          <StatusChip tone={tone} label={label} />
          {lastCommand.actual_state && (
            <span className="truncate text-xs text-ink-secondary">
              현재: {formatState(lastCommand.actual_state, catalogType.fields)}
            </span>
          )}
        </div>
      )}

      <div className="mt-4 space-y-3">
        {catalogType.fields.map((f) => (
          <FieldControl key={f.key} field={f} value={values[f.key]} onChange={(v) => updateField(f.key, v)} />
        ))}
      </div>

      <button
        onClick={apply}
        disabled={sending}
        className="mt-4 w-full rounded-md bg-actuator px-3 py-2 text-sm font-medium text-white transition-colors hover:bg-actuator-soft disabled:opacity-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white/60"
      >
        {sending ? "적용 중..." : "적용"}
      </button>
    </div>
  );
}

function Switch({ checked, onChange }: { checked: boolean; onChange: (v: boolean) => void }) {
  return (
    <label className="relative inline-flex h-6 w-11 shrink-0 cursor-pointer items-center">
      <input
        type="checkbox"
        className="peer sr-only"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
      />
      <span className="absolute inset-0 rounded-full bg-white/15 transition-colors peer-checked:bg-actuator" />
      <span className="absolute left-0.5 h-5 w-5 rounded-full bg-white transition-transform peer-checked:translate-x-5" />
      <span className="absolute inset-0 rounded-full ring-white/60 peer-focus-visible:ring-2" />
    </label>
  );
}

function FieldControl({
  field,
  value,
  onChange,
}: {
  field: CatalogField;
  value: FieldValue;
  onChange: (v: FieldValue) => void;
}) {
  if (field.type === "bool") {
    return (
      <div className="flex items-center justify-between text-sm">
        <span className="text-ink-secondary">{field.label_ko}</span>
        <Switch checked={Boolean(value)} onChange={onChange} />
      </div>
    );
  }

  if (field.type === "color") {
    const rgb = Array.isArray(value) ? value : [0, 0, 0];
    return (
      <div className="flex items-center justify-between text-sm">
        <span className="text-ink-secondary">{field.label_ko}</span>
        <div className="flex items-center gap-2">
          <span className="font-mono text-xs text-ink-muted">{rgbToHex(rgb)}</span>
          <input type="color" value={rgbToHex(rgb)} onChange={(e) => onChange(hexToRgb(e.target.value))} />
        </div>
      </div>
    );
  }

  if (field.type === "string" && field.options?.length) {
    return (
      <label className="flex items-center justify-between text-sm">
        <span className="text-ink-secondary">{field.label_ko}</span>
        <select
          value={String(value)}
          onChange={(e) => onChange(e.target.value)}
          className="rounded-md border border-line bg-bg px-2 py-1.5 text-sm text-ink-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-actuator"
        >
          {field.options.map((o) => (
            <option key={o} value={o}>
              {o}
            </option>
          ))}
        </select>
      </label>
    );
  }

  if (field.type === "float" || field.type === "int") {
    const hasRange = field.min != null && field.max != null;
    return (
      <div className="text-sm">
        <div className="flex items-center justify-between">
          <span className="text-ink-secondary">{field.label_ko}</span>
          <span className="tabular-nums text-xs text-ink-primary">
            {value}
            {field.unit}
          </span>
        </div>
        {hasRange ? (
          <input
            type="range"
            min={field.min ?? undefined}
            max={field.max ?? undefined}
            step={field.step ?? (field.type === "int" ? 1 : 0.1)}
            value={Number(value)}
            onChange={(e) => onChange(Number(e.target.value))}
            className="mt-2 text-actuator"
          />
        ) : (
          <input
            type="number"
            value={Number(value)}
            onChange={(e) => onChange(Number(e.target.value))}
            className="mt-1 w-full rounded-md border border-line bg-bg px-2 py-1.5 text-ink-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-actuator"
          />
        )}
      </div>
    );
  }

  return (
    <label className="flex items-center justify-between text-sm">
      <span className="text-ink-secondary">{field.label_ko}</span>
      <input
        type="text"
        value={String(value)}
        onChange={(e) => onChange(e.target.value)}
        className="rounded-md border border-line bg-bg px-2 py-1.5 text-sm text-ink-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-actuator"
      />
    </label>
  );
}
