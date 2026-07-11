// frontend/src/components/ui/FormField.jsx
export function Field({ label, hint, children }) {
    return (
        <label className="block">
            <span className="block text-xs font-medium text-muted mb-1.5">
                {label}
            </span>
            {children}
            {hint && <span className="block text-xs text-muted-2 mt-1">{hint}</span>}
        </label>
    );
}

export function Input({ className = "", ...props }) {
    return (
        <input
            className={`w-full h-9 rounded-lg border border-border bg-surface px-3 text-sm text-ink placeholder:text-muted-2 outline-none transition-all duration-150 focus:border-accent focus:ring-4 focus:ring-accent-soft ${className}`}
            {...props}
        />
    );
}

export function Select({ className = "", children, ...props }) {
    return (
        <select
            className={`w-full h-9 rounded-lg border border-border bg-surface px-3 text-sm text-ink outline-none transition-all duration-150 focus:border-accent focus:ring-4 focus:ring-accent-soft ${className}`}
            {...props}
        >
            {children}
        </select>
    );
}