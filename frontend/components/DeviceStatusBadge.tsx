import { StatusChip } from "@/components/StatusChip";

export function DeviceStatusBadge({ online }: { online: boolean }) {
  return <StatusChip tone={online ? "good" : "muted"} label={online ? "온라인" : "오프라인"} />;
}
