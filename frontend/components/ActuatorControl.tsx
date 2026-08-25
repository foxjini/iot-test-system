"use client";

import { useEffect, useState } from "react";
import { api, type CatalogComponent, type Command, type Component } from "@/lib/api";

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

  const statusLabel =
    lastCommand?.status === "acked" ? "실행 완료" : lastCommand?.status === "failed" ? "실패" : "대기 중";

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4">
      <div className="flex items-center justify-between">
        <span className="font-medium">{component.label}</span>
        <span className="text-xs text-gray-400">{catalogType.label_ko}</span>
      </div>

      <div className="mt-3 space-y-3">
        {catalogType.fields.map((f) => (
          <FieldControl key={f.key} field={f} value={values[f.key]} onChange={(v) => updateField(f.key, v)} />
        ))}
      </div>

      <button
        onClick={apply}
        disabled={sending}
        className="mt-3 w-full rounded-md bg-gray-900 px-3 py-1.5 text-sm font-medium text-white hover:bg-gray-700 disabled:opacity-50"
      >
        {sending ? "적용 중..." : "적용"}
      </button>

      {lastCommand && (
        <p className="mt-2 text-xs text-gray-400">
          마지막 명령: {statusLabel}
          {lastCommand.actual_state && ` · 실제 상태: ${JSON.stringify(lastCommand.actual_state)}`}
        </p>
      )}
    </div>
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
      <label className="flex items-center justify-between text-sm">
        <span className="text-gray-600">{field.label_ko}</span>
        <input type="checkbox" checked={Boolean(value)} onChange={(e) => onChange(e.target.checked)} className="h-4 w-4" />
      </label>
    );
  }

  if (field.type === "color") {
    const rgb = Array.isArray(value) ? value : [0, 0, 0];
    return (
      <label className="flex items-center justify-between text-sm">
        <span className="text-gray-600">{field.label_ko}</span>
        <input
          type="color"
          value={rgbToHex(rgb)}
          onChange={(e) => onChange(hexToRgb(e.target.value))}
          className="h-7 w-12 cursor-pointer rounded border border-gray-300"
        />
      </label>
    );
  }

  if (field.type === "string" && field.options?.length) {
    return (
      <label className="flex items-center justify-between text-sm">
        <span className="text-gray-600">{field.label_ko}</span>
        <select
          value={String(value)}
          onChange={(e) => onChange(e.target.value)}
          className="rounded-md border border-gray-300 px-2 py-1 text-sm"
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
          <span className="text-gray-600">{field.label_ko}</span>
          <span className="font-mono text-xs">
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
            className="mt-1 w-full"
          />
        ) : (
          <input
            type="number"
            value={Number(value)}
            onChange={(e) => onChange(Number(e.target.value))}
            className="mt-1 w-full rounded-md border border-gray-300 px-2 py-1"
          />
        )}
      </div>
    );
  }

  return (
    <label className="flex items-center justify-between text-sm">
      <span className="text-gray-600">{field.label_ko}</span>
      <input
        type="text"
        value={String(value)}
        onChange={(e) => onChange(e.target.value)}
        className="rounded-md border border-gray-300 px-2 py-1 text-sm"
      />
    </label>
  );
}
