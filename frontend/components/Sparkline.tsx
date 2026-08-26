/** 작은 추이 표시용 인라인 스파크라인. 색은 부모의 text color(currentColor)를 따른다. */
export function Sparkline({
  values,
  width = 88,
  height = 28,
}: {
  values: number[];
  width?: number;
  height?: number;
}) {
  if (values.length < 2) return null;

  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;
  const stepX = width / (values.length - 1);
  const pad = 3;

  const points = values.map((v, i) => {
    const x = i * stepX;
    const y = height - pad - ((v - min) / span) * (height - pad * 2);
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  });

  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} role="img" aria-label="최근 추이">
      <title>{values.map((v) => v.toFixed(1)).join(" → ")}</title>
      <polyline
        points={points.join(" ")}
        fill="none"
        stroke="currentColor"
        strokeWidth={2}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

/** bool 계열 센서(리드스위치, 버튼 등)용 — 최근 상태를 점 목록으로 보여준다. */
export function StateDots({ values }: { values: boolean[] }) {
  if (values.length === 0) return null;
  return (
    <div className="flex items-center gap-1" role="img" aria-label="최근 상태 변화">
      {values.map((v, i) => (
        <span
          key={i}
          className={`h-2 w-2 rounded-full ${v ? "bg-current" : "bg-white/20"}`}
          title={v ? "true" : "false"}
        />
      ))}
    </div>
  );
}
