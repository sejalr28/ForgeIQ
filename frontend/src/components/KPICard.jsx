// frontend/src/components/KPICard.jsx
function KPICard({ icon: Icon, label, value, suffix, hint, tone = "neutral" }) {
  const toneMap = {
    neutral: "bg-accent-soft text-accent",
    warning: "bg-warning-soft text-warning",
    danger: "bg-danger-soft text-danger",
    success: "bg-success-soft text-success",
  };

  return (
    <div className="lift-hover bg-surface border border-border rounded-xl p-5">
      <div className="flex items-center justify-between mb-5">
        <span className="text-xs font-medium text-muted uppercase tracking-wide">
          {label}
        </span>
        {Icon && (
          <span
            className={`w-9 h-9 rounded-lg flex items-center justify-center ${toneMap[tone]}`}
          >
            <Icon size={16} strokeWidth={2} />
          </span>
        )}
      </div>
      <div className="flex items-end justify-between gap-2">
        <p className="text-[26px] leading-none font-semibold text-ink tabular-nums tracking-tight">
          {value}
          {suffix && (
            <span className="text-sm font-normal text-muted ml-1">{suffix}</span>
          )}
        </p>
        {hint && (
          <span className="text-xs font-medium text-muted-2 whitespace-nowrap pb-0.5">
            {hint}
          </span>
        )}
      </div>
    </div>
  );
}

export default KPICard;