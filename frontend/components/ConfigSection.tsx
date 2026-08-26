"use client";

import { useState } from "react";
import type { CatalogComponent, Component } from "@/lib/api";

export function ConfigSection({
  catalog,
  components,
  onAdd,
  onRemove,
}: {
  catalog: CatalogComponent[];
  components: Component[];
  onAdd: (typeKey: string, label: string) => Promise<void>;
  onRemove: (componentId: number) => Promise<void>;
}) {
  const [typeKey, setTypeKey] = useState("");
  const [label, setLabel] = useState("");

  const sensors = catalog.filter((c) => c.category === "sensor");
  const actuators = catalog.filter((c) => c.category === "actuator");

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    if (!typeKey || !label.trim()) return;
    await onAdd(typeKey, label.trim());
    setLabel("");
  }

  return (
    <details className="group rounded-md border border-line bg-surface">
      <summary className="flex cursor-pointer list-none items-center justify-between px-4 py-3 [&::-webkit-details-marker]:hidden">
        <span className="flex items-center gap-2">
          <svg
            className="chevron h-3 w-3 text-ink-muted"
            viewBox="0 0 8 8"
            fill="none"
            aria-hidden="true"
          >
            <path d="M2 0L6 4L2 8" stroke="currentColor" strokeWidth="1.5" />
          </svg>
          <span className="text-xs font-medium uppercase tracking-wide text-ink-muted">구성 관리</span>
        </span>
        <span className="text-xs text-ink-muted">{components.length}개 등록됨</span>
      </summary>

      <div className="border-t border-line px-4 py-4">
        <p className="text-xs text-ink-secondary">
          15종 중 실제 작품에서 쓰는 항목만 추가하세요. Mock 프로그램이 이 목록을 자동으로 읽어 동작합니다.
        </p>

        <form onSubmit={handleAdd} className="mt-3 flex flex-wrap gap-2">
          <select
            className="rounded-md border border-line bg-bg px-3 py-2 text-sm text-ink-primary"
            value={typeKey}
            onChange={(e) => setTypeKey(e.target.value)}
          >
            <option value="">종류 선택...</option>
            <optgroup label="센서">
              {sensors.map((c) => (
                <option key={c.type_key} value={c.type_key}>
                  {c.label_ko}
                </option>
              ))}
            </optgroup>
            <optgroup label="액추에이터">
              {actuators.map((c) => (
                <option key={c.type_key} value={c.type_key}>
                  {c.label_ko}
                </option>
              ))}
            </optgroup>
          </select>
          <input
            className="min-w-[140px] flex-1 rounded-md border border-line bg-bg px-3 py-2 text-sm text-ink-primary placeholder:text-ink-muted"
            placeholder="이름 (예: 거실 온습도)"
            value={label}
            onChange={(e) => setLabel(e.target.value)}
          />
          <button
            type="submit"
            className="rounded-md bg-white/10 px-4 py-2 text-sm font-medium text-ink-primary transition-colors hover:bg-white/20"
          >
            추가
          </button>
        </form>

        {components.length > 0 && (
          <ul className="mt-4 flex flex-wrap gap-2">
            {components.map((c) => (
              <li
                key={c.id}
                className="flex items-center gap-2 rounded-full border border-line bg-surface-raised px-3 py-1 text-xs"
              >
                <span className={c.category === "sensor" ? "text-sensor" : "text-actuator"}>
                  {c.category === "sensor" ? "센서" : "액추에이터"}
                </span>
                <span className="font-medium text-ink-primary">{c.label}</span>
                <span className="text-ink-muted">({c.type_key})</span>
                <button
                  onClick={() => onRemove(c.id)}
                  className="ml-1 text-ink-muted hover:text-status-critical"
                  aria-label={`${c.label} 삭제`}
                >
                  ×
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </details>
  );
}
