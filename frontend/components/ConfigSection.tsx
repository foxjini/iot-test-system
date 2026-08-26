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
    <section className="rounded-lg border border-gray-200 bg-white p-5">
      <h2 className="font-semibold">구성 관리 — 우리 팀이 사용하는 센서/액추에이터 선택</h2>
      <p className="mt-1 text-xs text-gray-500">
        15종 중 실제 작품에서 쓰는 항목만 추가하세요. Mock 프로그램이 이 목록을 자동으로 읽어 동작합니다.
      </p>

      <form onSubmit={handleAdd} className="mt-3 flex flex-wrap gap-2">
        <select
          className="rounded-md border border-gray-300 px-3 py-2 text-sm"
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
          className="min-w-[140px] flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm"
          placeholder="이름 (예: 거실 온습도)"
          value={label}
          onChange={(e) => setLabel(e.target.value)}
        />
        <button
          type="submit"
          className="rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-700"
        >
          추가
        </button>
      </form>

      {components.length > 0 && (
        <ul className="mt-4 flex flex-wrap gap-2">
          {components.map((c) => (
            <li
              key={c.id}
              className="flex items-center gap-2 rounded-full border border-gray-200 bg-gray-50 px-3 py-1 text-xs"
            >
              <span className="text-gray-400">{c.category === "sensor" ? "센서" : "액추에이터"}</span>
              <span className="font-medium">{c.label}</span>
              <span className="text-gray-400">({c.type_key})</span>
              <button
                onClick={() => onRemove(c.id)}
                className="ml-1 text-gray-400 hover:text-red-600"
                aria-label="삭제"
              >
                ×
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
