export const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export type Category = "sensor" | "actuator";
export type FieldType = "bool" | "float" | "int" | "string" | "color";

export interface CatalogField {
  key: string;
  label_ko: string;
  type: FieldType;
  unit?: string | null;
  min?: number | null;
  max?: number | null;
  step?: number | null;
  options?: string[] | null;
}

export interface CatalogComponent {
  type_key: string;
  category: Category;
  label_ko: string;
  note_ko: string;
  fields: CatalogField[];
}

export interface Device {
  id: number;
  team_name: string;
  api_key: string;
  is_online: boolean;
  last_seen_at: string | null;
}

export interface Component {
  id: number;
  device_id: number;
  type_key: string;
  category: Category;
  label: string;
  gpio_pin: string | null;
}

export interface Reading {
  id: number;
  component_id: number;
  value: Record<string, unknown>;
  recorded_at: string;
}

export interface Command {
  id: number;
  component_id: number;
  desired_state: Record<string, unknown>;
  actual_state: Record<string, unknown> | null;
  status: "pending" | "acked" | "failed";
  created_at: string;
  acked_at: string | null;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
    cache: "no-store",
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`API 오류 (${res.status}): ${body}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export const api = {
  listCatalog: () => request<CatalogComponent[]>("/api/catalog/components"),

  listDevices: () => request<Device[]>("/api/devices"),
  createDevice: (team_name: string) =>
    request<Device>("/api/devices", { method: "POST", body: JSON.stringify({ team_name }) }),
  getDevice: (deviceId: number) => request<Device>(`/api/devices/${deviceId}`),
  deleteDevice: (deviceId: number) => request<void>(`/api/devices/${deviceId}`, { method: "DELETE" }),

  listComponents: (deviceId: number) => request<Component[]>(`/api/devices/${deviceId}/components`),
  createComponent: (deviceId: number, type_key: string, label: string, gpio_pin?: string) =>
    request<Component>(`/api/devices/${deviceId}/components`, {
      method: "POST",
      body: JSON.stringify({ type_key, label, gpio_pin: gpio_pin || null }),
    }),
  deleteComponent: (deviceId: number, componentId: number) =>
    request<void>(`/api/devices/${deviceId}/components/${componentId}`, { method: "DELETE" }),

  listReadings: (deviceId: number, componentId: number, limit = 8) =>
    request<Reading[]>(`/api/devices/${deviceId}/components/${componentId}/readings?limit=${limit}`),

  sendCommand: (deviceId: number, componentId: number, desired_state: Record<string, unknown>) =>
    request<Command>(`/api/devices/${deviceId}/components/${componentId}/command`, {
      method: "POST",
      body: JSON.stringify({ desired_state }),
    }),
  latestCommand: (deviceId: number, componentId: number) =>
    request<Command | null>(`/api/devices/${deviceId}/components/${componentId}/command/latest`),
};
