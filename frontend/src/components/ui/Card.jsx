// frontend/src/components/ui/Card.jsx
function Card({ children, className = "", padded = true, hover = false, ...props }) {
  return (
    <div
      className={`bg-surface border border-border rounded-xl ${
        padded ? "p-5" : ""
      } ${hover ? "lift-hover" : ""} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ title, subtitle, action }) {
  return (
    <div className="flex items-start justify-between mb-4">
      <div>
        <h3 className="text-sm font-semibold text-ink tracking-tight">{title}</h3>
        {subtitle && (
          <p className="text-xs text-muted mt-0.5">{subtitle}</p>
        )}
      </div>
      {action}
    </div>
  );
}

export default Card;